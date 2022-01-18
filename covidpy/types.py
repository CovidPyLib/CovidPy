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