from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery
from typing import Tuple, Any
from dataclasses import dataclass, field
from aiogram.contrib.middlewares.i18n import (
    I18nMiddleware as BaseI18nMiddleware)

chat_settings = CallbackData("chat", "id", "property", "value")


@dataclass
class LanguageData:
    flag: str
    title: str
    label: str = field(init=False, default=None)

    def __post_init__(self):
        self.label = f"{self.flag} {self.title}"


class I18nMiddleware(BaseI18nMiddleware):

    users = {}

    AVAILABLE_LANGUAGES = {
        "en": LanguageData("🇺🇸", "English"),
        "ru": LanguageData("🇷🇺", "Русский"),
    }

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        if isinstance(args[0], CallbackQuery):
            cdata: CallbackQuery = args[0]
            if cdata.data and "chat" in cdata.data:
                settings = chat_settings.parse(cdata.data)
                self.users[cdata.from_user.id] = settings['value']
        return self.users.get(args[0].from_user.id, self.default)
