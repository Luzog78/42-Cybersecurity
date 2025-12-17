CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    role TEXT DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    stock INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS secret_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    confidential_info TEXT,
    api_key TEXT,
    notes TEXT
);

INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@company.com', 'admin'),
('john_doe', 'password123', 'john@example.com', 'user'),
('jane_smith', 'pass456', 'jane@example.com', 'user'),
('bob_wilson', 'qwerty', 'bob@example.com', 'user'),
('alice_brown', 'letmein', 'alice@example.com', 'moderator');

INSERT INTO products (name, description, price, stock) VALUES
('Laptop', 'High performance laptop', 999.99, 15),
('Mouse', 'Wireless optical mouse', 29.99, 50),
('Keyboard', 'Mechanical gaming keyboard', 149.99, 30),
('Monitor', '27 inch 4K display', 449.99, 20),
('Webcam', 'HD video camera', 79.99, 25);

INSERT INTO secret_data (confidential_info, api_key, notes) VALUES
('Credit Card Processing Key: 4532-XXXX-XXXX-9876', 'sk_live_51H8fKj*********qr5st6uv7wx8yz', 'Production API key - DO NOT SHARE'),
('Database Backup Location: /backup/prod_db_2024', 'backup_token_ABC123XYZ789', 'Weekly automated backups'),
('Admin Portal URL: https://secret-admin.company.com', 'admin_session_token_987654', 'Emergency access only');
