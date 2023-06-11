<!DOCTYPE html>
<html>

<body>
  <h1>Телеграм-бот с использованием API ChatGPT</h1>
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python">
  <p>Данный проект представляет собой телеграм-бота, написанного на языке Python, который использует API ChatGPT для обработки запросов и предоставления ответов в виде текста или картинок. Бот интегрируется с платформой Telegram и позволяет пользователям общаться с моделью ChatGPT через интерфейс мессенджера.</p>
  <h2>Установка</h2>
  <ol>
    <li>Склонируйте репозиторий с помощью команды:<br><code>git clone https://github.com/maddyrucos/telegram_chatgpt_bot.git</code></li>
    <li>Перейдите в каталог проекта:<br><code>cd telegram-chatgpt_bot</code></li>
    <li>Создайте виртуальное окружение:<br><code>python3 -m venv venv</code></li>
    <li>Активируйте виртуальное окружение:</li>
    <ul>
      <li>Для Linux/Mac:<br><code>source venv/bin/activate</code></li>
      <li>Для Windows:<br><code>venv\Scripts\activate</code></li>
    </ul>
    <li>Установите зависимости, указанные в файле <code>requirements.txt</code>:<br><code>pip install -r requirements.txt</code></li>
    <li>Создайте файл <code>.env</code> в корневом каталоге проекта и добавьте следующие переменные среды:
      <ul>
        <li><code>TELEGRAM_TOKEN=&lt;YOUR_TELEGRAM_TOKEN&gt;</code> - токен вашего телеграм-бота. Для получения токена создайте нового бота с помощью <a href="https://core.telegram.org/bots#botfather">BotFather</a>.</li>
        <li><code>OPENAI_API_KEY=&lt;YOUR_OPENAI_API_KEY&gt;</code> - ключ API ChatGPT. Для получения ключа зарегистрируйтесь на <a href="https://openai.com/">openai.com</a>.</li>
      </ul>
    <li>Запустите бота:<br><code>python3 main.py</code></li>
