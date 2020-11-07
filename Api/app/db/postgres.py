import asyncpg
import dotenv
import os

dotenv.load_dotenv()


async def create_connection_pool():
    return await asyncpg.create_pool(
        user=os.environ['PG_USER'], 
        password=os.environ['PG_PASSWORD'],
        database=os.environ['PG_DB'], 
        host=os.environ['PG_HOST'], 
        max_size=10,
        )
