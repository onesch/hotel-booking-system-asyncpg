A backend project that demonstrates the business logic of a hotel booking system using PostgreSQL. Focuses on database design, raw SQL query writing, relationships between entities, CRUD operations, transactions, and asynchronous database access with asyncpg.

#### 1. Create the PostgreSQL database

```sql
CREATE DATABASE hotel_booking_system;
```

#### 2. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/hotel_booking_system
```

#### 3. Create the database schema

```bash
psql -U <username> -d hotel_booking_system -f app/db_services/database.sql
```

#### 4. Populate the database with sample data

```bash
psql -U <username> -d hotel_booking_system -f app/db_services/faker_values.sql
```

#### 5. Run the application

```bash
make dev
```
