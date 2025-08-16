import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy.pool import NullPool

from alembic import context

# Añade la raíz del proyecto al path de Python para que se pueda encontrar el módulo 'app'
sys.path.append(str(Path(__file__).resolve().parents[1]))

# --- IMPORTANTE: Importa aquí tus modelos y la Base ---
# Esto asegura que SQLAlchemy los "registre" antes de que Alembic intente autogenerar
from app.db.base import Base
from app.db.models import user, logs # Asegúrate de que estos import reflejen tus archivos de modelos

# ----------------------------------------------------

# Lee la configuración de Alembic desde el archivo .ini
config = context.config

# Configura el logging para Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Asigna los metadatos de tu Base a target_metadata ---
# Este es el paso clave para la autogeneración
target_metadata = Base.metadata
# ----------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()