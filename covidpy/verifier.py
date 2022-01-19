
# Copyright (c) 2022, CovidPyLib
# This file is part of CovidPy v0.0.8.
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.

from base64 import b64encode, b64decode
from cose.headers import KID
import requests, json
from cose.algorithms import Es256
from cose.keys.curves import P256
from cose.algorithms import Es256, Ps256
from cose.keys import CoseKey
from cose.keys.keyparam import KpAlg, EC2KpX, EC2KpY, EC2KpCurve, RSAKpE, RSAKpN
from cose.keys.keyparam import KpKty
from cose.keys.keytype import KtyEC2, KtyRSA
from cose.messages import CoseMessage
from cryptography.utils import int_to_bytes
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives import serialization
import schedule

class DCCVerifier:
    def __init__(self, disblrefresh, diskidsrefresh):
        self.diskidsrefresh = diskidsrefresh
        self.disblrefresh = disblrefresh
        self.kids:dict = {}
        self.sched = None
        self.blacklist:list = []
        if not self.disblrefresh and not self.diskidsrefresh:
            self.sched = schedule.every().day.at("08:00").do(self.reload_all)
        elif self.disblrefresh and not self.diskidsrefresh:
            self.sched = schedule.every().day.at("08:00").do(self.reload_kids)
        elif self.diskidsrefresh and not self.disblrefresh:
            self.sched = schedule.every().day.at("08:00").do(self.reload_bl)

    def reload_all(self):
        self.reload_kids()
        self.reload_bl()

    def reload_bl(self):
        self.blacklist = []
        self.load_blacklist()
    
    def reload_kids(self):
        self.kids = {}
        self.load_eu_keys()

    def append_kid(self, kid_b64, key_b64):
        asn1data = b64decode(key_b64)

        pub = serialization.load_der_public_key(asn1data)
        if (isinstance(pub, RSAPublicKey)):
              self.kids[kid_b64] = CoseKey.from_dict(
               {
                    KpAlg: Ps256, 
                    KpKty: KtyRSA,
                    RSAKpE: int_to_bytes(pub.public_numbers().e),
                    RSAKpN: int_to_bytes(pub.public_numbers().n)
               })
        elif (isinstance(pub, EllipticCurvePublicKey)):
              self.kids[kid_b64] = CoseKey.from_dict(
               {
                    EC2KpCurve: P256, 
                    KpKty: KtyEC2, 
                    KpAlg: Es256,  
                    EC2KpX: pub.public_numbers().x.to_bytes(32, byteorder="big"),
                    EC2KpY: pub.public_numbers().y.to_bytes(32, byteorder="big")
               })
        else:
            pass #INVALID TYPE 

    def load_blacklist(self):
        settings = requests.get('https://get.dgc.gov.it/v1/dgc/settings').json()
        for sett in settings:
            if sett.get('name',None) == 'black_list_uvci':
                self.blacklist = sett.get('value').split(';')
                break

    def load_eu_keys(self):
        keys = requests.get('https://verifier-api.coronacheck.nl/v4/verifier/public_keys')
        kjson = keys.json()
        payload = b64decode(kjson['payload'])
        trustlist = json.loads(payload)
        eutrusts = trustlist['eu_keys']
        for b64kid in eutrusts:
            self.append_kid(b64kid,eutrusts[b64kid][0]['subjectPk'])
    def is_valid(self, key):
        cose = CoseMessage.decode(key)
        a_kid = cose.phdr[KID] if KID in cose.phdr.keys() else cose.uhdr[KID]
        b64_a_kid = b64encode(a_kid).decode('ASCII')
        if not b64_a_kid in self.kids:
            return False
        else:
            key  = self.kids[b64_a_kid]

            cose.key = key
            if not cose.verify_signature():
                return False
            else:
                return True