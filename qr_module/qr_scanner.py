from pyzbar.pyzbar import decode
from PIL import Image

def scan_qr(image_path):
    image=Image.open(image_path)
    result=decode(image)
    if not result:
        return None
    return result[0].data.decode("utf-8")
