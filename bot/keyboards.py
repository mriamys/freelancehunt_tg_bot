from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def project_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Открыть на сайте", url=url)],
            [
                InlineKeyboardButton(
                    text="🤖 Хочу откликнуться (AI)", callback_data="apply_ai"
                )
            ],
        ]
    )
