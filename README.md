# Sem_Sim

## Установка
1. Склонируйте репозиторий
2. Создайте чистое python окружение и подключитесь к нему
3. Установите зависимости
```bash
pip install -U pip poetry
poetry install
```
Установка для работы ноутбука test.ipynb
```bash
poetry install --with notebook
```

4. Создать копию файла .env.example и назвать .env. Добавить настройки доступа к GigaChat API название модели, пока доступно имя gigachat:
```
MODEL_NAME=...
GIGACHAT_CREDENTIALS=...
GIGACHAT_SCOPE=...

SENT_THRESH=0.8
SIM_EPSILON=0.001
```

SENT_THRESH - порог принятия решения, что фраза семантически находится в предложении
SIM_EPSILON - значение окрестности, в которой относительно самого ближайшего н-грама подходят другие n-грамы

5. Запустите приложение в корне проекта
```bash
streamlit run main.py
```
6. Откройте в браузере http://localhost:8501/

## Пример работы
![alt text](images/example.jpg)

## Метрики
Для проведения оценки качества сервиса был сформирован тестовый датасет в synth_set.csv
В качестве метрики использовалась Accuracy.
#### Результаты:
| Metrics  | GigaChat Embedder |
| ------------- | ------------- |
| Accuracy_overall  | 0.746  |
| Accuracy_sents  | 0.879  |
| Accuracy_words  | 0.729  |

Accuracy_overall - общая точность сервиса
Accuracy_sents - точность, что сервис правильно угадал семантическое наличие или отсутсвие в предолжении 
Accuracy_words - точность, что в предложениях, где есть семантическая близость к фразе правильно угадана