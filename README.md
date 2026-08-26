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

#### 3. Apply all database migrations

```bash
alembic upgrade head
```

#### 3. Populate the database with sample data

```bash
psql -U <username> -d hotel_booking_system -f faker_values.sql
```

#### 4. Run the application

```bash
make dev
```
