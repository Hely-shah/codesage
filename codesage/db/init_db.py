from codesage.db.session import engine
from codesage.db.models import Base

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
