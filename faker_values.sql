TRUNCATE TABLE Guests RESTART IDENTITY CASCADE;
TRUNCATE TABLE Hotels RESTART IDENTITY CASCADE;
TRUNCATE TABLE Room_Type RESTART IDENTITY CASCADE;
TRUNCATE TABLE Rooms RESTART IDENTITY CASCADE;

INSERT INTO Guests (First_name, Last_name, Email, Phone, Password_hash)
VALUES
('Иван', 'Иванов', 'ivan.ivanov@example.com', '+79990000001', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Петр', 'Петров', 'petr.petrov@example.com', '+79990000002', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Анна', 'Сидорова', 'anna.sidorova@example.com', '+79990000003', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Мария', 'Кузнецова', 'maria.kuznetsova@example.com', '+79990000004', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Алексей', 'Смирнов', 'alexey.smirnov@example.com', '+79990000005', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Екатерина', 'Попова', 'ekaterina.popova@example.com', '+79990000006', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Дмитрий', 'Васильев', 'dmitry.vasilyev@example.com', '+79990000007', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Ольга', 'Новикова', 'olga.novikova@example.com', '+79990000008', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Сергей', 'Федоров', 'sergey.fedorov@example.com', '+79990000009', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Наталья', 'Морозова', 'natalia.morozova@example.com', '+79990000010', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Максим', 'Волков', 'maxim.volkov@example.com', '+79990000011', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Елена', 'Алексеева', 'elena.alekseeva@example.com', '+79990000012', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Артем', 'Лебедев', 'artem.lebedev@example.com', '+79990000013', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Татьяна', 'Семенова', 'tatyana.semenova@example.com', '+79990000014', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Кирилл', 'Павлов', 'kirill.pavlov@example.com', '+79990000015', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Дарья', 'Орлова', 'daria.orlova@example.com', '+79990000016', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Никита', 'Егоров', 'nikita.egorov@example.com', '+79990000017', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Виктория', 'Николаева', 'victoria.nikolaeva@example.com', '+79990000018', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Андрей', 'Захаров', 'andrey.zakharov@example.com', '+79990000019', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW'),
('Юлия', 'Беляева', 'yulia.belyaeva@example.com', '+79990000020', '$2a$12$gRnhRZBhD/9MOrSOiYRNQ.p.B13d7hvQJBszGzOF01TIU4j0aj4oW');

INSERT INTO Hotels (name, address, description)
VALUES
('Grand Palace Hotel', 'Москва, ул. Тверская 10', 'Пятизвездочный отель в центре города'),
('Sea Breeze Resort', 'Сочи, ул. Морская 25', 'Отель рядом с морем'),
('Mountain View Hotel', 'Красная Поляна, ул. Горная 5', 'Отель с видом на горы'),
('Royal Garden', 'Санкт-Петербург, Невский проспект 50', 'Исторический отель'),
('Sunrise Hotel', 'Казань, ул. Баумана 15', 'Современный городской отель'),
('Green Valley', 'Алтай, ул. Лесная 8', 'Отель среди природы'),
('Ocean Star', 'Калининград, ул. Побережная 12', 'Отель у Балтийского моря'),
('City Lights Hotel', 'Екатеринбург, ул. Ленина 30', 'Бизнес-отель'),
('Golden Bridge', 'Владивосток, ул. Светланская 20', 'Отель с видом на залив'),
('Lake View Resort', 'Карелия, ул. Озерная 7', 'Курортный отель');

INSERT INTO Room_Types (room_type)
VALUES
('Single'),
('Double'),
('Deluxe');

INSERT INTO Rooms (
    room_number,
    room_floor,
    is_active,
    hotel_id,
    room_type_id
)
VALUES
('101', '1', TRUE, 1, 1),
('102', '1', TRUE, 1, 2),
('201', '2', TRUE, 2, 3),
('202', '2', TRUE, 2, 2),
('301', '3', TRUE, 3, 3),
('302', '3', FALSE, 4, 1),
('401', '4', TRUE, 5, 2),
('402', '4', TRUE, 6, 3),
('501', '5', TRUE, 7, 1),
('502', '5', FALSE, 8, 2);

INSERT INTO Bookings (
    guest_id,
    room_id,
    check_in_date,
    check_out_date
)
VALUES
(1, 1, '2026-01-05', '2026-01-10'),
(2, 2, '2026-01-12', '2026-01-15'),
(3, 3, '2026-02-01', '2026-02-07'),
(4, 4, '2026-02-10', '2026-02-14'),
(5, 5, '2026-03-01', '2026-03-05'),
(6, 6, '2026-03-10', '2026-03-13'),
(7, 7, '2026-04-02', '2026-04-08'),
(8, 8, '2026-04-15', '2026-04-20'),
(9, 9, '2026-05-01', '2026-05-06'),
(10, 10, '2026-05-10', '2026-05-15')
