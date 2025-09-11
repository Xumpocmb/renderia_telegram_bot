from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.handlers.inline_handlers.main_menu import get_user_keyboard
from tg_bot.service.api_requests import get_erip_payment_help, get_payment_data_from_api
from tg_bot.configs.logger_config import get_logger
from tg_bot.configs.bot_messages import ERIP_INSTRUCTION_UNAVAILABLE, ERIP_INSTRUCTION_TEMPLATE, ERIP_ERROR

logger = get_logger()
erip_router = Router()


@erip_router.callback_query(F.data == "erip_info")
async def process_button_erip_press(callback: CallbackQuery):
    """
    Обработчик нажатия на кнопку "Инструкция по оплате".
    """
    help_data = await get_erip_payment_help()
    if not help_data:
        await callback.message.answer(ERIP_INSTRUCTION_UNAVAILABLE)
        await callback.answer()
        return

    erip_link = help_data.get("erip_link", "")
    erip_instructions = help_data.get("erip_instructions", "")

    formatted_text = ERIP_INSTRUCTION_TEMPLATE.format(
        erip_instructions=erip_instructions,
        erip_link=erip_link
    )
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="<< Главное меню", callback_data="inline_main_menu")
    keyboard.adjust(1)

    try:
        await callback.message.answer(formatted_text, reply_markup=keyboard.as_markup())
        logger.info(f"Отправлено сообщение пользователю {callback.from_user.id} с инструкцией по оплате через ЕРИП.")
    except Exception as e:
        logger.error(f"Ошибка при отправке инструкции: {e}")
        await callback.message.answer(ERIP_ERROR)

    finally:
        await callback.answer()



@erip_router.callback_query(F.data == "erip_payment")
async def process_button_erip_payment(callback: CallbackQuery):
    """
    Обработчик нажатия на кнопку "Оплатить через ЕРИП".
    """
    telegram_id = callback.from_user.id
    await callback.message.answer("⌛️ Сейчас всё подготовлю, ожидайте! ")

    payment_data = await get_payment_data_from_api(telegram_id)
    if not payment_data:
        await callback.message.answer("❌ Упс.. Мне не удалось получить данные для оплаты.")
        return

    for data in payment_data:
        await callback.message.answer(data)

    await callback.answer()
