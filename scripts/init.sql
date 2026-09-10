CREATE DATABASE IF NOT EXISTS restaurante_db;
USE restaurante_db;

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    fecha_registro DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_pedido DATETIME NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pedidos_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_fecha ON pedidos(fecha_pedido);
CREATE INDEX idx_pedidos_estado ON pedidos(estado);
CREATE INDEX idx_clientes_email ON clientes(email);

INSERT INTO clientes (nombre, email, telefono, direccion, fecha_registro) VALUES
('Juan Perez', 'juan.perez@example.com', '999111222', 'Av. Lima 123', '2024-01-15'),
('Maria Garcia', 'maria.garcia@example.com', '999333444', 'Jr. Cusco 456', '2024-02-20'),
('Carlos Lopez', 'carlos.lopez@example.com', '999555666', 'Calle Arequipa 789', '2024-03-10');

INSERT INTO pedidos (cliente_id, fecha_pedido, total, estado) VALUES
(1, '2024-04-01 12:30:00', 45.50, 'entregado'),
(1, '2024-04-15 19:00:00', 32.00, 'entregado'),
(2, '2024-04-20 13:45:00', 78.90, 'en preparacion'),
(3, '2024-05-05 20:15:00', 120.00, 'pendiente');