CREATE DATABASE IF NOT EXISTS aquaflow;
USE aquaflow;

CREATE TABLE IF NOT EXISTS stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS refilling_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    volume_liters DECIMAL(10,2) NOT NULL,
    customer_name VARCHAR(100),
    amount_paid DECIMAL(10,2),
    payment_method ENUM('cash', 'gcash', 'transfer') DEFAULT 'cash',
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id)
);

INSERT INTO stations (name, location) VALUES 
('Station A', 'Downtown Cagayan de Oro'),
('Station B', 'Uptown Cagayan de Oro');
