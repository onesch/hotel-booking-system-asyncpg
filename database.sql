CREATE TABLE IF NOT EXISTS Guests (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Hotels (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Room_Types (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    room_type VARCHAR(30) CHECK (room_type IN ('Single', 'Double', 'Deluxe'))
);

CREATE TABLE IF NOT EXISTS Rooms (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    room_number VARCHAR(50) NOT NULL,
    room_floor VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT False,

    hotel_id INTEGER NOT NULL,
    room_type_id INTEGER NOT NULL,

    CONSTRAINT fk_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES Hotels(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_room_type
        FOREIGN KEY (room_type_id)
        REFERENCES Room_Types(id)
        ON DELETE RESTRICT
);

CREATE TABLE if not exists Bookings (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    guest_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,

    CONSTRAINT fk_guest
        FOREIGN KEY (guest_id)
        REFERENCES Guests(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_room
        FOREIGN KEY (room_id)
        REFERENCES Rooms(id)
        ON DELETE CASCADE
);
