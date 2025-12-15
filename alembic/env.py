from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

from sqlmodel import SQLModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import the app settings to get the database URL
try:
    from app.settings import settings
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
except Exception:
    db_url = config.get_main_option("sqlalchemy.url")

target_metadata = SQLModel.metadata


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        url=db_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise RuntimeError("Offline mode not supported by this env.py")
else:
    run_migrations_online()
