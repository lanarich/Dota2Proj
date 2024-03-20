import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd

from converting.converter_script import get_decomposed_match_data
from api_requests.get_graphql_match import get_match_data
from prediction.model import predict_dataframe
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
from io import BytesIO

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, User!"}


@app.get('/predict_completed/{match_id}')
def predict_winner(match_id):  # тут он должен принимать уже датафрейм
    game = get_decomposed_match_data(match_id)
    pred = predict_dataframe('for_prediction.csv')
    pred_df = pd.DataFrame({'Внутригровая минута': game['currentMinute'], 'Вероятность победы света': pred})
    html_content = pred_df.sort_values(by=['Внутригровая минута']).reset_index(drop=True).to_html()
    return HTMLResponse(content=html_content)


@app.get('/get_match_info/{match_id}')
def get_info(match_id):
    single_match = asyncio.run(get_match_data(match_id))
    return single_match


@app.get('/get_match_dataframe/{match_id}')
def get_info(match_id):
    converted_match = get_decomposed_match_data(match_id)
    return HTMLResponse(content=converted_match.to_html())


@app.get('/gold_graph/{match_id}')
def get_gold_graph(match_id):  # тут он должен принимать уже датафрейм
    game = get_decomposed_match_data(match_id)
    game = game.sort_values('currentMinute').reset_index(drop=True)
    plt.figure(figsize=(10, 5))
    plt.xlabel("Минута")
    plt.ylabel("Золото")
    plt.axhline(color='gray', alpha=0.05)
    plt.ylim(-30000, 30000)
    plt.text(3, 28000, 'СВЕТ', fontsize=12, ha='left', va='top')
    plt.text(3, -28000, 'ТЬМА', fontsize=12, ha='left', va='bottom')
    plt.plot(game['currentMinute'], game['minuteRadiantNetworthLead'], color='gold')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.get('/exp_graph/{match_id}')
def get_exp_graph(match_id):  # тут он должен принимать уже датафрейм
    game = get_decomposed_match_data(match_id)
    game = game.sort_values('currentMinute').reset_index(drop=True)
    plt.figure(figsize=(10, 5))
    plt.xlabel("Минута")
    plt.ylabel("Опыт")
    plt.axhline(color='gray', alpha=0.05)
    plt.ylim(-30000, 30000)
    plt.text(3, 28000, 'СВЕТ', fontsize=12, ha='left', va='top')
    plt.text(3, -28000, 'ТЬМА', fontsize=12, ha='left', va='bottom')
    plt.plot(game['currentMinute'], game['minuteRadiantExperienceLeads'], color='lightblue')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.post('/heroes_stats_in_match')
def get_heroes_stats():
    pass


@app.post('/heroes_stats')
def get_heroes_stats_entire():
    pass
