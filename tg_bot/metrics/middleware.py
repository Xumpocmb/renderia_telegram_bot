from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, Update

from tg_bot.metrics.metrics_counter import metrics_counter


class MetricsMiddleware(BaseMiddleware):
    """
    Middleware for counting bot usage metrics.
    Counts the number of calls for each command or callback.
    """
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """
        Process update and count metrics.
        
        :param handler: Handler function
        :param event: Update event
        :param data: Additional data
        :return: Result of the handler
        """
        # Process the update first to avoid affecting user experience
        result = await handler(event, data)
        
        # Count metrics after processing
        if event.callback_query:
            await self._process_callback_query(event.callback_query)
        elif event.message:
            await self._process_message(event.message)
            
        return result
    
    async def _process_callback_query(self, callback_query: CallbackQuery) -> None:
        """
        Process callback query and increment metrics counter.
        
        :param callback_query: Callback query to process
        """
        if callback_query.data:
            # Use callback data as metric name
            metrics_counter.increment(callback_query.data)
    
    async def _process_message(self, message: Message) -> None:
        """
        Process message and increment metrics counter.
        
        :param message: Message to process
        """
        if message.text and message.text.startswith('/'):
            # Use command as metric name (without parameters)
            command = message.text.split()[0]
            metrics_counter.increment(command)