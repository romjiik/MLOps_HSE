import pandas as pd
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
from typing import Literal


class Models:
    def __init__(self):
        self.models = {
            "Linear models": {"models": {}},
            "Tree models": {"models": {}}
        }

    def add_model(
        self,
        model_class: Literal["Linear models", "Tree models"],
        model_name: str,
        hyperparameters: dict = {},
    ):
        """
        Добавляет новую модель в класс

        Аргументы:
        - model_class (Literal["Linear models", "Tree models"]): Семейство
        моделей - "Linear models" или "Tree models"
        - model_name (str): Название модели
        - hyperparameters (dict, опционально): Гиперпараметры модели.
        По умолчанию - пустой словарь

        """

        if model_class == "Linear models":
            self.models[model_class]["models"] = {
                model_name: {
                    "model": LogisticRegression(**hyperparameters),
                    "is_trained": False,
                }
            }
        else:
            self.models[model_class]["models"] = {
                model_name: {
                    "model": CatBoostClassifier(**hyperparameters),
                    "is_trained": False,
                }
            }

    def delete_model(self, model_class: str, model_name: str):
        """
        Удаляет модель из класса

        Аргументы:
        - model_class (str): Семейство моделей, из которого нужно удалить
        модель
        - model_name (str): Название модели, которую нужно удалить

        """

        del self.models[model_class]["models"][model_name]

    def prepare_data(self, data: dict, train: bool = True):
        """
        Подготавливает данные для обучения модели или для предсказания

        Аргументы:
        - data (dict): Словарь с данными, содержащий признаки и целевую
        переменную
        - train (bool, опционально): Флаг, указывающий, являются ли данные для
        обучения модели или для предсказания. По умолчанию - True,
        то есть данные предназначены для обучения модели

        Возвращает:
        Если train=True:
        - tuple: Кортеж из двух элементов: X_train - матрица признаков для
        обучения, y_train - вектор с целевой переменной.
        Если train=False:
        - pd.DataFrame: DataFrame с данными, готовыми для предсказания

        """

        df = pd.DataFrame(data)
        if train:
            data_train, target_train = df.iloc[:, :-1], df.iloc[:, -1]
            return data_train, target_train
        return df

    def train(
        self,
        model_class: Literal["Linear models", "Tree models"],
        model_name: str,
        data: dict,
    ):
        """
        Обучает указанную модель на предоставленных данных

        Аргументы:
        - model_class (Literal["Linear models", "Tree models"]): Класс модели,
        которую нужно обучить - "Linear models" или "Tree models"
        - model_name (str): Название модели, которую нужно обучить
        - data (dict): Словарь с данными для обучения, содержащий признаки и
        целевую переменную

        """

        data_train, target_train = self.prepare_data(data)
        print(self.models)
        clf = self.models[model_class]["models"][model_name]
        clf["model"].fit(data_train, target_train)
        clf["is_trained"] = True

    def predict(
        self,
        model_class: Literal["Linear models", "Tree models"],
        model_name: str,
        data: dict,
    ):
        """
        Выполняет предсказание с использованием указанной модели на
        предоставленных данных

        Аргументы:
        - model_class (Literal["Linear models", "Tree models"]): Класс модели,
        для которой нужно выполнить предсказание - "Linear models" или
        "Tree models"
        - model_name (str): Название модели, для которой нужно выполнить
        предсказание
        - data (dict): Словарь с данными для предсказания, содержащий признаки

        Возвращает:
        - list: Список предсказанных значений

        """

        data_test = self.prepare_data(data, train=False)
        clf = self.models[model_class]["models"][model_name]
        pred = list(clf["model"].predict(data_test))
        return pred

    def get_available_models(self):
        """
        Возвращает доступные модели, разделенные на семейства
        Linear models" и "Tree models"

        Возвращает:
        - dict: Словарь с доступными моделями, разделенными на семейства:
            - "Семейство Linear models":
                - "Модели": Список названий моделей в семействе Linear models
            - "Семейство Tree models":
                - "Модели": Список названий моделей в семействе Tree models
        """

        return {
            "Семейство Linear models": {
                "Модели": [*self.models["Linear models"]["models"].keys()]
            },
            "Семейство Tree models": {
                "Модели": [*self.models["Tree models"]["models"].keys()]
            },
        }
