import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor




bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message):
  markup = types.InlineKeyboardMarkup()
  buttonC = types.InlineKeyboardButton('Помощь', callback_data='c')

  markup.row(buttonC)

  await bot.send_message(message.chat.id, 'Привет! Я бот погоды! Я готов к использованию, для помощи нажми кнопку под текстом', reply_markup=markup)


@dp.callback_query_handler(lambda call: True)
async def handle(call):
    await bot.send_message(call.message.chat.id, 'Привет! Напиши мне название города и я пришлю сводку погоды! (Пример:Москва)'.format(str(call.data)))
    await bot.answer_callback_query(call.id)


@dp.message_handler(commands=["help"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды! (Пример:Москва)")




@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"\U0001F44B {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} \U00002600\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"\U0000270C Хорошего дня! \U0000270A"
              )

    except:
        await message.reply("\U0000267F Проверьте название города \U0000267F")





if __name__ == '__main__':
    executor.start_polling(dp)