import os
import qrcode

QR_FOLDER = os.path.join("static", "qr_codes")
os.makedirs(QR_FOLDER, exist_ok=True)


def generate_qr(product_code):

    # CHANGE THIS IP TO YOUR LAPTOP'S IPv4 ADDRESS
    verification_url = f"http://192.168.167.1:5000/verify/{product_code}"

    filename = f"{product_code}.png"
    path = os.path.join(QR_FOLDER, filename)

    img = qrcode.make(verification_url)
    img.save(path)

    return path