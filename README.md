# d2ds
master project about data science and dota2

### In current branch we got scipt, that convert dota 2 matches into dataframe and script for preprocessing, training model and displaying result
## Dota 2 match converter
1. First of all, we need to convert every single match with non linear structure into N pandas series
2. We achieve this in the following way: we transform each match into a set of metrics that are recorded every minute. If a match consists of 40 minutes, then we will have 40 pandas Series. \
   Each Series displays statistics on characters, towers and the current situation on the map
3. This way we also increase the training set by about 40 times!
### Dota 2 prediction model 
1. The model for predicting the probability of winning in a Dota 2 match was trained using the Gradient Boosting algorithm based on the Catboost library
2. The model produces a result on a delayed sample of 20k matches equal to 0.85 ROC-AUC score and 0.75 Accuracy score
