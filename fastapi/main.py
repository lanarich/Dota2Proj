import asyncio
import json

import requests
from fastapi import FastAPI
import pandas as pd

from converting.converter_script import convert_match_data_into_df, create_dataframe
from api_requests.get_graphql_match import get_match_data, stratz_match_request_wout_db
from prediction.model import predict_dataframe
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import FileResponse

app = FastAPI(title='DOTA 2 APP')


@app.get("/")
def root():
    return {"message": "Hello, User!"}


def get_decomposed_match_data_wout_db(match_id):
    single_match = asyncio.run(stratz_match_request_wout_db(match_id))
    match_data = convert_match_data_into_df(single_match)
    return create_dataframe(match_data)


@app.get('/predict_completed/{match_id}')
def predict_winner(match_id):  # тут он должен принимать уже датафрейм
    game_df = get_decomposed_match_data_wout_db(match_id)
    pred = predict_dataframe(game_df)
    pred_df = pd.DataFrame({'Внутригровая минута': game_df['currentMinute'], 'Вероятность победы света': pred})
    html_content = pred_df.sort_values(by=['Внутригровая минута']).reset_index(drop=True).to_html()
    return HTMLResponse(content=html_content)


@app.get('/get_match_info/{match_id}')
def get_info(match_id):
    single_match = asyncio.run(stratz_match_request_wout_db(match_id))
    filename = str(match_id)+'.json'
    with open(filename, 'w') as fp:
        json.dump(single_match, fp)
        return FileResponse(filename)


@app.get('/get_match_dataframe/{match_id}')
def get_info(match_id):
    converted_match = get_decomposed_match_data_wout_db(match_id)
    return HTMLResponse(content=converted_match.to_html())


@app.get('/gold_graph/{match_id}')
def get_gold_graph(match_id):  # тут он должен принимать уже датафрейм
    game = get_decomposed_match_data_wout_db(match_id)
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
    game = get_decomposed_match_data_wout_db(match_id)
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


@app.post('/heroes_stats_in_match/{match_id}')
def get_heroes_stats(match_id):
    '''
    Метод возвращает статисттику игроков в конкретном 
    матче.

    В эндпоинт следует передать айди матча, например 5721798888 
    '''
    local_stratz_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiZDVlZWFiMWUtMDlmNS00OTc2LWJiOGEtZmY2NjhlOGU5MDYyIiwiU3RlYW1JZCI6IjM0MTI3NDA0MCIsIm5iZiI6MTY5Nzk2NTIxMiwiZXhwIjoxNzI5NTAxMjEyLCJpYXQiOjE2OTc5NjUyMTIsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.NBpwwl-RBlHLvPr3o1UuzFbI5NZFU7zJWSKKk_1wxvM"

    url = 'https://api.stratz.com/graphql'

    headers = {"Authorization": f"Bearer {local_stratz_token}"}
    match_id = int(match_id)
    
    query2 = ''' 
    {
    
      match(id:%d){
        players{
          hero{shortName}
          networth
          kills
          deaths
          assists
          numLastHits
          numDenies
          
        }
      }
    }

    ''' % (match_id)


    data = {'query':query2}
    response = requests.post(url, json=data, headers=headers)
    d = response.json()['data']['match']['players']
    df = pd.DataFrame(d)
    df.hero = df.hero.apply(lambda x: x['shortName'])
    


    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    ax.axis('off')
    plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colLoc='center')
    plt.show()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

@app.get('/heroes_stats/{hero}')
def get_heroes_winrate(hero:str):
    '''
    Метод возвращает винрейт героя в текущем патче.
    
    Необходимо ввести имя героя.
    Например mars, axe, anti_mage
    '''
    local_stratz_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiZDVlZWFiMWUtMDlmNS00OTc2LWJiOGEtZmY2NjhlOGU5MDYyIiwiU3RlYW1JZCI6IjM0MTI3NDA0MCIsIm5iZiI6MTY5Nzk2NTIxMiwiZXhwIjoxNzI5NTAxMjEyLCJpYXQiOjE2OTc5NjUyMTIsImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.NBpwwl-RBlHLvPr3o1UuzFbI5NZFU7zJWSKKk_1wxvM"

    url = 'https://api.stratz.com/graphql'

    headers = {"Authorization": f"Bearer {local_stratz_token}"}

    query1 = ''' 
                {
                constants{
                    heroes{
                    id
                    shortName
                    }
                }
                }


                '''

    query2 = ''' 
                {
                heroStats{
                    winGameVersion (gameModeIds:ALL_PICK_RANKED){
                    heroId
                    winCount
                    matchCount
                    gameVersionId
                    }
                }
                }


                '''
    data1 = {'query':query1}
    response1 = requests.post(url, json=data1, headers=headers)
    d = response1.json()['data']['constants']['heroes']
    names = pd.DataFrame(d)

    data2 = {'query':query2}
    response2 = requests.post(url, json=data2, headers=headers)
    d1 = response2.json()['data']['heroStats']['winGameVersion']
    a = pd.DataFrame(d1)
    a = a[a.gameVersionId==170]
    a['winRate'] = round(a.winCount / a.matchCount,2)

    a = a.merge(names, how='inner', left_on='heroId', right_on='id')
    a = a[['shortName', 'matchCount', 'winCount','winRate']]
    df = a[a.shortName==hero]



    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    ax.axis('off')
    plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colLoc='center')
    plt.show()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

if __name__ == '__main__':
    get_decomposed_match_data_wout_db(7648214204)
