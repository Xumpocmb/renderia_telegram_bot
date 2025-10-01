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
        # Создаем клавиатуру с выбором возрастных групп
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Младшая группа 6-8 лет", callback_data="study_programm_junior")
        keyboard.button(text="Средняя группа 9-11 лет", callback_data="study_programm_middle")
        keyboard.button(text="Старшая группа 12-14 лет", callback_data="study_programm_senior")
        keyboard.button(text="🔙 Назад", callback_data="faq")
        keyboard.adjust(1)  # Размещаем кнопки в один столбец

        # Отправляем сообщение с выбором возрастной группы
        await callback.message.edit_text(
            "Программа обучения в RENDERIA\n\nВыберите возрастную группу:",
            reply_markup=keyboard.as_markup()
        )
    except Exception as e:
        await callback.message.answer("Произошла ошибка при отображении меню")
    finally:
        await callback.answer()


@faq_router.callback_query(F.data == "study_programm_junior")
async def study_programm_junior_handler(callback: CallbackQuery):
    try:
        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="🔙 Назад", callback_data="study_programms")
        keyboard.adjust(1)

        # Отправляем сообщение с описанием
        await callback.message.answer("Программа обучения в RENDERIA - Младшая группа\nФайл отправляется..")

        # Отправляем файл для младшей группы
        file_path = "tg_bot/files/study_programs/junior_RENDERIA.pdf"
        if os.path.isfile(file_path):
            await callback.message.answer_document(
                types.FSInputFile(file_path), 
                caption="Программа обучения - Младшая группа",
                reply_markup=keyboard.as_markup()
            )
        else:
            await callback.message.answer("Файл программы обучения не найден", reply_markup=keyboard.as_markup())
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка при отправке файла: {str(e)}")
    finally:
        await callback.answer()


@faq_router.callback_query(F.data == "study_programm_middle")
async def study_programm_middle_handler(callback: CallbackQuery):
    try:
        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="🔙 Назад", callback_data="study_programms")
        keyboard.adjust(1)

        # Отправляем сообщение с описанием
        await callback.message.answer("Программа обучения в RENDERIA - Средняя группа\nФайл отправляется..")

        # Отправляем файл для средней группы
        file_path = "tg_bot/files/study_programs/middle_RENDERIA.pdf"
        if os.path.isfile(file_path):
            await callback.message.answer_document(
                types.FSInputFile(file_path), 
                caption="Программа обучения - Средняя группа",
                reply_markup=keyboard.as_markup()
            )
        else:
            await callback.message.answer("Файл программы обучения не найден", reply_markup=keyboard.as_markup())
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка при отправке файла: {str(e)}")
    finally:
        await callback.answer()


@faq_router.callback_query(F.data == "study_programm_senior")
async def study_programm_senior_handler(callback: CallbackQuery):
    try:
        # Создаем клавиатуру с кнопкой "Назад"
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="🔙 Назад", callback_data="study_programms")
        keyboard.adjust(1)

        # Отправляем сообщение с описанием
        await callback.message.answer("Программа обучения в RENDERIA - Старшая группа\nФайл отправляется..")

        # Отправляем файл для старшей группы
        file_path = "tg_bot/files/study_programs/senior_RENDERIA.pdf"
        if os.path.isfile(file_path):
            await callback.message.answer_document(
                types.FSInputFile(file_path), 
                caption="Программа обучения - Старшая группа",
                reply_markup=keyboard.as_markup()
            )
        else:
            await callback.message.answer("Файл программы обучения не найден", reply_markup=keyboard.as_markup())
    except Exception as e:
        await callback.message.answer("Произошла ошибка при отправке файла")
    finally:
        await callback.answer()
