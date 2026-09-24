from typing import Any

from app.db import Database


class HotelAnalyticsRepository():
    """
    Provides database access for hotel analytics queries.
    """

    def __init__(self):
        self.db = Database()

    async def room_type_counts(
        self,
        hotel_id: int
    ) -> list[dict[str, Any]]:
        query = """--sql
            SELECT
                rt.id AS room_type_id,
                rt.room_type,
                COUNT(r.id) AS room_count
            FROM rooms AS r
            INNER JOIN room_types AS rt
                ON rt.id = r.room_type_id
            WHERE r.hotel_id = $1
            GROUP BY
                rt.id,
                rt.room_type
            ORDER BY rt.id;
        """
        return await self.db.fetch(query, hotel_id)

    async def monthly_bookings(
        self,
        hotel_id: int,
    ) -> list[dict[str, Any]]:
        '''
        query = """--sql
            SELECT
                DATE_TRUNC('month', check_in_date) AS month,
                COUNT(*) AS booking_count
            FROM bookings
            WHERE hotel_id = $1  # ! add hotel_id in table bookings
            GROUP BY DATE_TRUNC('month', check_in_date)
            ORDER BY month;
        """
        return await self.db.fetch(query, hotel_id)
        '''

    async def room_type_popularity(
        self,
        hotel_id: int,
    ) -> list[dict[str, Any]]:
        query = """--sql
            WITH room_type_stats AS (
                SELECT
                    rt.id AS room_type_id,
                    rt.room_type,
                    COUNT(b.id) AS booking_count
                FROM bookings AS b
                INNER JOIN rooms AS r
                    ON r.id = b.room_id
                INNER JOIN room_types AS rt
                    ON rt.id = r.room_type_id
                WHERE r.hotel_id = $1
                GROUP BY
                    rt.id,
                    rt.room_type
            )
            SELECT
                room_type_id,
                room_type,
                booking_count,
                ROW_NUMBER() OVER (
                    ORDER BY booking_count DESC, room_type_id
                ) AS rank
            FROM room_type_stats
            ORDER BY rank;
        """
        return await self.db.fetch(query, hotel_id)
