"""SQL queries used by BlockSure Flask routes."""
INSERT_USER = "INSERT INTO users(name,email,password,role,status) VALUES(?,?,?,?,?)"
GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email=?"
GET_USER_BY_ID = "SELECT * FROM users WHERE user_id=?"
GET_ALL_USERS = "SELECT user_id,name,email,role,status,created_at FROM users ORDER BY user_id DESC"
UPDATE_USER_STATUS = "UPDATE users SET status=? WHERE user_id=?"

INSERT_MANUFACTURER = "INSERT INTO manufacturers(user_id,company_name,address,contact_no) VALUES(?,?,?,?)"
GET_MANUFACTURER_BY_USER = "SELECT * FROM manufacturers WHERE user_id=?"
INSERT_SELLER = "INSERT INTO sellers(user_id,shop_name,address,contact_no) VALUES(?,?,?,?)"
GET_SELLER_BY_USER = "SELECT * FROM sellers WHERE user_id=?"
INSERT_CUSTOMER = "INSERT INTO customers(user_id,name,address,contact_no) VALUES(?,?,?,?)"
GET_CUSTOMER_BY_USER = "SELECT * FROM customers WHERE user_id=?"

INSERT_PRODUCT = """
INSERT INTO products(product_code,product_name,brand,batch_number,manufacturing_date,expiry_date,price,manufacturer_id,seller_id,status)
VALUES(?,?,?,?,?,?,?,?,?,?)
"""
GET_PRODUCT_BY_CODE = """
SELECT p.*,m.company_name,s.shop_name FROM products p
LEFT JOIN manufacturers m ON p.manufacturer_id=m.manufacturer_id
LEFT JOIN sellers s ON p.seller_id=s.seller_id
WHERE p.product_code=?
"""
GET_PRODUCT_BY_ID = "SELECT * FROM products WHERE product_id=?"
GET_ALL_PRODUCTS = """
SELECT p.*,m.company_name,s.shop_name FROM products p
LEFT JOIN manufacturers m ON p.manufacturer_id=m.manufacturer_id
LEFT JOIN sellers s ON p.seller_id=s.seller_id
ORDER BY p.product_id DESC
"""
GET_PRODUCTS_BY_MANUFACTURER = "SELECT * FROM products WHERE manufacturer_id=? ORDER BY product_id DESC"
GET_PRODUCTS_BY_SELLER = "SELECT * FROM products WHERE seller_id=? ORDER BY product_id DESC"
UPDATE_PRODUCT_STATUS = "UPDATE products SET status=?,updated_at=CURRENT_TIMESTAMP WHERE product_id=?"
ASSIGN_PRODUCT_TO_SELLER = "UPDATE products SET seller_id=?,status=?,updated_at=CURRENT_TIMESTAMP WHERE product_id=?"

INSERT_BLOCK = """
INSERT INTO blockchain(block_number,product_id,product_code,action,from_user,to_user,location,timestamp,previous_hash,current_hash,extra_data)
VALUES(?,?,?,?,?,?,?,?,?,?,?)
"""
GET_BLOCKCHAIN_HISTORY = "SELECT * FROM blockchain WHERE product_code=? ORDER BY block_number ASC"
GET_LAST_BLOCK = "SELECT * FROM blockchain ORDER BY block_number DESC LIMIT 1"

INSERT_TRANSACTION = "INSERT INTO transactions(product_id,from_user,to_user,action,location,date_time) VALUES(?,?,?,?,?,?)"
GET_PRODUCT_TRANSACTIONS = "SELECT * FROM transactions WHERE product_id=? ORDER BY transaction_id ASC"
INSERT_QR = "INSERT INTO qr_codes(product_id,qr_code,qr_path,generated_at) VALUES(?,?,?,?)"
GET_QR_BY_PRODUCT = "SELECT * FROM qr_codes WHERE product_id=? ORDER BY qr_id DESC LIMIT 1"
INSERT_SCAN = "INSERT INTO scan_logs(product_id,scan_location,scan_time,result,ip_address) VALUES(?,?,?,?,?)"
GET_SCAN_HISTORY = "SELECT * FROM scan_logs WHERE product_id=? ORDER BY scan_id DESC"
INSERT_WARRANTY = "INSERT INTO warranty(product_id,start_date,end_date,status) VALUES(?,?,?,?)"
GET_WARRANTY_BY_PRODUCT = "SELECT * FROM warranty WHERE product_id=? ORDER BY warranty_id DESC LIMIT 1"
INSERT_COMPLAINT = "INSERT INTO complaints(product_id,customer_id,complaint_text,status,date) VALUES(?,?,?,?,?)"
GET_ALL_COMPLAINTS = """
SELECT c.*,p.product_code,p.product_name,cu.name customer_name FROM complaints c
LEFT JOIN products p ON c.product_id=p.product_id
LEFT JOIN customers cu ON c.customer_id=cu.customer_id
ORDER BY c.complaint_id DESC
"""
GET_ADMIN_COUNTS = """
SELECT
(SELECT COUNT(*) FROM users) users_count,
(SELECT COUNT(*) FROM manufacturers) manufacturers_count,
(SELECT COUNT(*) FROM sellers) sellers_count,
(SELECT COUNT(*) FROM products) products_count,
(SELECT COUNT(*) FROM scan_logs) scans_count
"""
