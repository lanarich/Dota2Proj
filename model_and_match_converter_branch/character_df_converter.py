import pandas as pd
import pymongo.errors
from pymongo import MongoClient


def create_mongo_connection():
    try:
        # Менять соединение с монгой
        client = MongoClient("localhost", 27017)
        db = client.dota_db
        return client, db
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(err)

mongo_client, mongo_db = create_mongo_connection()
match_ups = mongo_db.matchup_coll


def get_combined_data():
    cursor = match_ups.find({})
    df_list = []
    for doc in cursor:
        df_list.append(flatten_data(doc))
    df = pd.DataFrame(df_list)
    columns_to_remove = [col for col in df.columns if 'week' in col or 'stats_heroId' in col
                         or 'stats_time' in col or 'bans_heroId' in col or 'wins_heroId' in col
                         or 'attributes_id' in col or 'winRateHeroId2' in col]

    remove_columns = ['attributes_role_4_roleId', 'attributes_role_4_level',
                      'attributes_role_5_roleId', 'attributes_role_5_level']
    df.drop(columns=columns_to_remove, inplace=True)
    df.drop(columns=remove_columns, inplace=True)
    for col in df.columns:
        if df[col].dtype != 'object':  # Проверка, что тип столбца не str (object)
            median_value = df[col].median()
            df[col].fillna(median_value, inplace=True)
    df.to_csv('character_stats.csv')


def flatten_data(record):
    flat_record = {}

    # Process root level fields
    flat_record['_id'] = record['_id']

    # Process 'stats' fields
    for key, value in record.get('stats', {}).items():
        flat_record[f'stats_{key}'] = value

    # Process 'bans' fields
    for key, value in record.get('bans', {}).items():
        flat_record[f'bans_{key}'] = value

    # Process 'wins' fields
    for key, value in record.get('wins', {}).items():
        flat_record[f'wins_{key}'] = value

    # Process 'attributes' fields
    for key, value in record.get('attributes', {}).items():
        if key == 'roles':
            for i, role in enumerate(value):
                for role_key, role_value in role.items():
                    flat_record[f'attributes_role_{i}_{role_key}'] = role_value
        elif key == 'stats':
            for stats_key, stats_value in value.items():
                flat_record[f'attributes_stats_{stats_key}'] = stats_value
        else:
            flat_record[f'attributes_{key}'] = value

    # Process 'matchup' fields
    for key, value in record.get('matchup', {}).items():
        if key == 'with':
            for with_record in value:
                for with_key, with_value in with_record.items():
                    if with_key != 'heroId2':
                        flat_record[f'with_{with_record["heroId2"]}_{with_key}'] = with_value
                    else:
                        flat_record[f'with_heroId2'] = with_value
        elif key == 'vs':
            for vs_record in value:
                for vs_key, vs_value in vs_record.items():
                    if vs_key != 'heroId2':
                        flat_record[f'vs_{vs_record["heroId2"]}_{vs_key}'] = vs_value
                    else:
                        flat_record[f'vs_heroId2'] = vs_value
        else:
            flat_record[f'matchup_{key}'] = value

    return flat_record


if __name__ == '__main__':
    get_combined_data()
