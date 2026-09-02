A backend project that demonstrates the business logic of a hotel booking system using PostgreSQL. Focuses on database design, raw SQL query writing, relationships between entities, CRUD operations, transactions, and asynchronous database access with asyncpg.

## Guide
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

#### 4. Populate the database with sample data

```bash
psql -U <username> -d hotel_booking_system -f faker_values.sql
```

#### 5. Run the application

```bash
make dev
```

## Testing

The project uses a separate PostgreSQL database for integration tests.

#### 1. Create a test database

Open PostgreSQL:
```bash
psql -U <username>
```
Create a separate database owned by your PostgreSQL user:
```sql
CREATE DATABASE <test_db_name> OWNER <username>;
```

#### 2. Apply migrations to the empty test database

Run all Alembic migrations against the test database:

```bash
alembic -x db_url='postgresql://<username>:<password>@localhost/<test_db_name>' upgrade head
```
> This creates the complete schema in the test database, including tables, foreign keys, constraints, and extensions defined by the migration history.

⚠️ The Alembic **`env.py` must be configured** to read the database URL passed through the -x argument.

Use the following configuration:
```python
db_url = context.get_x_argument(as_dictionary=True).get("db_url")

config.set_main_option(
    "sqlalchemy.url",
    db_url or os.getenv("DATABASE_URL")
)
```
> This allows Alembic to use the database URL provided through -x db_url. If no -x db_url argument is provided, it falls back to the DATABASE_URL environment variable.

#### 3. Verify the database schema

Connect to the test database:
```bash
psql -U <username> -d <test_db_name>
```

Check that the tables were created:

```bash
\dt
```
