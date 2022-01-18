
# This file is part of CovidPy v0.0.5.
#
# The project has been distributed in the hope it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# You can use it and/or modify it under the terms of the GNU General Public License v3.0 or later.
# You should have received a copy of the GNU General Public License along with the project.
import io
from qrcode.image.pil import PilImage

class QRCode:
    def __init__(self, img:PilImage, rawdata:dict, in_blacklist:bool, instance) -> None:
        super().__init__()
        self.raw_data = rawdata
        self.pil_img = img
        self.in_blacklist = in_blacklist
        self.__cpyinstance = instance
    def save(self, path:str):
        self.pil_img.save(path)
    def to_bytesio(self)->io.BytesIO:
        bio = io.BytesIO()
        self.pil_img.save(bio)
        return bio
    def decode(self):
        self.__cpyinstance.decode(self)
    def verify(self):
        self.__cpyinstance.verify(self)

class VerifyResult:
    def __init__(self, is_valid:bool, is_revoked:bool):
        self.valid = is_valid
        self.revoked = is_revoked