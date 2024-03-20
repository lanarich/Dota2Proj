import pandas as pd
import numpy as np
import joblib
import requests
import json

columns_for_drop = ['_id', 'dire_POSITION_2_id', 'radiant_POSITION_4_id', 'radiant_POSITION_1_id',
                    'radiant_POSITION_2_position', 'startDateTime', 'radiant_POSITION_2_id', 'radiant_POSITION_5_id',
                    'dire_POSITION_2_position', 'radiant_POSITION_3_position', 'dire_POSITION_5_id',
                    'dire_POSITION_4_position', 'radiant_POSITION_5_position', 'dire_POSITION_1_id',
                    'durationSeconds', 'radiant_POSITION_4_position', 'dire_POSITION_4_id',
                    'dire_POSITION_1_position', 'radiant_POSITION_1_position', 'radiant_POSITION_3_id',
                    'dire_POSITION_3_id', 'id', 'dire_POSITION_3_position', 'gameMode', 'dire_POSITION_5_position',
                    ]

columns_with_leaver_status = ['dire_POSITION_4_leaverStatus', 'radiant_POSITION_3_leaverStatus',
                              'radiant_POSITION_2_leaverStatus', 'dire_POSITION_5_leaverStatus',
                              'dire_POSITION_3_leaverStatus', 'dire_POSITION_2_leaverStatus',
                              'dire_POSITION_1_leaverStatus', 'radiant_POSITION_4_leaverStatus',
                              'radiant_POSITION_5_leaverStatus', 'radiant_POSITION_1_leaverStatus']

columns_true_false_convert = ['dire_POSITION_5_isRadiant', 'dire_POSITION_4_intentionalFeeding',
                              'radiant_POSITION_5_isRadiant', 'dire_POSITION_5_intentionalFeeding',
                              'dire_POSITION_1_isRadiant', 'radiant_POSITION_3_intentionalFeeding',
                              'dire_POSITION_3_intentionalFeeding', 'radiant_POSITION_1_isRadiant',
                              'radiant_POSITION_4_isRadiant', 'radiant_POSITION_2_isRadiant',
                              'dire_POSITION_4_isRadiant', 'dire_POSITION_3_isRadiant',
                              'radiant_POSITION_3_isRadiant', 'radiant_POSITION_1_intentionalFeeding',
                              'radiant_POSITION_4_intentionalFeeding', 'radiant_POSITION_2_intentionalFeeding',
                              'dire_POSITION_2_isRadiant', 'dire_POSITION_1_intentionalFeeding',
                              'dire_POSITION_2_intentionalFeeding', 'radiant_POSITION_5_intentionalFeeding']

leaver_status_map = {'NONE': 0, 'DISCONNECTED': 1, 'AFK': 2, 'DISCONNECTED_TOO_LONG': 3, 'ABANDONED': 4}


def dataframe_preprocessing(dataframe, predict_items=False):
    if not predict_items:
        dataframe = dataframe.drop(columns_for_drop, axis=1)
        dataframe = dataframe['didRadiantWin'].astype(int)
        dataframe = dataframe['didRadiantWin'].astype(int)
    dataframe[columns_true_false_convert] = dataframe[columns_true_false_convert].astype(int)
    dataframe = dataframe.fillna(9999)
    dataframe[columns_with_leaver_status] = (dataframe[columns_with_leaver_status] != 'NONE').astype(int)
    return dataframe

def predict_csv_file(file_name):
    best_model = joblib.load('random_forest_calibrated.h5')
    model_features = best_model.feature_names_in_
    pred_df = pd.read_csv(file_name)
    pred_df = pred_df[model_features]
    converted_df = dataframe_preprocessing(pred_df, True)
    pred = best_model.predict_proba(converted_df)[:, 1]
    return pred



def get_info_stratz(match_id):
    url = 'https://api.stratz.com/graphql'
    api_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiMzVlZDA4NjYtNGVhOS00MDZhLTk0YWItNmFkMjQwMjgwZWNjIiwiU3RlYW1JZCI6IjE2NzM1MTc0MiIsIm5iZiI6MTY5NzcyNjAwOSwiZXhwIjoxNzI5MjYyMDA5LCJpYXQiOjE2OTc3MjYwMDksImlzcyI6Imh0dHBzOi8vYXBpLnN0cmF0ei5jb20ifQ.1y16eybJDLasnZBFT75d0q9QDdNsPwsV1v_8vaC-oyo'
    headers = {"Authorization": f"Bearer {api_token}"}
    graphql_query = f"""
    {{
        match(id: {match_id}){{
            id
            didRadiantWin
            firstBloodTime
            gameMode
            regionId
            gameVersionId
            radiantKills
            direKills
            radiantNetworthLeads
            radiantExperienceLeads
        }}     
    }}
    """
    data = {'query': graphql_query}
    response = requests.post(url, json=data, headers=headers)
    data_dict = json.loads(response.content)['data']['match']
    data_dict['radiantKills'] = np.sum(data_dict['radiantKills'])
    data_dict['direKills'] = np.sum(data_dict['direKills'])
    data_dict['radiantNetworthLeads'] = data_dict['radiantNetworthLeads'][-1]
    data_dict['radiantExperienceLeads'] = data_dict['radiantExperienceLeads'][-1]
    return pd.DataFrame([data_dict])

