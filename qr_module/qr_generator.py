import os
import qrcode

QR_FOLDER=os.path.join("static","qr_codes")
os.makedirs(QR_FOLDER,exist_ok=True)

def generate_qr(product_code):
    data=f"PRODUCT:{product_code}"
    filename=f"{product_code}.png"
    path=os.path.join(QR_FOLDER,filename)
    img=qrcode.make(data)
    img.save(path)
    return path
