DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS warranty;
DROP TABLE IF EXISTS scan_logs;
DROP TABLE IF EXISTS qr_codes;
DROP TABLE IF EXISTS blockchain;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS manufacturers;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT DEFAULT 'Active'
);

CREATE TABLE manufacturers(
    manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    company_name TEXT NOT NULL,
    address TEXT,
    contact_no TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE sellers(
    seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    shop_name TEXT NOT NULL,
    address TEXT,
    contact_no TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE customers(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    address TEXT,
    contact_no TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE products(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code TEXT UNIQUE NOT NULL,
    product_name TEXT NOT NULL,
    brand TEXT,
    batch_number TEXT,
    manufacturing_date TEXT,
    expiry_date TEXT,
    price REAL,
    manufacturer_id INTEGER,
    seller_id INTEGER,
    status TEXT DEFAULT 'Created',

    FOREIGN KEY(manufacturer_id)
        REFERENCES manufacturers(manufacturer_id),

    FOREIGN KEY(seller_id)
        REFERENCES sellers(seller_id)
);

CREATE TABLE blockchain(
    block_id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_number INTEGER,
    product_id INTEGER,
    action TEXT,
    timestamp TEXT,
    previous_hash TEXT,
    current_hash TEXT,
    extra_data TEXT,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

CREATE TABLE transactions(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    from_user INTEGER,
    to_user INTEGER,
    action TEXT,
    location TEXT,
    date_time TEXT,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

CREATE TABLE qr_codes(
    qr_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    qr_code TEXT,
    qr_path TEXT,
    generated_at TEXT,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

CREATE TABLE scan_logs(
    scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    scan_location TEXT,
    scan_time TEXT,
    result TEXT,
    ip_address TEXT,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

CREATE TABLE warranty(
    warranty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    start_date TEXT,
    end_date TEXT,
    status TEXT,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
);

CREATE TABLE complaints(
    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    customer_id INTEGER,
    complaint_text TEXT,
    status TEXT,
    date TEXT,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id),

    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
);
