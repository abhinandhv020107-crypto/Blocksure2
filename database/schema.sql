PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS warranty;
DROP TABLE IF EXISTS scan_logs;
DROP TABLE IF EXISTS qr_codes;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS blockchain;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS manufacturers;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
 user_id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 email TEXT UNIQUE NOT NULL,
 password TEXT NOT NULL,
 role TEXT NOT NULL CHECK(role IN ('admin','manufacturer','seller','customer')),
 status TEXT NOT NULL DEFAULT 'Active',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE manufacturers(
 manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER UNIQUE NOT NULL,
 company_name TEXT NOT NULL,
 address TEXT,
 contact_no TEXT,
 FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE sellers(
 seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER UNIQUE NOT NULL,
 shop_name TEXT NOT NULL,
 address TEXT,
 contact_no TEXT,
 FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE customers(
 customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER UNIQUE NOT NULL,
 name TEXT NOT NULL,
 address TEXT,
 contact_no TEXT,
 FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE products(
 product_id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_code TEXT UNIQUE NOT NULL,
 product_name TEXT NOT NULL,
 brand TEXT,
 batch_number TEXT,
 manufacturing_date TEXT,
 expiry_date TEXT,
 price REAL DEFAULT 0 CHECK(price>=0),
 manufacturer_id INTEGER NOT NULL,
 seller_id INTEGER,
 status TEXT NOT NULL DEFAULT 'Created',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(manufacturer_id) REFERENCES manufacturers(manufacturer_id),
 FOREIGN KEY(seller_id) REFERENCES sellers(seller_id)
);
CREATE TABLE blockchain(
 block_id INTEGER PRIMARY KEY AUTOINCREMENT,
 block_number INTEGER NOT NULL,
 product_id INTEGER,
 product_code TEXT NOT NULL,
 action TEXT NOT NULL,
 from_user TEXT,
 to_user TEXT,
 location TEXT,
 timestamp TEXT NOT NULL,
 previous_hash TEXT NOT NULL,
 current_hash TEXT UNIQUE NOT NULL,
 extra_data TEXT,
 FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
CREATE INDEX idx_blockchain_product_code ON blockchain(product_code);
CREATE TABLE transactions(
 transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL,
 from_user INTEGER,
 to_user INTEGER,
 action TEXT NOT NULL,
 location TEXT,
 date_time TEXT NOT NULL,
 FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE,
 FOREIGN KEY(from_user) REFERENCES users(user_id),
 FOREIGN KEY(to_user) REFERENCES users(user_id)
);
CREATE TABLE qr_codes(
 qr_id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL,
 qr_code TEXT UNIQUE NOT NULL,
 qr_path TEXT,
 generated_at TEXT NOT NULL,
 FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
CREATE TABLE scan_logs(
 scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER,
 scan_location TEXT,
 scan_time TEXT NOT NULL,
 result TEXT NOT NULL,
 ip_address TEXT,
 FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE SET NULL
);
CREATE TABLE warranty(
 warranty_id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL,
 start_date TEXT,
 end_date TEXT,
 status TEXT,
 FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE
);
CREATE TABLE complaints(
 complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL,
 customer_id INTEGER NOT NULL,
 complaint_text TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'Open',
 date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE,
 FOREIGN KEY(customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);
