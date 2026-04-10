import asyncio
from database.storage import clean_old_projects
from utils.logger import logger

async def start_cleaner():
    logger.info("Cleaner service started")
    while True:
        try:
            await clean_old_projects(days=30)
        except Exception as e:
            logger.error(f"Error in cleaner service: {e}")
        
        await asyncio.sleep(86400) # Раз в сутки
