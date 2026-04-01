from core.db import engine
from core.db_models import Base

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Done Tables created.")