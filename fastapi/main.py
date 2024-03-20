from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
from prediction.model import predict_csv_file, get_info_stratz
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
from io import BytesIO

app = FastAPI()



@app.get("/")
def root():
    return {"message": "Hello, User!"}



@app.get('/predict_winer')
def predict_winer(): #тут он должен принимать уже датафрейм
    game = pd.read_csv('for_prediction.csv')
    pred = predict_csv_file('for_prediction.csv')
    pred_df = pd.DataFrame({'Внутригровая минута': game['currentMinute'], 'Вероятность победы света': pred})
    html_content = pred_df.sort_values(by=['Внутригровая минута']).reset_index(drop = True).to_html()
    return HTMLResponse(content=html_content)


@app.get('/get_info')
def get_info(match_id):
    data = get_info_stratz(match_id)
    return HTMLResponse(content=data.to_html())
    



@app.get('/gold_graph')
def get_gold_graph(): #тут он должен принимать уже датафрейм
    game = pd.read_csv('for_prediction.csv')
    game = game.sort_values('currentMinute').reset_index(drop=True)
    plt.figure(figsize=(10, 5))
    plt.xlabel("Минута")
    plt.ylabel("Золото")
    plt.axhline(color='gray', alpha=0.05)
    plt.ylim(-30000, 30000)
    plt.text(3, 28000, 'СВЕТ', fontsize=12, ha='left', va='top')
    plt.text(3, -28000, 'ТЬМА', fontsize=12, ha='left', va='bottom')
    plt.plot( game['currentMinute'], game['minuteRadiantNetworthLead'], color='gold')
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
    



@app.get('/exp_graph')
def get_exp_graph(): #тут он должен принимать уже датафрейм
    game = pd.read_csv('for_prediction.csv')
    game = game.sort_values('currentMinute').reset_index(drop=True)
    plt.figure(figsize=(10, 5))
    plt.xlabel("Минута")
    plt.ylabel("Опыт")
    plt.axhline(color='gray', alpha=0.05)
    plt.ylim(-30000, 30000)
    plt.text(3, 28000, 'СВЕТ', fontsize=12, ha='left', va='top')
    plt.text(3, -28000, 'ТЬМА', fontsize=12, ha='left', va='bottom')
    plt.plot( game['currentMinute'], game['minuteRadiantExperienceLeads'], color='lightblue')
    
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







