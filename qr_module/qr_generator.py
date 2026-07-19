import os

import qrcode


QR_FOLDER = os.path.join("static", "qr_codes")

# Create the folder automatically if it does not exist
os.makedirs(QR_FOLDER, exist_ok=True)


def generate_qr(product_code):
    """
    Generate a QR code containing the BlockSure verification URL.
    """

    product_code = product_code.strip().upper()

    # Laptop Wi-Fi IPv4 address
    verification_url = (
        f"http://192.168.1.4:5000/verify/{product_code}"
    )

    filename = f"{product_code}.png"
    qr_path = os.path.join(QR_FOLDER, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    image.save(qr_path)

    return qr_path
