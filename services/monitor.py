import asyncio
from aiogram import Bot
from api.freelancehunt import FreelancehuntAPI
from database.storage import is_project_sent, save_sent_project
from bot.layouts import format_project_notification
from bot.keyboards import project_keyboard
from config import settings
from utils.logger import logger

fh_api = FreelancehuntAPI()

async def start_monitoring(bot: Bot):
    logger.info("Monitoring service started")
    while True:
        try:
            projects = fh_api.get_new_projects()
            for project in projects:
                p_id = int(project['id'])
                if not await is_project_sent(p_id):
                    # Отправляем
                    attrs = project['attributes']
                    employer_id = attrs.get('employer', {}).get('id')
                    stats = ""
                    if employer_id:
                        emp_info = fh_api.get_employer_info(employer_id)
                        rating = emp_info.get('rating', 0)
                        pos = emp_info.get('positive_reviews', 0)
                        neg = emp_info.get('negative_reviews', 0)
                        stats = f"(⭐ {rating} | 👍{pos} 👎{neg})"
                    
                    text = format_project_notification(project, stats)
                    url = fh_api.get_project_link(p_id, attrs.get('name', ''))
                    kb = project_keyboard(url)
                    
                    try:
                        await bot.send_message(chat_id=settings.CHAT_ID, text=text, reply_markup=kb)
                        await save_sent_project(p_id)
                        logger.info(f"New project sent: {attrs.get('name')}")
                        await asyncio.sleep(1) # Небольшая пауза между отправками
                    except Exception as e:
                        logger.error(f"Error sending project {p_id}: {e}")
            
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
        
        await asyncio.sleep(30) # Пауза между проверками API
