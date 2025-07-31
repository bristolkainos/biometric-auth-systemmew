from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings
import logging
import time

logger = logging.getLogger(__name__)

# Create database engine with improved connection pooling for Railway
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=3,  # Smaller pool for development
    max_overflow=5,  # Reduced overflow for development
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_timeout=10,  # Reduced timeout for development
    echo=False if settings.ENVIRONMENT == "production" else settings.DEBUG  # Disable debug in production
    # Note: connect_args removed as they may not be compatible with all PostgreSQL drivers
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables with retry logic"""
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            break
        except Exception as e:
            logger.error(f"Database initialization attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying database initialization in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.error("All database initialization attempts failed")
                raise

def test_db_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            result.fetchone()
            logger.info("Database connection test successful")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False 