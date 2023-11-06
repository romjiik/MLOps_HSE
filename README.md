# MLOps_HSE
В репозитории реализован REST API, который умеет:
* Добавлять, хранить и удалять ML-модели для задач классификации - линейные и древесные
* Обучать модели с возможностью настройки гиперпараметров. При этом гиперпараметры для различных моделей могут быть разными
* Возвращать список доступных для обучения моделей
* Возвращать предсказание конкретной модели
* Обучать заново и удалять имеющиеся модели

# Структура файлов
В файле model.py находится код с реализацией ML-моделей  
В файле main.py находится код с приложением, реализованном на FastAPI  
В файле swagger.yaml лежит описание API написанное на Swagger
В файле requirements.txt зафиксированы зависимости

# Как запустить
Для запуска API достатосно запустить main.py и перейти по адресу http://0.0.0.0:8080
Команды для работы модели для двух моделей - логистической регрессии, catboost
* Чтобы посмотреть список доступных моделей:
```
curl -X GET http://0.0.0.0:8080/models
```
* Чтобы добавить модель:
```
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Linear models", "model_name":"logreg" ,"hyperparameters":{}}' http://0.0.0.0:8080/add_model    
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Tree models", "model_name":"catboost" ,"hyperparameters":{}}' http://0.0.0.0:8080/add_model       
```
* Чтобы удалить модель:
```
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Linear models", "model_name":"logreg"}' http://0.0.0.0:8080/delete_model
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Tree models", "model_name":"catboost"}' http://0.0.0.0:8080/delete_model
```
* Чтобы обучить модель(данные поступают в формате словаря из фичей и таргета в последнем столбце):
```
 curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Linear models", "model_name":"logreg", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7], "target": [0, 1, 0]}}' http://localhost:8080/train
 curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Tree models", "model_name":"catboost", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7], "target": [0, 1, 0]}}' http://localhost:8080/train
```
* Чтобы сделать предсказание(данные поступают в формате словаря из фичей):
```
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Linear models", "model_name":"logreg", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7]}}' http://localhost:8080/predict  
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Tree models", "model_name":"catboost", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7]}}' http://localhost:8080/predict
```
