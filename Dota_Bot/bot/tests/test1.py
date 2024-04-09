import unittest
from unittest.mock import patch, mock_open, MagicMock
from handlers.predict_items import load_model, dataframe_preprocessing, \
    predict_csv_file, columns_true_false_convert, columns_with_leaver_status
import pandas as pd
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline import place_kb
from utils.database import DataBase


class TestLoadModel(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open,
           read_data=b'random_forest_model_data')
    @patch('joblib.load')
    def test_load_model(self, joblib_load_mock, open_mock):
        model_mock = 'mocked_model'
        joblib_load_mock.return_value = model_mock

        model = load_model()

        open_mock.assert_called_once_with('random_forest.h5', 'rb')
        joblib_load_mock.assert_called_once_with(open_mock())
        self.assertEqual(model, model_mock)


class TestPlaceKb(unittest.TestCase):
    def test_place_kb(self):
        # Вызываем функцию
        keyboard_markup = place_kb()

        # Проверяем, что возвращаемый объект является экземпляром
        # InlineKeyboardMarkup
        self.assertIsInstance(keyboard_markup, InlineKeyboardMarkup)

        # Проверяем, что в клавиатуре  5 кнопок
        self.assertEqual(len(keyboard_markup.inline_keyboard), 5)

        # Проверяем, что кнопки имеют правильные тексты и данные обратного
        # вызова
        for i, button in enumerate(keyboard_markup.inline_keyboard[0]):
            self.assertIsInstance(button, InlineKeyboardButton)
            self.assertEqual(button.text, "🌟" * (i + 1))
            self.assertEqual(button.callback_data, f"set:{i +  1}")


class TestDataframePreprocessing(unittest.TestCase):

    def test_dataframe_preprocessing(self):
        # тестовый DataFrame
        test_data = 'for_prediction.csv'
        df = pd.read_csv(test_data)

        # Вызываем функцию dataframe_preprocessing
        processed_df = dataframe_preprocessing(df, predict_items_bool=True)

        # Проверки работы функции
        self.assertEqual(processed_df['didRadiantWin'].dtype, int)
        for column in columns_true_false_convert:
            self.assertEqual(processed_df[column].dtype, int)
        for column in columns_with_leaver_status:
            self.assertEqual(processed_df[column].dtype, int)


class TestPredictCsvFile(unittest.TestCase):

    @patch('joblib.load')
    @patch('handlers.predict_items.dataframe_preprocessing')
    @patch('pandas.read_csv')
    def test_predict_csv_file(
            self, mock_read_csv, mock_dataframe_preprocessing, mock_load):
        # Создаем фиктивные данные для теста
        file_name = 'test_data.csv'
        model_features = ['feature1', 'feature2']
        mock_model = MagicMock()
        mock_model.feature_names_in_ = model_features
        mock_load.return_value = mock_model

        # Вызываем функцию predict_csv_file
        predictions = predict_csv_file(file_name)

        # Проверки
        # Проверяем, что функция pd.read_csv была вызвана с правильным
        # аргументом
        mock_read_csv.assert_called_once_with(file_name)
        # Проверяем, что функция dataframe_preprocessing была вызвана
        mock_dataframe_preprocessing.assert_called_once()
        # Проверяем, что метод predict_proba был вызван у модели
        mock_model.predict_proba.assert_called_once()
        # Проверяем, что возвращаемое значение соответствует предсказаниям
        # модели
        self.assertEqual(
            predictions, mock_model.predict_proba.return_value[:, 1])


class TestDataBase(unittest.TestCase):

    def setUp(self):
        # Используем временную базу данных для тестов
        self.db = DataBase(':memory:')

    def test_create_db(self):
        # Проверяем, что таблица users создается успешно
        self.db.create_db()
        self.assertIn(('users',), self.db.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';").fetchall())

    def test_add_mark(self):
        # Проверяем добавление метки пользователя
        user_mark = 'A'
        telegram_id = '12345'
        self.db.add_mark(user_mark, telegram_id)
        result = self.db.cursor.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)).fetchone()
        self.assertEqual(result[1], user_mark)
        self.assertEqual(result[2], telegram_id)

    def test_select_marks(self):
        # Проверяем выборку всех меток пользователей
        marks = self.db.select_marks()
        # Предполагаем, что изначально нет меток
        self.assertEqual(len(marks), 0)
        self.db.add_mark('A', '12345')
        marks = self.db.select_marks()
        # Проверяем, что после добавления есть одна метка
        self.assertEqual(len(marks), 1)

    def test_select_user_id(self):
        # Проверяем выборку пользователя по telegram_id
        telegram_id = '12345'
        self.db.add_mark('A', telegram_id)
        user = self.db.select_user_id(telegram_id)
        self.assertIsNotNone(user)  # Проверяем, что пользователь найден
        # Проверяем, что telegram_id совпадает
        self.assertEqual(user[2], telegram_id)

    def tearDown(self):
        del self.db  # Закрываем соединение с базой данных


if __name__ == '__main__':
    unittest.main()
