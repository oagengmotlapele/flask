import base64
from dataclasses import dataclass
@dataclass
class Encode:
    def base64Encode(self,pictures_dict:dict[str,str]):
        encoded_pictures={}
        for i in pictures_dict:
            with open(pictures_dict[i], "rb") as img_file:
                encoded_pictures[i]=base64.b64encode(img_file.read()).decode('utf-8')
        return encoded_pictures