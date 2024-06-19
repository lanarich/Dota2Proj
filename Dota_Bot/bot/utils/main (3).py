import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark import SQLContext
import requests
from pyspark.ml.recommendation import ALS, ALSModel

def preprocess_train_df():
    df = pd.read_csv('als_df.csv')
    df = df[['didRadiantWin', 'heroId', 'steamAccountId', 'isRadiant']]
    df[['didRadiantWin', 'isRadiant']] = df[['didRadiantWin', 'isRadiant']].astype(int)
    df['Won'] = (~((df['didRadiantWin'] ^ df['isRadiant']).astype(bool))).astype(int)

    return df

def create_pyspark_context():
    spark = SparkSession.builder.appName("ALS_algo").getOrCreate()
    return spark

def train_als_model(context, df):
    data = context.createDataFrame(df)
    # Преобразуем данные в формат, необходимый для ALS
    ratings = data[["steamAccountId", "heroId", "Won"]]
    # Разделяем данные на тренировочный и тестовый наборы
    (training, test) = ratings.randomSplit([0.8, 0.2])
    # Создаем и обучаем модель ALS
    als = ALS(maxIter=10, implicitPrefs=False, regParam=0.1, userCol="steamAccountId", itemCol="heroId",
              ratingCol="Won", coldStartStrategy='drop')
    model = als.fit(training)

    model.save('als_model')

    evaluator = RegressionEvaluator(metricName="rmse", labelCol="Won", predictionCol="prediction")
    predictions = model.transform(test)
    rmse = evaluator.evaluate(predictions)
    print("RMSE=" + str(rmse))

    userRecs = model.recommendForAllUsers(5)
    userRecs.show(truncate=False)

    # Останавливаем SparkSession
    context.stop()

    return model


def get_user_hero_matrix(my_id):
    matches = requests.get(f"https://api.opendota.com/api/players/{my_id}/matches?limit=100")
    parsed_matches = matches.json()
    base_dict = {'didRadiantWin': [single['radiant_win'] for single in parsed_matches],
                 'heroId': [hero['hero_id'] for hero in parsed_matches],
                 'steamAccountId': [my_id] * len(parsed_matches),
                 'isRadiant': [1 if _match['player_slot'] < 10 else 0 for _match in parsed_matches],
                 }
    new_df = pd.DataFrame(base_dict)
    new_df[['didRadiantWin', 'isRadiant']] = new_df[['didRadiantWin', 'isRadiant']].astype(int)
    new_df['Won'] = (~((new_df['didRadiantWin'] ^ new_df['isRadiant']).astype(bool))).astype(int)

    return new_df


def als_predict_heroes(user_id):
    #data = spark.createDataFrame(predict_df[['heroId', 'steamAccountId']])
    context = SparkSession.builder.appName('predict').getOrCreate()

    model = ALSModel.load("als_model")

    user_pred = model.recommendForAllUsers(5)

    row = user_pred.where(user_pred.steamAccountId == user_id).select("recommendations.heroId",
                                                                      "recommendations.rating").collect()
    context.stop()

    return row[0]['heroId'], row[0]['rating']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # df = preprocess_train_df()
    # base_context = create_pyspark_context()
    # model = train_als_model(base_context, df)

    #Фарид, тебе нужна нижняя часть
    id = 103721977
    hero_id, rating = als_predict_heroes(id)
