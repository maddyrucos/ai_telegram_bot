<!DOCTYPE html>
<html>

<body>
  <h1>Телеграм-бот с использованием MistalAI </h1>
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python">
  <p>Данный проект представляет собой телеграм бота, написанного на языке Python, который использует API  <a href="https://mistral.ai/">Mistral AI</a> для обработки запросов и предоставления ответов в виде текста. Бот интегрируется с платформой Telegram и позволяет пользователям общаться с моделью Mistral через интерфейс мессенджера.</p>

  <h2>Возможности</h2>
    <ol>
      <li>
        <b>Пользователь</b>:
        <ul>
          <li> Отправлять запросы к модели Mistral и получать развернутые информативные ответы </li>
        </ul>
        <i>Будет дополняться...</i>
      </li>
      <li>
        <b>Админ</b>:
        <ul>
          <li>Добавлять и удалять пользовтелей из БД (разрешение на использование моделей)</li>
          <li>Делать рассылку всем пользователям бота</li>
          <li>Получать БД в формате .xlsx</li>
        </ul>
      </li>
    </ol>

  
  <h2>Установка</h2>
  <ol>
    <li>Склонируйте репозиторий с помощью команды:<br><code>git clone https://github.com/maddyrucos/ai_telegram_bot.git</code></li><br>
    <li>Перейдите в каталог проекта:<br><code>cd ai_telegram_bot</code></li> <br>
    <li>Создайте виртуальное окружение:<br><code>python3 -m venv venv</code></li> <br>
    <li>Активируйте виртуальное окружение:</li>
    <ul>
      <li>Для Linux/Mac:<br>
        <code>source venv/bin/activate</code></li>
      <li>Для Windows:<br>
        <code>venv\Scripts\activate</code></li>
    </ul> <br>
    <li>Установите зависимости, указанные в файле <code>requirements.txt</code>:<br><code>pip install -r requirements.txt</code></li> <br>
    <li>Создайте файл <code>.env</code> в корневом каталоге проекта и добавьте следующие переменные среды:
      <ul> 
        <li><code>BOT_TOKEN</code> - токен вашего телеграм-бота. Для получения токена создайте нового бота с помощью <a href="https://core.telegram.org/bots#botfather">BotFather</a>.</li>
        <li><code>MISTRAL_TOKEN</code> - ключ API Mistral. Получить ключ можно <a href="https://console.mistral.ai/api-keys/)">по ссылке</a>.</li>
         <li><code>ADMIN</code> - ваш username в телеграм. </li><br>
      </ul>
    <li>Запустите бота:<br><code>python3 main.py</code></li> 
  </ol>

<h3> P.S. </h3>
Вы можете воспользоваться <a href="https://github.com/maddyrucos/ai_telegram_bot/tree/old_version"> старой версией </a> бота на aiogram 2, которая имеет более расширенный функционал и взаимодействует с моделями openai.
