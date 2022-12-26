import pandas as pd

from connector.scv_connector import get_data
from sklearn.linear_model import Ridge
from util.model import save_model, load_model
from util.df import encode_df, split
from conf.conf import settings, logging

def training(train_ohe: list) -> None: 
    x_train_ohe = train_ohe.drop('Profit', axis=1)
    y_train_ohe = train_ohe['Profit']

    logging.info("Initialising Ridge")
    RidgeModelInitializer = Ridge(settings.ridge.RIDGE_ALPHA)
    logging.info("Training Ridge")
    RidgeModel = RidgeModelInitializer.fit(x_train_ohe, y_train_ohe)

def prediction(test_ohe: list) -> None:
    x_test_ohe = test_ohe.drop('Profit', axis=1)
    y_test_ohe = test_ohe['Profit']

    logging.info("Loading Ridge model")
    pickled_model = load_model(settings.ridge.MODEL_DIR)
    logging.info("Predicting Ridge")
    predictions_ridge_ohe = pickled_model.predict(x_test_ohe)

    logging.info(f'Ridge prediction is {predictions_ridge_ohe}')
    output_ridge_ohe = pd.DataFrame({ 'realProfit': y_test_ohe, 'Profit': predictions_ridge_ohe})
    
    return output_ridge_ohe

def process():
    df = get_data(settings.data.DATA_SET)
    df = encode_df(df)
    train_ohe, test_ohe = split(df, settings.general.DF_SPLIT_TEST_SIZE, settings.general.DF_SPLIT_RANDOM_STATE)
    clf = training(train_ohe)
    prediction_result = prediction(test_ohe)

    return prediction_result
if __name__ == '__main__':
    process()