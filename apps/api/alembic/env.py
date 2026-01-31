from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from alembic import context
import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your models and config
from app.core.database import Base
from app.core.config import settings

# Import all models to ensure they're registered with Base.metadata
from app.models import *  # This imports all models in correct order

# this is the Alembic Config object
config = context.config

# Set the database URL in alembic config
config.set_main_option("sqlalchemy.url", settings.database_url_with_fallback)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

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
    """Run migrations in 'online' mode with retry logic."""
    url = config.get_main_option("sqlalchemy.url")
    
    # Configure engine with connection resilience
    engine_kwargs = {
        "poolclass": pool.NullPool,
        "pool_pre_ping": True,
    }
    
    # Add PostgreSQL specific settings
    if url.startswith("postgresql://"):
        engine_kwargs["connect_args"] = {
            "connect_timeout": 10,
            "sslmode": "require",
            "application_name": "creator_ai_alembic"
        }
    elif url.startswith("sqlite://"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            connectable = create_engine(url, **engine_kwargs)
            
            with connectable.connect() as connection:
                context.configure(
                    connection=connection, 
                    target_metadata=target_metadata
                )

                with context.begin_transaction():
                    context.run_migrations()
            
            print(f"✅ Migration completed successfully (attempt {attempt + 1})")
            return
            
        except Exception as e:
            print(f"❌ Migration attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("🚨 All migration attempts failed")
                if url.startswith("postgresql://"):
                    print("💡 Consider using SQLite for local development:")
                    print("   export DATABASE_URL='sqlite:///./creator_ai_local.db'")
                raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()