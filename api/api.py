from fastapi import FastAPI, HTTPException
from models import Models
import uvicorn
from requests import (
    AddModelRequest,
    DeleteModelRequest,
    TrainModelRequest,
    PredictionModelRequest,
)

model = Models()
app = FastAPI()


@app.get("/models")
def return_models():
    """
    Возвращает список доступных моделей

    Возвращает:
    - dict: Список имен доступных моделей

    """

    return model.get_available_models()


@app.post("/add_model")
def add(request: AddModelRequest):
    """
    Добавляет новую модель с указанным классом, названием модели и
    гиперпараметрами

    Аргументы:
    - request (AddModel): Объект запроса, содержащий информацию о модели,
    которую нужно добавить

    Возвращает:
    - dict: Словарь с сообщением о добавлении модели

    Исключения:
    - HTTPException: Возникает, если указано неправильное семейство классов
    моделей

    """

    model_class = request.model_class
    model_name = request.model_name
    hyperparameters = request.hyperparameters

    try:
        model.add_model(model_class, model_name, hyperparameters)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Такого семейства классов моделей не существует.Выберите один из Linear models, Tree models",
        )

    return {"Message": "Модель добавлена"}


@app.post("/delete_model")
def delete(request: DeleteModelRequest):
    """
    Удаляет модель с указанным классом, названием модели

    Аргументы:
    - request (DeleteModel): Объект запроса, содержащий информацию о модели,
    которую нужно удалить

    Возвращает:
    - dict: Словарь с сообщением об удалении модели

    Исключения:
    - HTTPException: Возникает, если указанная модель не была добавлена

    """

    model_class = request.model_class
    model_name = request.model_name

    try:
        model.delete_model(model_class, model_name)
    except KeyError:
        raise HTTPException(
            status_code=404, detail="Модель с таким названием не была добавлена"
        )
    return {"Message": "Модель удалена"}


@app.post("/train")
def train_model(request: TrainModelRequest):
    """
    Обучает модель с указанным классом, названием модели на поданных данных

    Аргументы:
    - request (Training): Объект запроса, содержащий информацию о модели,
    которую нужно обучить, и данных для обучения

    Возвращает:
    - dict: Словарь с сообщением об успешном обучении модели

    Исключения:
    - HTTPException: Возникает, если недостаточно данных или указанная модель
    не была добавлена или в данных есть менее двух классов

    """

    model_class = request.model_class
    model_name = request.model_name
    data = request.data
    data_name = request.data_name

    if len(list(data.values())[0]) < 2:
        raise HTTPException(status_code=400, detail="Недостаточно данных")

    try:
        model.train(model_class, model_name, data, data_name)
    except KeyError:
        raise HTTPException(
            status_code=404, detail="Модель с таким названием не была добавлена"
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="В данных нужно хотя бы два класса")
    return {"Message": "Модель успешно обучена"}


@app.post("/predict")
def predict_model(request: PredictionModelRequest):
    """
    Выполняет предсказание с использованием указанной модели на данных
    поданных в модель

    Аргументы:
    - request (Prediction): Объект запроса, содержащий информацию о модели,
    для которой нужно выполнить предсказание, и данных для предсказания

    Возвращает:
    - dict: Словарь с предсказанием модели в виде строки

    Исключения:
    - HTTPException: Возникает, если модель не была обучена, указанная модель
    не была добавлена

    """

    model_class = request.model_class
    model_name = request.model_name
    data = request.data
    data_name = request.data_name

    if not model.models[model_class]["models"][model_name]["is_trained"]:
        raise HTTPException(status_code=404, detail="Модель не обучена. Обучите модель")
    try:
        prediction = model.predict(model_class, model_name, data, data_name)
    except KeyError:
        raise HTTPException(
            status_code=404, detail="Модель с таким названием не была добавлена"
        )
    return {"Prediction": str(prediction)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
