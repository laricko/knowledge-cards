from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool, text

from alembic import context

from db.base import metadata
from config import get_settings

settings = get_settings()

base_database_url = settings.DATABASE_URL
postgres_db = settings._POSTGRES_DB


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    if os.environ.get("TESTING"):
        raise ValueError("Running testing migrations offline currently not permitted.")
    url = base_database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    database_url = (
        f"{base_database_url}_test" if os.environ.get("TESTING") else base_database_url
    )
    # handle testing config for migrations
    if os.environ.get("TESTING"):
        # connect to primary db
        default_engine = create_engine(
            base_database_url, pool_pre_ping=True, isolation_level="AUTOCOMMIT"
        )
        # drop testing db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(text(f"DROP DATABASE IF EXISTS {postgres_db}_test"))
            default_conn.execute(text(f"CREATE DATABASE {postgres_db}_test"))

    config.set_main_option("sqlalchemy.url", database_url)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=database_url,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
