import unittest
from unittest.mock import patch, AsyncMock, Mock
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.context import FSMContext


class TestBot(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = Mock()
        self.dp = Dispatcher(bot=self.bot)

    @patch('handlers.start.get_started')
    async def test_start_command(self, get_started_mock):
        message = types.Message(
            message_id=1, date=1, chat=types.Chat(
                id=1, type='private'), text='/start')
        get_started_mock.return_value = AsyncMock()
        await get_started_mock(message, self.bot)
        get_started_mock.assert_called_once()

    @patch('handlers.start.get_help')
    async def test_help_command(self, get_help_mock):
        message = types.Message(
            message_id=1, date=1, chat=types.Chat(
                id=1, type='private'), text='/help')
        get_help_mock.return_value = AsyncMock()
        await get_help_mock(message, self.bot)
        get_help_mock.assert_called_once()

    @patch('handlers.predict_items.start_predict_items')
    async def test_predict_items_command(self, start_predict_items_mock):
        message = types.Message(message_id=1,
                                date=1,
                                chat=types.Chat(id=1,
                                                type='private'),
                                text='🔮 Предсказания для игры 🔮')
        start_predict_items_mock.return_value = AsyncMock()
        await start_predict_items_mock(message,
                                       FSMContext(storage=None,
                                                  key='test_key'))
        start_predict_items_mock.assert_called_once()

    @patch('handlers.user_mark.get_inline')
    async def test_user_mark_command(self, get_inline_mock):
        message = types.Message(
            message_id=1, date=1, chat=types.Chat(
                id=1, type='private'), text='📌 Оценить бота 📌')
        get_inline_mock.return_value = AsyncMock()
        await get_inline_mock(message, FSMContext(storage=None,
                                                  key='test_key'))
        get_inline_mock.assert_called_once()

    @patch('handlers.statistics.statistic')
    async def test_statistics_command(self, statistic_mock):
        message = types.Message(
            message_id=1, date=1, chat=types.Chat(
                id=1, type='private'), text='📊 Статистика бота 📊')
        statistic_mock.return_value = AsyncMock()
        await statistic_mock(message, FSMContext(storage=None, key='test_key'))
        statistic_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
