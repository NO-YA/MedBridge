"""Utility script to create DB tables in the configured DATABASE_URL.

Run with:
    python create_tables.py
"""
import asyncio

from medbridge import db


async def main():
    await db.init_db()


if __name__ == "__main__":
    asyncio.run(main())
