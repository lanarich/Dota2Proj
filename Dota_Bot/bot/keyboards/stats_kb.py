from aiogram.utils.keyboard import ReplyKeyboardBuilder

def stats_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text='🔍 Информация о матче 🔍')
    kb.button(text='💰 График золота 💰')
    kb.button(text='📚 График опыта 📚')
    kb.button(text='📊 Статистика героев 📊')
    kb.button(text='🏆 Винрейт персонажа в патче 🏆')
    kb.button(text='◀️ Назад ◀️')
    
    kb.adjust(3,2,1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)