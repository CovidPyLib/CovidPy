# Copyright (c) 2022, CovidPyLib
# This file is part of CovidPy v0.1.2
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.

import platform
import zlib
import qrcode
import cbor2

try:
    import pyzbar.pyzbar
except ImportError as import_error:
    if platform.system() == "Windows":
        raise ImportError(
            """ERROR: pyzbar or zbar not found CovidPy won't work without it
            since you are on windows zbar should be included with pyzbar."""
        ) from import_error
    if platform.system() == "Linux":
        raise ImportError(
            """ERROR: pyzbar or zbar not found CovidPy won't work without it
            please install pyzbar using pip or zbar using your package manager.
            example: sudo apt install libzbar0 on debian-based distros."""
        ) from import_error
    if platform.system() == "Darwin":
        raise ImportError(
            """ERROR: pyzbar or zbar not found CovidPy won't work without it
            please install pyzbar using pip or zbar using your package manager.
            example: brew install zbar on Mac OS X."""
        ) from import_error
    raise ImportError(
        """ERROR: pyzbar or zbar not found CovidPy won't work without it
        please install pyzbar using pip or zbar using your package manager."""
    ) from import_error

from base45 import b45encode, b45decode
from cose.algorithms import Es256
from cose.keys.curves import P256
from cose.keys.keyparam import KpKty, KpAlg, EC2KpD, EC2KpCurve
from cose.headers import Algorithm, KID
from cose.keys import CoseKey
from cose.keys.keytype import KtyEC2
from cose.messages import Sign1Message
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import PIL

from .verifier import DCCVerifier
from .types import QRCode, VerifyResult, Certificate
from .errors import InvalidDCC

class CovidPy:
    def __init__(
        self,
        disable_keys_update: bool = False,
        disable_blacklist_update: bool = False,
        disable_blacklist: bool = False,
    ) -> None:
        self.__autoblacklist = disable_blacklist_update
        self.__autokids = disable_keys_update
        self.__disableblacklist = disable_blacklist
        self.__verifier = DCCVerifier(self.__autoblacklist, self.__autokids)
        self.__verifier.load_eu_keys()
        if not self.__disableblacklist:
            self.__verifier.load_blacklist()
        self.__dscworkerpem = (r'-----BEGIN CERTIFICATE-----'
r'MIIBXzCCAQUCEBcHI+fTFbKUN8AhX4B41swwCgYIKoZIzj0EAwIwMjEjMCEGA1UE'
r'AwwaTmF0aW9uYWwgQ1NDQSBvZiBGcmllc2xhbmQxCzAJBgNVBAYTAkZSMB4XDTIx'
r'MTEwMTEzMTQyMVoXDTI2MDkxNjEzMTQyMVowNjEnMCUGA1UEAwweRFNDIG51bWJl'
r'ciB3b3JrZXIgb2YgRnJpZXNsYW5kMQswCQYDVQQGEwJGUjBZMBMGByqGSM49AgEG'
r'CCqGSM49AwEHA0IABABcawF9OaBFQtkkmoS35RV6hgs+7MvT4uAkmIivAxQc8jka'
r'1SgdagspK4S+Q1KbhN0rB/L0M8dwnGJACQDtE8YwCgYIKoZIzj0EAwIDSAAwRQIg'
r'V3UerYPuSfvPJ19j7NKMzh5Hupn2x4poKsWfZp+sZbMCIQDY3qjg8RT/ALfiyfV+'
r'HTnXm2xsSKEv5Mafw88CaUqMsA=='
r'-----END CERTIFICATE-----')
        self.__dscworkerkey = (r'-----BEGIN EC PRIVATE KEY-----'
r'MHcCAQEEIOWIj7qstVUIO0k6GszFh9i+9HGXBC+Sxf3G+3sHU0a7oAoGCCqGSM49'
r'AwEHoUQDQgAEAFxrAX05oEVC2SSahLflFXqGCz7sy9Pi4CSYiK8DFBzyORrVKB1q'
r'CykrhL5DUpuE3SsH8vQzx3CcYkAJAO0Txg=='
r'-----END EC PRIVATE KEY-----')


    def __decodecertificate(self, cert):
        img = PIL.Image.open(cert) if isinstance(cert, str) else cert.to_bytesio
        data = pyzbar.pyzbar.decode(img)
        try:
            cert = data[0].data.decode()
        except IndexError as index_error:
            raise InvalidDCC(
                "The given code is not a DCC, check the 'details' attribute for more details",
                "QR_NOT_FOUND",
            ) from index_error
        if cert.startswith("HC1:"):
            b45data = cert.replace("HC1:", "")
            compresseddata = b45decode(b45data)
            return zlib.decompress(compresseddata)

        raise InvalidDCC(
            "The given code is not a DCC, check the 'details' attribute for more details",
            "HC1_MISSING",
        )

    def __get_uvci(self, cert):
        if isinstance(cert, Certificate):
            return cert.certificate[0].certificate_identifier
        else:
            raise InvalidDCC(
                "The given code is not a DCC, check the 'details' attribute for more details",
                "UNKNOWN_CERTIFICATE",
            )

    def __is_blacklisted(self, raw: dict):
        ci_value = self.__get_uvci(raw)
        return ci_value in self.__verifier.blacklist

    def decode(self, cert) -> Certificate:
        cbordata = self.__decodecertificate(cert)
        decoded = cbor2.loads(cbordata)
        cbl = cbor2.loads(decoded.value[2])
        return Certificate(cbl)

    def __genqr(self, payload: dict):
        cbordata = cbor2.dumps(payload) #pem load
        cert = x509.load_pem_x509_certificate(self.__dscworkerpem)
        fingerprint = cert.fingerprint(hashes.SHA256())
        keyid = fingerprint[:8]


        keyfile = load_pem_private_key(self.__dscworkerkey, password=None) #key load
        priv = keyfile.private_numbers().private_value.to_bytes(32, byteorder="big")

        msg = Sign1Message(phdr={Algorithm: Es256, KID: keyid}, payload=cbordata)

        cose_key = {
            KpKty: KtyEC2,
            KpAlg: Es256,
            EC2KpCurve: P256,
            EC2KpD: priv,
        }

        msg.key = CoseKey.from_dict(cose_key)

        out = zlib.compress(msg.encode(), 9)

        out = b"HC1:" + b45encode(out).encode("ascii")

        return qrcode.make(out), out

    def encode(self, data: dict) -> QRCode:
        gen_qr = self.__genqr(data)
        return QRCode(gen_qr[0], gen_qr[1], self.__is_blacklisted(data), self)

    def verify(self, cert) -> VerifyResult:
        revoked = self.__is_blacklisted(self.decode(cert))
        if not revoked and not self.__disableblacklist:
            return VerifyResult(
                self.__verifier.is_valid(self.__decodecertificate(cert)), False
            )
        if revoked and self.__disableblacklist:
            return VerifyResult(
                self.__verifier.is_valid(self.__decodecertificate(cert)), None
            )
        if revoked and not self.__disableblacklist:
            return VerifyResult(False, True)

        return VerifyResult(
            self.__verifier.is_valid(self.__decodecertificate(cert)), False
        )
