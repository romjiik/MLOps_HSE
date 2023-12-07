# MLOps_HSE
В репозитории реализован REST API, который умеет:
* Добавлять, хранить и удалять ML-модели для задач классификации - линейные и древесные. Хранение реализовано в S3 с помощью minio
* Сохранять данные. Хранение реализовано в S3 с помощью dvc и minio
* Обучать модели с возможностью настройки гиперпараметров. При этом гиперпараметры для различных моделей могут быть разными
* Возвращать список доступных для обучения моделей
* Возвращать предсказание конкретной модели
* Обучать заново и удалять имеющиеся модели

**Образ апи загружен в Docker hub - romjiik/ml_ops_api**

# Структура файлов
В папке api находится весь код по реализации api  
    - В файле model.py находится код с реализацией ML-моделей  
    - В файле api.py находится код с приложением, реализованном на FastAPI  
    - В файле requests.py находятся классы запросов в API
    - В файле utils.py реализовны дополнительные функции  
    - Файл init_mini_and_dvc.sh настраивает minio и dvc  
В папке .dvc находится мета-информация для dvc  
В папке data сохраняются данные  
В папке minio конфигурация minio  
В файле docker-compose.yaml контейнеры с API и сервером minio (не успел доделать до конца)  
В файле Dockerfile конфигурация image для Docker hub  
В файле swagger.yaml лежит описание API написанное на Swagger  
В файле requirements.txt зафиксированы зависимости  

# Как запустить
Не успел до конца разобраться с docker-compose, поэтому пока что запуск такой:
1. Запускаем конфигурацию minio и dvc
```
sh api/init_minio_and_dvc.sh
```
Дальше можно зайти на http://127.0.0.1:9000 авторизоваться под minioadmin minioadmin и посмотреть созданный бакет. Если на этом этапе все успешно, то далее необходимо запустить сам API  
2. Для запуска API достатосно запустить
```
python3 api/api.py
``` 
и перейти по адресу http://0.0.0.0:8080  


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
* Чтобы обучить модель(данные поступают в формате словаря из фичей и таргета в последнем столбце, название данных):
```
 curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Linear models", "model_name":"logreg", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7], "target": [0, 1, 0]}, "data_name": "test_data"}' http://localhost:8080/train
 curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Tree models", "model_name":"catboost", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7], "target": [0, 1, 0]}, "data_name": "test_data"}' http://localhost:8080/train
```
* Чтобы сделать предсказание(данные поступают в формате словаря из фичей):
```
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Linear models", "model_name":"logreg", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7]}, "data_name": "test_data_predict"}' http://localhost:8080/predict  
curl -X POST -H "Content-Type: application/json" -d '{"model_class":"Tree models", "model_name":"catboost", "data":{"feature_1":[1.2, 0, 4], "feature_2":[3.4, 1, 4.7]}}, "data_name": "test_data_predict"' http://localhost:8080/predict
```
