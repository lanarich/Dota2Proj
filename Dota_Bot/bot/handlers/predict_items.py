from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from state.prediction import PredictionState
import joblib
import pandas as pd
from keyboards.predict_item_kb import predict_item_keyboard


def load_model():
    with open('random_forest.h5', 'rb') as file:
        model = joblib.load(file)
    return model


columns_for_drop = [
    '_id',
    'dire_POSITION_2_id',
    'radiant_POSITION_4_id',
    'radiant_POSITION_1_id',
    'radiant_POSITION_2_position',
    'startDateTime',
    'radiant_POSITION_2_id',
    'radiant_POSITION_5_id',
    'dire_POSITION_2_position',
    'radiant_POSITION_3_position',
    'dire_POSITION_5_id',
    'dire_POSITION_4_position',
    'radiant_POSITION_5_position',
    'dire_POSITION_1_id',
    'durationSeconds',
    'radiant_POSITION_4_position',
    'dire_POSITION_4_id',
    'dire_POSITION_1_position',
    'radiant_POSITION_1_position',
    'radiant_POSITION_3_id',
    'dire_POSITION_3_id',
    'id',
    'dire_POSITION_3_position',
    'gameMode',
    'dire_POSITION_5_position',
]

columns_with_leaver_status = [
    'dire_POSITION_4_leaverStatus', 'radiant_POSITION_3_leaverStatus',
    'radiant_POSITION_2_leaverStatus', 'dire_POSITION_5_leaverStatus',
    'dire_POSITION_3_leaverStatus', 'dire_POSITION_2_leaverStatus',
    'dire_POSITION_1_leaverStatus', 'radiant_POSITION_4_leaverStatus',
    'radiant_POSITION_5_leaverStatus', 'radiant_POSITION_1_leaverStatus'
]

columns_true_false_convert = [
    'dire_POSITION_5_isRadiant',
    'dire_POSITION_4_intentionalFeeding',
    'radiant_POSITION_5_isRadiant',
    'dire_POSITION_5_intentionalFeeding',
    'dire_POSITION_1_isRadiant',
    'radiant_POSITION_3_intentionalFeeding',
    'dire_POSITION_3_intentionalFeeding',
    'radiant_POSITION_1_isRadiant',
    'radiant_POSITION_4_isRadiant',
    'radiant_POSITION_2_isRadiant',
    'dire_POSITION_4_isRadiant',
    'dire_POSITION_3_isRadiant',
    'radiant_POSITION_3_isRadiant',
    'radiant_POSITION_1_intentionalFeeding',
    'radiant_POSITION_4_intentionalFeeding',
    'radiant_POSITION_2_intentionalFeeding',
    'dire_POSITION_2_isRadiant',
    'dire_POSITION_1_intentionalFeeding',
    'dire_POSITION_2_intentionalFeeding',
    'radiant_POSITION_5_intentionalFeeding']

leaver_status_map = {
    'NONE': 0,
    'DISCONNECTED': 1,
    'AFK': 2,
    'DISCONNECTED_TOO_LONG': 3,
    'ABANDONED': 4}


def dataframe_preprocessing(dataframe, predict_items_bool=False):
    if not predict_items_bool:
        dataframe = dataframe.drop(columns_for_drop, axis=1)
        dataframe['didRadiantWin'] = dataframe['didRadiantWin']\
            .astype(int)
    dataframe[columns_true_false_convert] =\
        dataframe[columns_true_false_convert].astype(
        int)
    dataframe = dataframe.fillna(9999)
    dataframe[columns_with_leaver_status] = (
        dataframe[columns_with_leaver_status] != 'NONE').astype(int)
    return dataframe


def predict_csv_file(file_name):
    best_model = joblib.load('random_forest.h5')
    model_features = best_model.feature_names_in_
    pred_df = pd.read_csv(file_name)
    pred_df = pred_df[model_features]
    converted_df = dataframe_preprocessing(pred_df, True)
    pred = best_model.predict_proba(converted_df)[:, 1]
    return pred


router = Router()


@router.message(F.text == "🔮 Предсказания для игры 🔮")
async def start_predict_items(message: Message, state: FSMContext):
    await message.answer(
        'Давайте поминутно предскажем вероятность победы. \n'
        'Для этого загрузите файл формата <b>csv</b> весом не\
            более <b>20 МБ</b> \n'
    )
    await state.set_state(PredictionState.predItems)


@router.message(PredictionState.predItems)
async def predict_items(message: Message, bot, state: FSMContext):
    document = await bot.download(message.document)
    pred = predict_csv_file(document)
    text = (
        '🌟 Данные предсказаны! 🌟\n\n'
        f'Вероятность победы сил Света: {pred}\n'
    )
    await message.answer(text, reply_markup=predict_item_keyboard)
    await state.clear()
