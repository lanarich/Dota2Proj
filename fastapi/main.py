from fastapi import FastAPI


app = FastAPI()




@app.get("/")
def root():
    return {"message": "Hello, User!"}



@app.post('/predict_winer')
def predict_winer():
    pass


@app.post('/get_info')
def get_info():
    pass



@app.post('/gold_graph')
def get_gold_graph():
    pass



@app.post('/exp_graph')
def get_exp_graph():
    pass



@app.post('/heroes_stats_in_match')
def get_heroes_stats():
    pass




@app.post('/heroes_stats')
def get_heroes_stats_entire():
    pass







