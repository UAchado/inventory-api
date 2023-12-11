CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

CREATE TABLE IF NOT EXISTS items (
    id INT PRIMARY KEY auto_increment,
    description VARCHAR(30),
    tag VARCHAR(50),
    image VARCHAR(500) NULL,
    state VARCHAR(50),
    dropoff_point_id INT NULL,
    report_email VARCHAR(100) NULL,
    retrieved_email VARCHAR(100) NULL,
    retrieved_date VARCHAR(100) NULL
);

insert into items (id, description, tag, image, state, dropoff_point_id, report_email, retrieved_email, retrieved_date) values 
(1, 'description_opt', 'Tablets', null, 'stored', 1, null, null, null),
(2, 'description_opt', 'Carregadores', 'image_opt', 'stored', 1, null, null, null),
(3, 'description_opt', 'Carregadores', 'image_opt', 'stored', 1, null, null, null),
(4, 'description_opt', 'Telemóveis', null, 'stored', 1, null, null, null),
(5, 'description_opt', 'Tablets', null, 'stored', 1, null, null, null),
(6, 'description_opt', 'Telemóveis', null, 'stored', 1, null, null, null),
(7, 'description_opt', 'Telemóveis', 'image_opt', 'stored', 1, null, null, null),
(8, 'description_opt', 'Telemóveis', 'image_opt', 'stored', 1, null, null, null),
(9, 'description_opt', 'Carregadores', 'image_opt', 'stored', 1, null, null, null),
(10, 'description_opt', 'Auscultadores/Fones', 'image_opt', 'stored', 1, null, null, null),
(11, 'description_opt', 'Telemóveis', null, 'stored', 1, null, null, null),
(12, 'description_opt', 'Portáteis', null, 'stored', 1, null, null, null),
(13, 'description_opt', 'Tablets', 'image_opt', 'stored', 1, null, null, null),
(14, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(15, 'description_opt', 'Portáteis', 'image_opt', 'stored', 1, null, null, null),
(16, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(17, 'description_opt', 'Carregadores', null, 'stored', 1, null, null, null),
(18, 'description_opt', 'Tablets', 'image_opt', 'stored', 1, null, null, null),
(19, 'description_opt', 'Telemóveis', null, 'stored', 1, null, null, null),
(20, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(21, 'description_opt', 'Telemóveis', null, 'stored', 1, null, null, null),
(22, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(23, 'description_opt', 'Tablets', 'image_opt', 'stored', 1, null, null, null),
(24, 'description_opt', 'Auscultadores/Fones', 'image_opt', 'stored', 1, null, null, null),
(25, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(26, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(27, 'description_opt', 'Auscultadores/Fones', 'image_opt', 'stored', 1, null, null, null),
(28, 'description_opt', 'Auscultadores/Fones', 'image_opt', 'stored', 1, null, null, null),
(29, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(30, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(31, 'description_opt', 'Auscultadores/Fones', null, 'stored', 1, null, null, null),
(32, 'description_opt', 'Carregadores', null, 'stored', 1, null, null, null),
(33, 'description_opt', 'Tablets', 'image_opt', 'stored', 1, null, null, null),
(34, 'description_opt', 'Portáteis', null, 'stored', 1, null, null, null),
(35, 'description_opt', 'Tablets', 'image_opt', 'stored', 1, null, null, null);