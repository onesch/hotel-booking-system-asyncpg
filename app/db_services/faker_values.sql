TRUNCATE TABLE Guests RESTART IDENTITY CASCADE;
TRUNCATE TABLE Hotels RESTART IDENTITY CASCADE;
TRUNCATE TABLE Room_Type RESTART IDENTITY CASCADE;
TRUNCATE TABLE Rooms RESTART IDENTITY CASCADE;

INSERT INTO Guests (First_name, Last_name, Email, Phone)
VALUES
('Иван', 'Иванов', 'ivan.ivanov@example.com', '+79990000001'),
('Петр', 'Петров', 'petr.petrov@example.com', '+79990000002'),
('Анна', 'Сидорова', 'anna.sidorova@example.com', '+79990000003'),
('Мария', 'Кузнецова', 'maria.kuznetsova@example.com', '+79990000004'),
('Алексей', 'Смирнов', 'alexey.smirnov@example.com', '+79990000005'),
('Екатерина', 'Попова', 'ekaterina.popova@example.com', '+79990000006'),
('Дмитрий', 'Васильев', 'dmitry.vasilyev@example.com', '+79990000007'),
('Ольга', 'Новикова', 'olga.novikova@example.com', '+79990000008'),
('Сергей', 'Федоров', 'sergey.fedorov@example.com', '+79990000009'),
('Наталья', 'Морозова', 'natalia.morozova@example.com', '+79990000010'),
('Максим', 'Волков', 'maxim.volkov@example.com', '+79990000011'),
('Елена', 'Алексеева', 'elena.alekseeva@example.com', '+79990000012'),
('Артем', 'Лебедев', 'artem.lebedev@example.com', '+79990000013'),
('Татьяна', 'Семенова', 'tatyana.semenova@example.com', '+79990000014'),
('Кирилл', 'Павлов', 'kirill.pavlov@example.com', '+79990000015'),
('Дарья', 'Орлова', 'daria.orlova@example.com', '+79990000016'),
('Никита', 'Егоров', 'nikita.egorov@example.com', '+79990000017'),
('Виктория', 'Николаева', 'victoria.nikolaeva@example.com', '+79990000018'),
('Андрей', 'Захаров', 'andrey.zakharov@example.com', '+79990000019'),
('Юлия', 'Беляева', 'yulia.belyaeva@example.com', '+79990000020');

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
