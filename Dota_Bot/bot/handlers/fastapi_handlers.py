from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot
from aiogram.enums.parse_mode import ParseMode
from keyboards.stats_kb import stats_kb
from keyboards.predict_item_kb import predict_item_keyboard

router_stats = Router()

@router_stats.message(F.text == "◀️ Назад ◀️")
async def previews_kb(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id ,"Выберите опцию:", reply_markup=predict_item_keyboard())

@router_stats.message(F.text == "📝 Статистика 📝")
async def next_kb(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id ,"Выберите опцию:", reply_markup=stats_kb())
    























# @app.get('/get_match_info/{match_id}')
# async def get_info(match_id: int, background_tasks: BackgroundTasks):
#     start = datetime.datetime.now()
#     print(
#         start,
#         "| info | начало | endpoint: {get_match_info} |\
#             информация о матче | match_id : " +
#         str(match_id))
#     try:
#         match_data = await stratz_match_request_wout_db(match_id)
#         if match_data is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Match data not found or not parsed by Stratz yet")

#         filename = f'{match_id}.json'

#         with open(filename, 'w') as file:
#             json.dump(match_data, file)

#         background_tasks.add_task(os.remove, filename)

#         # Возвращаем файл
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| info | конец | endpoint: {get_match_info} |\
#                 информация о матче | match_id : " +
#             str(match_id))

#         return FileResponse(
#             path=filename,
#             filename=filename,
#             media_type='application/json')
#     except Exception as e:
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| error | конец | endpoint: {get_match_info} | информация о\
#                 матче | match_id : " +
#             str(match_id) +
#             str(e))
#         raise HTTPException(status_code=404,
#                             detail="Troubles with getting match info")


# @app.get('/get_match_dataframe/{match_id}')
# def get_info_df(match_id):
#     start = datetime.datetime.now()
#     print(
#         start,
#         "| info | начало | endpoint: {get_match_dataframe}\
#             | датафрейм по матчу\
#             | match_id : " +
#         str(match_id))
#     try:
#         converted_match = get_decomposed_match_data_wout_db(match_id)
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| info | конец | endpoint: {get_match_dataframe} |\
#                 датафрейм по матчу | match_id : " +
#             str(match_id))

#         return HTMLResponse(content=converted_match.to_html())
#     except Exception as e:
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| error | конец | endpoint: {get_match_dataframe} |\
#                 датафрейм по матчу | match_id : " +
#             str(match_id) +
#             str(e))
#         raise HTTPException(
#             status_code=404,
#             detail="Troubles with converting data to dataframe")


# @app.get('/gold_graph/{match_id}')
# def get_gold_graph(match_id):  # тут он должен принимать уже датафрейм
#     start = datetime.datetime.now()
#     print(
#         start,
#         "| info | начало | endpoint: {gold_graph} |\
#             график золота по матчу | match_id : " +
#         str(match_id))
#     try:
#         game = get_decomposed_match_data_wout_db(match_id)
#         game = game.sort_values('currentMinute').reset_index(drop=True)
#         plt.figure(figsize=(10, 5))
#         plt.xlabel("Минута")
#         plt.ylabel("Золото")
#         plt.axhline(color='gray', alpha=0.05)
#         plt.ylim(-30000, 30000)
#         plt.text(3, 28000, 'СВЕТ', fontsize=12, ha='left', va='top')
#         plt.text(3, -28000, 'ТЬМА', fontsize=12, ha='left', va='bottom')
#         plt.plot(
#             game['currentMinute'],
#             game['minuteRadiantNetworthLead'],
#             color='gold')

#         buf = BytesIO()
#         plt.savefig(buf, format='png')
#         plt.close()
#         buf.seek(0)

#         end = datetime.datetime.now()
#         print(
#             end,
#             "| info | конец | endpoint: {gold_graph} |\
#                 график золота по матчу | match_id : " +
#             str(match_id))

#         return StreamingResponse(buf, media_type="image/png")
#     except Exception as e:
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| error | конец | endpoint: {gold_graph} |\
#                 график золота по матчу | match_id : " +
#             str(match_id) +
#             str(e))
#         raise HTTPException(status_code=404,
#                             detail="Troubles with getting match info")


# @app.get('/exp_graph/{match_id}')
# def get_exp_graph(match_id):  # тут он должен принимать уже датафрейм
#     start = datetime.datetime.now()
#     print(
#         start,
#         "| info | начало | endpoint: {exp_graph} | график опыта по матчу |\
#             match_id : " +
#         str(match_id))
#     try:
#         game = get_decomposed_match_data_wout_db(match_id)
#         game = game.sort_values('currentMinute').reset_index(drop=True)
#         plt.figure(figsize=(10, 5))
#         plt.xlabel("Минута")
#         plt.ylabel("Опыт")
#         plt.axhline(color='gray', alpha=0.05)
#         plt.ylim(-30000, 30000)
#         plt.text(3, 28000, 'СВЕТ', fontsize=12, ha='left', va='top')
#         plt.text(3, -28000, 'ТЬМА', fontsize=12, ha='left', va='bottom')
#         plt.plot(
#             game['currentMinute'],
#             game['minuteRadiantExperienceLeads'],
#             color='lightblue')

#         buf = BytesIO()
#         plt.savefig(buf, format='png')
#         plt.close()
#         buf.seek(0)
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| info | конец | endpoint: {exp_graph} | график опыта по матчу |\
#                 match_id : " +
#             str(match_id))
#         return StreamingResponse(buf, media_type="image/png")
#     except Exception as e:
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| error | конец | endpoint: {exp_graph} | график опыта по матчу |\
#                 match_id : " +
#             str(match_id) +
#             str(e))
#         raise HTTPException(status_code=404,
#                             detail="Troubles with getting match info")


# @app.get('/heroes_stats_in_match/{match_id}')
# def get_heroes_stats(match_id):
#     '''
#     Метод возвращает статисттику игроков в конкретном
#     матче.

#     В эндпоинт следует передать айди матча, например 5721798888
#     '''
#     start = datetime.datetime.now()
#     print(
#         start,
#         "| info | начало | endpoint: {heroes_stats_in_match} |\
#             статистика по герою в матче | match_id : " +
#         str(match_id))
#     try:
#         local_stratz_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ\
#             TdWJqZWN0IjoiZDVlZWFiMWUtMDlmNS00OTc2LWJiOGEtZmY2NjhlOGU5MD\
#                 YyIiwiU3RlYW1JZCI6IjM0MTI3NDA0MCIsIm5iZiI6MTY5Nzk2NTIxM\
#                     iwiZXhwIjoxNzI5NTAxMjEyLCJpYXQiOjE2OTc5NjUyMTIsImlzc\
#                         yI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.NBpwwl-RBlH\
#                             LvPr3o1UuzFbI5NZFU7zJWSKKk_1wxvM"

#         url = 'https://api.stratz.com/graphql'

#         headers = {"Authorization": f"Bearer {local_stratz_token}"}
#         match_id = int(match_id)

#         query2 = '''
#         {

#           match(id:%d){
#             players{
#               hero{shortName}
#               networth
#               kills
#               deaths
#               assists
#               numLastHits
#               numDenies

#             }
#           }
#         }

#         ''' % (match_id)

#         data = {'query': query2}
#         response = requests.post(url, json=data, headers=headers)
#         d = response.json()['data']['match']['players']
#         df = pd.DataFrame(d)
#         df.hero = df.hero.apply(lambda x: x['shortName'])

#         plt.figure(figsize=(8, 6))
#         ax = plt.gca()
#         ax.axis('off')
#         plt.table(
#             cellText=df.values,
#             colLabels=df.columns,
#             cellLoc='center',
#             loc='center',
#             colLoc='center')
#         plt.show()

#         buf = BytesIO()
#         plt.savefig(buf, format='png')
#         plt.close()
#         buf.seek(0)
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| info | конец | endpoint: {heroes_stats_in_match}\
#                 | график опыта по матчу | match_id : " +
#             str(match_id))
#     except Exception as e:
#         end = datetime.datetime.now()
#         print(
#             end,
#             "| error | конец | endpoint: {heroes_stats_in_match} |\
#                 статистика по герою в матче | "
#             "match_id : " +
#             str(match_id) +
#             str(e))
#         raise HTTPException(status_code=404,
#                             detail="Troubles with getting match info")
#     else:
#         return StreamingResponse(buf, media_type="image/png")


# @app.get('/heroes_stats/{hero}')
# def get_heroes_winrate(hero: str):
#     '''
#     Метод возвращает винрейт героя в текущем патче.

#     Необходимо ввести имя героя.
#     Например mars, axe, anti_mage
#     '''
#     start = datetime.datetime.now()
#     print(
#         start,
#         "| info | начало | endpoint: {heroes_stats} |\
#             статистика по герою в матче | hero_name : " +
#         str(hero))
#     local_stratz_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTd\
#         WJqZWN0IjoiZDVlZWFiMWUtMDlmNS00OTc2LWJiOGEtZmY2NjhlOGU5MDYyIi\
#             wiU3RlYW1JZCI6IjM0MTI3NDA0MCIsIm5iZiI6MTY5Nzk2NTIxMiwiZXhw\
#                 IjoxNzI5NTAxMjEyLCJpYXQiOjE2OTc5NjUyMTIsImlzcyI6Imh0dHB\
#                     zOi8vYXBpLnN0cmF0ei5jb20ifQ.NBpwwl-RBlHLvPr3o1UuzFbI\
#                         5NZFU7zJWSKKk_1wxvM"

#     url = 'https://api.stratz.com/graphql'

#     headers = {"Authorization": f"Bearer {local_stratz_token}"}

#     query1 = '''
#                     {
#                     constants{
#                         heroes{
#                         id
#                         shortName
#                         }
#                     }
#                     }


#                     '''

#     query2 = '''
#                     {
#                     heroStats{
#                         winGameVersion (gameModeIds:ALL_PICK_RANKED){
#                         heroId
#                         winCount
#                         matchCount
#                         gameVersionId
#                         }
#                     }
#                     }


#                     '''
#     data1 = {'query': query1}
#     response1 = requests.post(url, json=data1, headers=headers)
#     d = response1.json()['data']['constants']['heroes']
#     names = pd.DataFrame(d)

#     data2 = {'query': query2}
#     response2 = requests.post(url, json=data2, headers=headers)
#     d1 = response2.json()['data']['heroStats']['winGameVersion']
#     a = pd.DataFrame(d1)
#     a = a[a.gameVersionId == 170]
#     a['winRate'] = round(a.winCount / a.matchCount, 2)

#     a = a.merge(names, how='inner', left_on='heroId', right_on='id')
#     a = a[['shortName', 'matchCount', 'winCount', 'winRate']]
#     df = a[a.shortName == hero]

#     plt.figure(figsize=(8, 6))
#     ax = plt.gca()
#     ax.axis('off')
#     plt.table(
#         cellText=df.values,
#         colLabels=df.columns,
#         cellLoc='center',
#         loc='center',
#         colLoc='center')
#     plt.show()

#     buf = BytesIO()
#     plt.savefig(buf, format='png')
#     plt.close()
#     buf.seek(0)
#     end = datetime.datetime.now()
#     print(
#         end,
#         "| info | конец | endpoint: {heroes_stats} |\
#             статистика по герою | hero_name : " +
#         hero)
#     return StreamingResponse(buf, media_type="image/png")
