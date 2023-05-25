import os
import sys
import dill

import pandas as pd
import numpy as np
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
# from src.logger import logging

def save_obj(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path,'wb') as f:
            dill.dump(obj, f)
    except Exception as e:
        raise CustomException(e,sys)
def evaluate_model(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = list(param.values())[i]

            grid_search = GridSearchCV(model, para, cv=3, )
            grid_search.fit(X_train,y_train)

            model.set_params(**grid_search.best_params_)
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_score = r2_score(y_train_pred,y_train)
            test_score = r2_score(y_test_pred,y_test)

            print(list(models.keys())[i],train_score, test_score)
            report[list(models.keys())[i]] = [train_score,test_score]

        return report 
    except Exception as e:
        raise CustomException(e,sys)


def load_object(file_path):
    try:
        with open(file_path, 'rb') as f:
            return dill.load(file_path)
    except Exception as e:
        raise CustomException(e, sys)
