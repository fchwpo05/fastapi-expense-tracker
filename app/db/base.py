from sqlalchemy.orm import declarative_base
from app.db.session import engine

# Base class that all models will inherit from
Base = declarative_base()

# We Import all models here so Alembic can detect them
# We have set target_metadata = Base.metadata in alembic/env.py)



from app.db.models import user