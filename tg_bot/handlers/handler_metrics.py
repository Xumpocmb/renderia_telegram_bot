from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from tg_bot.filters.filter_admin import IsAdmin
from tg_bot.metrics.metrics_counter import metrics_counter

metrics_router = Router()


@metrics_router.message(Command("metrics"), IsAdmin())
async def show_metrics(message: Message):
    """
    Handler for showing metrics to admins.
    Shows the number of calls for each command or callback.
    Also sends a CSV file with metrics.
    
    :param message: Message object
    """
    metrics = metrics_counter.get_metrics()
    
    if not metrics:
        await message.answer("Метрики пока отсутствуют.")
        return
    
    # Sort metrics by number of calls (descending)
    sorted_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)
    
    # Format metrics as text
    metrics_text = "📊 <b>Метрики использования бота:</b>\n\n"
    for name, count in sorted_metrics:
        metrics_text += f"<code>{name}</code> - {count}\n"
    
    await message.answer(metrics_text)
    
    # Export metrics to XLSX and send the file
    xlsx_path = metrics_counter.export_to_xlsx()
    if xlsx_path:
        xlsx_file = FSInputFile(xlsx_path)
        await message.answer_document(
            document=xlsx_file,
            caption="📊 Отчет по метрикам использования бота в формате Excel"
        )


@metrics_router.message(Command("reset_metrics"), IsAdmin())
async def reset_metrics(message: Message):
    """
    Handler for resetting all metrics.
    Only available to admins.
    
    :param message: Message object
    """
    metrics_counter.reset_metrics()
    await message.answer("✅ Все метрики сброшены.")