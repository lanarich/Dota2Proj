from aiogram.utils.keyboard import ReplyKeyboardBuilder

def predict_item_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text='🔮 Предсказания для игры 🔮')
    kb.button(text='🥠 Предсказать персонажа M1 🥠')
    kb.button(text='📝 Статистика 📝')
    kb.button(text='📌 Оценить бота 📌')
    kb.button(text='📈 Статистика оценок 📈')
    
    kb.adjust(3,2)
    return kb.as_markup(input_field_placeholder='Нажмите на одну из кнопок ниже', resize_keyboard=True, one_time_keyboard=True)
