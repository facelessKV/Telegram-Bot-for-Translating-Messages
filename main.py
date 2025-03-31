import os
import json
import logging
import asyncio
from typing import Dict, Any
import httpx
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, hitalic
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация бота
# Замените на ваш токен
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Замените на ваш ключ API для перевода
# Для Google Translate API: https://cloud.google.com/translate/docs/setup
TRANSLATE_API_KEY = 'YOUR_TRANSLATE_API_KEY'

# Можно использовать другие API перевода, например:
# - Google Translate API
# - Yandex Translate API
# - Microsoft Translator API
# - DeepL API

# Определение состояний для FSM (Finite State Machine)
class UserState(StatesGroup):
    waiting_for_text = State()  # Ожидание текста для перевода

# Словарь для хранения пользовательских настроек
# В реальном проекте лучше использовать базу данных
user_preferences = {}

# Поддерживаемые языки (код: название)
SUPPORTED_LANGUAGES = {
    'en': 'Английский',
    'ru': 'Русский',
    'fr': 'Французский',
    'de': 'Немецкий',
    'es': 'Испанский',
    'it': 'Итальянский',
    'zh': 'Китайский',
    'ja': 'Японский',
    'ko': 'Корейский',
    'ar': 'Арабский',
    'hi': 'Хинди',
    'pt': 'Португальский',
}

# Функция сохранения пользовательских настроек
def save_user_preferences():
    """Сохраняет пользовательские настройки в JSON файл"""
    with open('user_preferences.json', 'w', encoding='utf-8') as f:
        json.dump(user_preferences, f, ensure_ascii=False, indent=4)

# Функция загрузки пользовательских настроек
def load_user_preferences():
    """Загружает пользовательские настройки из JSON файла"""
    global user_preferences
    try:
        with open('user_preferences.json', 'r', encoding='utf-8') as f:
            user_preferences = json.load(f)
    except FileNotFoundError:
        user_preferences = {}

# Функция для определения языка текста
async def detect_language(text: str) -> str:
    """
    Определяет язык входного текста с помощью Google Translate API
    
    Args:
        text: Текст для определения языка
        
    Returns:
        Код языка (например, 'en', 'ru')
    """
    # URL для Google Translate API - detect language
    url = f"https://translation.googleapis.com/language/translate/v2/detect"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                params={"key": TRANSLATE_API_KEY},
                data={"q": text}
            )
            
            if response.status_code == 200:
                result = response.json()
                detected_language = result["data"]["detections"][0][0]["language"]
                return detected_language
            else:
                logger.error(f"Error detecting language: {response.text}")
                return "en"  # Возвращаем английский по умолчанию в случае ошибки
    
    except Exception as e:
        logger.error(f"Exception when detecting language: {e}")
        return "en"  # Возвращаем английский по умолчанию в случае ошибки

# Функция для перевода текста
async def translate_text(text: str, target_lang: str, source_lang: str = None) -> str:
    """
    Переводит текст с одного языка на другой с помощью Google Translate API
    
    Args:
        text: Текст для перевода
        target_lang: Целевой язык (код, например 'en', 'ru')
        source_lang: Исходный язык (код). Если None, будет определен автоматически
        
    Returns:
        Переведенный текст
    """
    # URL для Google Translate API
    url = f"https://translation.googleapis.com/language/translate/v2"
    
    params = {
        "key": TRANSLATE_API_KEY,
        "q": text,
        "target": target_lang,
    }
    
    if source_lang:
        params["source"] = source_lang
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, params=params)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result["data"]["translations"][0]["translatedText"]
                return translated_text
            else:
                logger.error(f"Error translating text: {response.text}")
                return "Ошибка перевода. Пожалуйста, попробуйте позже."
    
    except Exception as e:
        logger.error(f"Exception when translating: {e}")
        return "Произошла ошибка при переводе. Пожалуйста, попробуйте позже."

# Создаем роутер для обработки сообщений
router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start - отправляет приветственное сообщение"""
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    
    # Устанавливаем язык по умолчанию, если пользователь новый
    if user_id not in user_preferences:
        user_preferences[user_id] = {"target_lang": "en"}
        save_user_preferences()
    
    welcome_text = (
        f"👋 Привет, {user_name}!\n\n"
        f"Я бот-переводчик. Вот что я умею:\n"
        f"• /translate - перевести текст\n"
        f"• /set_lang - изменить язык перевода\n\n"
        f"Текущий язык перевода: {hbold(SUPPORTED_LANGUAGES[user_preferences[user_id]['target_lang']])}"
    )
    
    await message.answer(welcome_text, parse_mode=ParseMode.HTML)

# Обработчик команды /translate
@router.message(Command("translate"))
async def cmd_translate(message: Message, state: FSMContext):
    """Обработчик команды /translate - запрашивает текст для перевода"""
    await message.answer("📝 Пожалуйста, введите текст для перевода:")
    await state.set_state(UserState.waiting_for_text)

# Обработчик текста для перевода
@router.message(StateFilter(UserState.waiting_for_text))
async def process_text_to_translate(message: Message, state: FSMContext):
    """Обрабатывает полученный текст и выполняет перевод"""
    user_id = str(message.from_user.id)
    text_to_translate = message.text
    
    # Получаем целевой язык из настроек пользователя
    target_lang = user_preferences.get(user_id, {}).get("target_lang", "en")
    
    # Определяем исходный язык текста
    await message.answer("🔍 Определяю язык и перевожу...")
    source_lang = await detect_language(text_to_translate)
    
    # Если исходный язык совпадает с целевым, меняем целевой
    if source_lang == target_lang:
        # Если текст на английском, переводим на русский, иначе на английский
        target_lang = "ru" if source_lang == "en" else "en"
    
    # Переводим текст
    translated_text = await translate_text(text_to_translate, target_lang, source_lang)
    
    # Формируем ответ
    response = (
        f"📋 {hbold('Исходный текст:')}\n"
        f"{text_to_translate}\n\n"
        f"🌍 {hbold('Исходный язык:')} {SUPPORTED_LANGUAGES.get(source_lang, source_lang)}\n\n"
        f"🔤 {hbold('Перевод')} ({SUPPORTED_LANGUAGES.get(target_lang, target_lang)}):\n"
        f"{translated_text}"
    )
    
    await message.answer(response, parse_mode=ParseMode.HTML)
    await state.clear()

# Обработчик команды /set_lang
@router.message(Command("set_lang"))
async def cmd_set_lang(message: Message):
    """Обработчик команды /set_lang - предлагает выбрать язык перевода"""
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    
    # Создаем кнопки для каждого поддерживаемого языка
    # Группируем кнопки по 2 в ряд
    rows = []
    current_row = []
    
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        current_row.append(types.InlineKeyboardButton(
            text=lang_name,
            callback_data=f"lang_{lang_code}"
        ))
        
        if len(current_row) == 2:
            rows.append(current_row)
            current_row = []
    
    # Добавляем оставшиеся кнопки, если есть
    if current_row:
        rows.append(current_row)
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=rows)
    
    await message.answer(
        "🌐 Выберите язык перевода:",
        reply_markup=keyboard
    )

# Обработчик инлайн-кнопок выбора языка
@router.callback_query(F.data.startswith('lang_'))
async def process_callback_language(callback: CallbackQuery):
    """Обрабатывает выбор языка перевода"""
    # Подтверждаем получение колбэка
    await callback.answer()
    
    user_id = str(callback.from_user.id)
    lang_code = callback.data.split('_')[1]
    
    # Сохраняем выбранный язык в настройках пользователя
    if user_id not in user_preferences:
        user_preferences[user_id] = {}
    
    user_preferences[user_id]["target_lang"] = lang_code
    save_user_preferences()
    
    await callback.message.answer(
        f"✅ Язык перевода изменен на: {SUPPORTED_LANGUAGES[lang_code]}"
    )

# Обработчик для прямого перевода текста (без команды /translate)
@router.message(F.text & ~F.text.startswith('/'))
async def direct_translate(message: Message):
    """Обрабатывает текстовые сообщения для прямого перевода"""
    user_id = str(message.from_user.id)
    text_to_translate = message.text
    
    # Получаем целевой язык из настроек пользователя
    target_lang = user_preferences.get(user_id, {}).get("target_lang", "en")
    
    # Определяем исходный язык текста
    source_lang = await detect_language(text_to_translate)
    
    # Если исходный язык совпадает с целевым, меняем целевой
    if source_lang == target_lang:
        # Если текст на английском, переводим на русский, иначе на английский
        target_lang = "ru" if source_lang == "en" else "en"
    
    # Переводим текст
    translated_text = await translate_text(text_to_translate, target_lang, source_lang)
    
    # Формируем ответ
    response = (
        f"🌍 {hbold(SUPPORTED_LANGUAGES.get(source_lang, source_lang))} → "
        f"{hbold(SUPPORTED_LANGUAGES.get(target_lang, target_lang))}:\n"
        f"{translated_text}"
    )
    
    await message.answer(response, parse_mode=ParseMode.HTML)

# Основная функция запуска бота
async def main():
    # Загружаем настройки при запуске
    load_user_preferences()
    
    # Инициализация бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрируем роутер
    dp.include_router(router)
    
    # Запускаем бота
    await dp.start_polling(bot, skip_updates=True)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())