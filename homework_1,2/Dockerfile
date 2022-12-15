# Docker-команда FROM указывает базовый образ контейнера
# Наш базовый образ - это Linux с предустановленным python-3.10
FROM python:3.10

# Установим переменную окружения
ENV APP_HOME /app

# Установим рабочую директорию внутри контейнера
WORKDIR $APP_HOME

# Скопируем остальные файлы в рабочую директорию контейнера
COPY . $APP_HOME

# Установим зависимости внутри контейнера
RUN pip install --upgrade pip
RUN python -m pip install --upgrade setuptools
RUN pip install -r requirements.txt

# Установим наш персональный помощник, чтобы он запускался командой из консоли
RUN pip install .

# Запустим наше приложение внутри контейнера
ENTRYPOINT ["smart-bot"]
