
# This file is part of CovidPy v0.0.5.
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.
import os
import qrcode
import zlib
import cbor2
import pyzbar.pyzbar
from base45 import b45encode, b45decode
from cose.algorithms import Es256
from cose.keys.curves import P256
from cose.algorithms import Es256
from cose.keys.keyparam import KpKty, KpAlg, EC2KpD, EC2KpCurve
from cose.headers import Algorithm, KID
from cose.keys import CoseKey
from cose.keys.keyparam import KpAlg, EC2KpD, EC2KpCurve
from cose.keys.keyparam import KpKty
from cose.keys.keytype import KtyEC2
from cose.messages import Sign1Message
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import PIL

from .verifier import DCCVerifier
from .types import QRCode, VerifyResult
from .errors import InvalidDCC

class CovidPy:
    def __init__(self, disable_keys_update:bool=False, disable_blalcklist_update:bool=False, disable_blacklist:bool=False) -> None:
        self.__autoblacklist = disable_blalcklist_update
        self.__autokids = disable_keys_update
        self.__disableblacklist = disable_blacklist
        self.__verifier = DCCVerifier(self.__autoblacklist, self.__autokids)
        self.__verifier.load_eu_keys()
        if not self.__disableblacklist:
            self.__verifier.load_blacklist()
        self.certspath = 'certs'

    def __decodecertificate(self, cert):
        img = PIL.Image.open(cert) if isinstance(cert, str) else cert.to_bytesio
        data = pyzbar.pyzbar.decode(img)
        try:
            cert = data[0].data.decode()
        except IndexError:
            raise InvalidDCC('The given code is not a DCC, check the \'details\' attribute for more details', 'QR_NOT_FOUND')
        if cert.startswith('HC1:'):
            b45data = cert.replace("HC1:", "")
            compresseddata = b45decode(b45data)
            decompressed = zlib.decompress(compresseddata)
            return decompressed
        else:
            raise InvalidDCC('The given code is not a DCC, check the \'details\' attribute for more details', 'HC1_MISSING')
    
    def __getUVCI(self,dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                if (val := self.__getUVCI(value)) is not None:
                    return val
            elif isinstance(value,list):
                for v in value:
                    if isinstance(v, dict):
                        ci = v.get('ci', None)
                        return ci
            else:
                if key == "ci":
                    return value
        else:
            return None
    
    def __is_blacklisted(self, raw:dict):
        ci = self.__getUVCI(raw)
        return ci in self.__verifier.blacklist

            
    def decode(self, cert): 
        cbordata = self.__decodecertificate(cert)
        decoded = cbor2.loads(cbordata)
        return cbor2.loads(decoded.value[2]) 

    def __finddatapaths(self): #TODO upload to pypi and remove this function
        rootdir = os.getcwd()

        for subdir, _, files in os.walk(rootdir):
            for file in files:
                filepath = subdir + os.sep + file

                if filepath.endswith("lib.py"):
                    return subdir + os.sep + 'certs'

    def __genqr(self, payload:dict):
        cbordata = cbor2.dumps(payload)
        with open(f'{self.certspath}\\dsc-worker.pem', "rb") as file:
            pem = file.read()
            cert = x509.load_pem_x509_certificate(pem)
            fingerprint = cert.fingerprint(hashes.SHA256())
            keyid = fingerprint[0:8]

        with open(f'{self.certspath}\\dsc-worker.key', "rb") as file:
            pem = file.read()
            keyfile = load_pem_private_key(pem, password=None)
            priv = keyfile.private_numbers().private_value.to_bytes(32, byteorder="big")

        msg = Sign1Message(phdr={Algorithm: Es256, KID: keyid}, payload=cbordata)

        cose_key = {
        KpKty: KtyEC2,
        KpAlg: Es256, 
        EC2KpCurve: P256, 
        EC2KpD: priv,
        }

        msg.key = CoseKey.from_dict(cose_key)
        out = msg.encode()

        out = zlib.compress(out, 9)

        out = b'HC1:' + b45encode(out).encode('ascii')

        return qrcode.make(out), out

    def encode(self, data:dict)->QRCode:
        gqr = self.__genqr(data)
        qr = QRCode(gqr[0], gqr[1],self.__is_blacklisted(data), self)
        return qr
    def verify(self, cert) -> VerifyResult:
        bl = self.__is_blacklisted(self.decode(cert))
        if not self.__disableblacklist and not bl:
            return VerifyResult(self.__verifier.is_valid(self.__decodecertificate(cert)), False)
        elif bl and self.__disableblacklist:
            return VerifyResult(self.__verifier.is_valid(self.__decodecertificate(cert)), None)
        elif bl and not self.__disableblacklist:
            return VerifyResult(False, True)