from logging.config import fileConfig

from alembic import context
config = context.config

# -------------------------------------------- #

from app.models import Base
from app.core import settings
from sqlalchemy import create_engine

url_default = 'postgresql://{}:{}@{}:{}/{}'.format(
    settings.DATABASE_NAME,
    settings.DATABASE_PASSWORD,
    settings.DATABASE_HOST,
    settings.DATABASE_PORT,
    settings.DATABASE_NAME,
)

url_test = 'postgresql://{}:{}@{}:{}/{}'.format(
    settings.DATABASE_NAME + '_test',
    settings.DATABASE_PASSWORD,
    settings.DATABASE_HOST,
    settings.DATABASE_PORT,
    settings.DATABASE_NAME + '_test',
)

databases = {
    'default': url_default,
    'test': url_test
}

target_metadata = Base.metadata

# -------------------------------------------- #

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline(db_url) -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(db_url) -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = create_engine(db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    for db in databases.values():
        run_migrations_offline(db)
else:
    for db in databases.values():
        run_migrations_online(db)
