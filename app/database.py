from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# Ruta de la base de datos SQLite (archivo local)
DATABASE_URL = "sqlite:///./app.db"

# Crea el motor de conexión a la base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Clase base de la que heredarán todos los modelos
class Base(DeclarativeBase):
    pass

# Dependencia para obtener y cerrar sesión de una DB en cada petición
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
