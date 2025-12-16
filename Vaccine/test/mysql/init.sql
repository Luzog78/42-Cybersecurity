-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    stock INT DEFAULT 0
);

-- Create secret_data table (the "hidden" sensitive data)
CREATE TABLE IF NOT EXISTS secret_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    confidential_info VARCHAR(255),
    api_key VARCHAR(100),
    notes TEXT
);

-- Insert dummy users
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@company.com', 'admin'),
('john_doe', 'password123', 'john@example.com', 'user'),
('jane_smith', 'pass456', 'jane@example.com', 'user'),
('bob_wilson', 'qwerty', 'bob@example.com', 'user'),
('alice_brown', 'letmein', 'alice@example.com', 'moderator');

-- Insert dummy products
INSERT INTO products (name, description, price, stock) VALUES
('Laptop', 'High performance laptop', 999.99, 15),
('Mouse', 'Wireless optical mouse', 29.99, 50),
('Keyboard', 'Mechanical gaming keyboard', 149.99, 30),
('Monitor', '27 inch 4K display', 449.99, 20),
('Webcam', 'HD video camera', 79.99, 25);

-- Insert secret data (what attackers might want to find)
INSERT INTO secret_data (confidential_info, api_key, notes) VALUES
('Credit Card Processing Key: 4532-XXXX-XXXX-9876', 'sk_live_51H8fKj*********qr5st6uv7wx8yz', 'Production API key - DO NOT SHARE'),
('Database Backup Location: /backup/prod_db_2024', 'backup_token_ABC123XYZ789', 'Weekly automated backups'),
('Admin Portal URL: https://secret-admin.company.com', 'admin_session_token_987654', 'Emergency access only');
