import json
import logging
import aiohttp
import html
from config import settings
from bio import BIO
from utils.logger import logger

class GeminiService:
    def __init__(self):
        self.keys = settings.gemini_keys_list
        self.url_template = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={}"

    def _prepare_prompt(self, project_text: str) -> str:
        skills_str = "\n- ".join(BIO["main_skills"])
        portfolio_str = "\n".join([f"- {p['title']}: {p['url']}" for p in BIO["portfolio"]])
        
        prompt = f"""Ты — интеллектуальный ассистент фрилансера по имени {BIO['name']}. 
Твоя задача: проанализировать проект и составить идеальный отклик + инструкцию.

ДАННЫЕ ФРИЛАНСЕРА:
Имя: {BIO['name']}
Специализация: {BIO['specialization']}
Навыки:
- {skills_str}

Портфолио (используй ссылки, только если они подходят по теме):
{portfolio_str}

ПРАВИЛА ОТВЕТА (СТРОГО):
1. ЯЗЫК: Определи язык описания проекта. Если он на УКРАИНСКОМ — отвечай СТРОГО на украинском. Если на РУССКОМ — на русском. Никогда не смешивай языки.
2. ОТКЛИК:
    - Без воды, 2-3 коротких предложения.
    - Если задача подходит под портфолио — упомяни это и вставь ОДНУ самую релевантную ссылку из списка выше.
    - Если проект не в компетенции — пиши "Маю досвід у рутинних задачах" (или на рус аналогично).
    - Формат: "Здравствуйте... готов помочь... [кейс из портфолио]... Буду рад обсудить!"
3. ИНСТРУКЦИЯ ПО ВЫПОЛНЕНИЮ:
    - Вместо промпта выдай конкретный пошаговый алгоритм (1, 2, 3), как Дмитрий может выполнить эту задачу быстро с помощью Gemini Pro или других инструментов.
4. ОЦЕНКА (СКОРИНГ):
    - В начале инструкции поставь оценку сложности от 1 до 5 и пометку релевантности (⭐⭐⭐⭐⭐).

СТРУКТУРА ОТВЕТА:
[ОТКЛИК]
(текст отклика)

[ИНСТРУКЦИЯ]
(оценка и пошаговый план)

ТЕКСТ ПРОЕКТА:
{project_text}"""
        return prompt

    async def generate_response(self, project_text: str) -> str:
        prompt = self._prepare_prompt(project_text)
        
        for key in self.keys:
            url = self.url_template.format(key)
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7}
            }
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, timeout=20) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return data['candidates'][0]['content']['parts'][0]['text'].strip()
                        else:
                            logger.warning(f"Gemini key failed (status {resp.status})")
            except Exception as e:
                logger.error(f"Gemini API error: {e}")
                
        return "❌ Не удалось сгенерировать отклик. Все лимиты исчерпаны."

gemini_service = GeminiService()
