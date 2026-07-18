from database.database import Database

db = Database()

# ---------------- USERS ----------------

INSERT_USER = """
INSERT INTO users(name,email,password,role,status)
VALUES(?,?,?,?,?)
"""

GET_USER_BY_EMAIL = """
SELECT * FROM users
WHERE email=?
"""

# ---------------- MANUFACTURER ----------------

INSERT_MANUFACTURER = """
INSERT INTO manufacturers(
user_id,
company_name,
address,
contact_no
)
VALUES(?,?,?,?)
"""

# ---------------- SELLER ----------------

INSERT_SELLER = """
INSERT INTO sellers(
user_id,
shop_name,
address,
contact_no
)
VALUES(?,?,?,?)
"""

# ---------------- CUSTOMER ----------------

INSERT_CUSTOMER = """
INSERT INTO customers(
user_id,
name,
address,
contact_no
)
VALUES(?,?,?,?)
"""

# ---------------- PRODUCTS ----------------

INSERT_PRODUCT = """
INSERT INTO products(
product_code,
product_name,
brand,
batch_number,
manufacturing_date,
expiry_date,
price,
manufacturer_id,
seller_id,
status
)
VALUES(?,?,?,?,?,?,?,?,?,?)
"""

GET_PRODUCT = """
SELECT *
FROM products
WHERE product_code=?
"""

GET_ALL_PRODUCTS = """
SELECT *
FROM products
"""

UPDATE_PRODUCT_STATUS = """
UPDATE products
SET status=?
WHERE product_id=?
"""

# ---------------- BLOCKCHAIN ----------------

INSERT_BLOCK = """
INSERT INTO blockchain(
block_number,
product_id,
action,
timestamp,
previous_hash,
current_hash,
extra_data
)
VALUES(?,?,?,?,?,?,?)
"""

GET_BLOCKCHAIN_HISTORY = """
SELECT *
FROM blockchain
WHERE product_id=?
ORDER BY block_number
"""

# ---------------- TRANSACTIONS ----------------

INSERT_TRANSACTION = """
INSERT INTO transactions(
product_id,
from_user,
to_user,
action,
location,
date_time
)
VALUES(?,?,?,?,?,?)
"""

# ---------------- QR ----------------

INSERT_QR = """
INSERT INTO qr_codes(
product_id,
qr_code,
qr_path,
generated_at
)
VALUES(?,?,?,?)
"""

GET_QR = """
SELECT *
FROM qr_codes
WHERE product_id=?
"""

# ---------------- SCAN LOGS ----------------

INSERT_SCAN = """
INSERT INTO scan_logs(
product_id,
scan_location,
scan_time,
result,
ip_address
)
VALUES(?,?,?,?,?)
"""

GET_SCAN_HISTORY = """
SELECT *
FROM scan_logs
WHERE product_id=?
"""

# ---------------- WARRANTY ----------------

INSERT_WARRANTY = """
INSERT INTO warranty(
product_id,
start_date,
end_date,
status
)
VALUES(?,?,?,?)
"""

# ---------------- COMPLAINTS ----------------

INSERT_COMPLAINT = """
INSERT INTO complaints(
product_id,
customer_id,
complaint_text,
status,
date
)
VALUES(?,?,?,?,?)
"""
