from psycopg2 import pool
import os
from dotenv import load_dotenv
import time
import logging
from typing import Optional
from app.core.config import settings

load_dotenv()

logger = logging.getLogger(__name__)

class DatabasePool:
    _pool: Optional[pool.SimpleConnectionPool] = None
    
    @classmethod
    def get_pool(cls, min_conn=1, max_conn=10):
        if cls._pool is None:
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    cls._pool = pool.SimpleConnectionPool(
                        min_conn,
                        max_conn,
                        user=settings.DB_USER,
                        password=settings.DB_PASSWORD,
                        host=settings.DB_HOST,
                        port=settings.DB_PORT,
                        database=settings.DB_NAME
                    )
                    logger.info("Database pool created successfully")
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        logger.error(f"Failed to create database pool after {max_retries} attempts: {str(e)}")
                        raise
                    logger.warning(f"Failed to create pool (attempt {retry_count}): {str(e)}")
                    time.sleep(2 ** retry_count)  # Exponential backoff
        
        return cls._pool
    
    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.get_pool()
        
        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                connection = cls._pool.getconn()
                logger.debug("Database connection acquired from pool")
                return connection
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    logger.error(f"Failed to get connection from pool after {max_retries} attempts")
                    raise
                logger.warning(f"Failed to get connection (attempt {retry_count}): {str(e)}")
                time.sleep(2 ** retry_count)
    
    @classmethod
    def return_connection(cls, connection):
        cls._pool.putconn(connection)
        logger.debug("Database connection returned to pool")
    
    @classmethod
    def close_all(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            logger.info("All database connections closed")
            cls._pool = None
