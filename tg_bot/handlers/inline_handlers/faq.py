from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from tg_bot.service.api_requests import get_all_questions, get_answer_by_question_id
from tg_bot.handlers.inline_handlers.main_menu import get_user_keyboard
from tg_bot.configs.bot_messages import FAQ_EMPTY, FAQ_SELECT, FAQ_ANSWER_NOT_FOUND

faq_router = Router()


@faq_router.callback_query(F.data == "faq")
async def faq_handler(callback: CallbackQuery):
    """
    Обработчик нажатия на кнопку FAQ.
    Отправляет список вопросов.
    """
    questions = await get_all_questions()
    if not questions:
        await callback.message.answer(FAQ_EMPTY)
        await callback.answer()  # Завершаем коллбэк
        return

    # Создаем клавиатуру с вопросами
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Программа обучения в RENDERIA", callback_data="study_programms")

    for question in questions:
        keyboard.button(text=question["question"], callback_data=f"faq_question_{question['id']}")
    keyboard.button(text="<< Главное меню", callback_data="inline_main_menu")
    keyboard.adjust(1)

    await callback.message.edit_text(FAQ_SELECT, reply_markup=keyboard.as_markup())
    await callback.answer()  # Завершаем коллбэк


@faq_router.callback_query(F.data.startswith("faq_question_"))
async def handle_faq_question(callback: CallbackQuery):
    """
    Обработчик выбора вопроса.
    Отправляет ответ на выбранный вопрос.
    """
    question_id = callback.data.split("_")[-1]
    answer_data = await get_answer_by_question_id(question_id)
    if not answer_data:
        await callback.message.answer(FAQ_ANSWER_NOT_FOUND)
        return

    # Создаем клавиатуру с кнопкой "Назад"
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="<< Назад", callback_data="faq")
    keyboard.adjust(1)

    await callback.message.edit_text(
        f"<b>Вопрос:</b> {answer_data['question']}\n\n<b>Ответ:</b> {answer_data['answer']}",
        reply_markup=keyboard.as_markup(),
    )
    await callback.answer()


@faq_router.callback_query(F.data == "study_programms")
async def study_programms_handler(callback: CallbackQuery):
    try:
        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="faq")]])

        # Отправляем сообщение с описанием
        await callback.message.edit_text("Программа обучения в RENDERIA", reply_markup=keyboard)

        # Получаем список файлов и отправляем их
        study_programs_path = "tg_bot/files/study_programs"
        for file_name in os.listdir(study_programs_path):
            file_path = os.path.join(study_programs_path, file_name)
            if os.path.isfile(file_path):
                await callback.message.answer_document(types.FSInputFile(file_path), caption=file_name.replace("_", " ").replace(".pdf", ""))

        await callback.answer("Все файлы отправлены")
    except Exception as e:
        await callback.message.answer("Произошла ошибка при отправке файлов")
        await callback.answer()
