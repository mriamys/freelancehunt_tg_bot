import html
from aiogram import Router, F
from aiogram.types import CallbackQuery
from api.gemini import gemini_service
from utils.logger import logger

router = Router()

@router.callback_query(F.data == "apply_ai")
async def handle_apply_ai(callback: CallbackQuery):
    await callback.answer("Генерирую персональный отклик... ⏳")
    
    project_text = callback.message.text or callback.message.caption or ""
    response = await gemini_service.generate_response(project_text)
    
    # Разделяем отклик и инструкцию
    parts = response.split("[ИНСТРУКЦИЯ]")
    otklik = parts[0].replace("[ОТКЛИК]", "").strip()
    instruction = parts[1].strip() if len(parts) > 1 else ""
    
    msg_text = f"<b>Ваш отклик готов:</b>\n\n<code>{html.escape(otklik)}</code>\n\n<i>(Нажмите, чтобы скопировать)</i>"
    if instruction:
        msg_text += f"\n\n💡 <b>Инструкция по выполнению:</b>\n{html.escape(instruction)}"
        
    await callback.message.reply(msg_text)
