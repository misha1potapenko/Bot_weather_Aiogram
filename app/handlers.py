from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import requests
import datetime

router = Router()


class Town(StatesGroup):
    name_town = State()


class TownProfessional(StatesGroup):
    name_town = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, я бот прогноза погоды. Пожалуйста, выбери кнопочку ниже, какой прогноз тебе нужен.',
                         reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Напиши еще раз название города, если не работает, я сломался((((")


@router.message(F.text == 'Как дела')
async def how_are_you(message: Message):
    await message.answer("Ok")



@router.callback_query(F.data == 'professional')
async def for_professional(message: Message, state: FSMContext):
    await state.set_state(TownProfessional.name_town)
    await message.answer('Введите название города для прогноза погоды')


@router.callback_query(F.data == 'users')
async def get_town(message: Message, state: FSMContext):
    await state.set_state(Town.name_town)
    await message.answer('Введите название города для прогноза погоды')


@router.message(TownProfessional.name_town)
async def get_town_save(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш город {data['name']}")
    city = data['name']
    url_lat_lon = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=ru&format=json'
    # Парси JSON
    result = requests.get(url_lat_lon).json()
    lat = result['results'][0]['latitude']
    lon = result['results'][0]['longitude']
    # # формируем запрос
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,' \
          f'relative_humidity_2m,apparent_temperature,precipitation,cloud_cover,pressure_msl,wind_speed_10m,' \
          f'wind_direction_10m,wind_gusts_10m&hourly=temperature_2m,precipitation_probability,precipitation,' \
          f'weather_code,pressure_msl,cloud_cover,cloud_cover_low,visibility,wind_speed_10m,wind_direction_10m,' \
          f'wind_gusts_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&forecast_days=16&models=best_match'
    # отправляем запрос на сервер и сразу получаем результат
    weather_data = requests.get(url).json()
    list_weather = []
    max_temperature = -40
    min_temperature = 50
    precipitation = 0
    time_precipitation_start = None
    time_precipitation = None
    list_precipitation = []
    pressure_list = []
    visibility_list = []
    for i in range(24):
        pressure = weather_data['hourly']['pressure_msl'][i]
        pressure_list.append(pressure)
    for i in range(24):
        visibility = weather_data['hourly']['visibility'][i]
        if visibility <= 1000:
            time_visibility = weather_data['hourly']['time'][i]
            visibility_list.append(time_visibility[-5:])
            visibility_list.append(visibility)
    for i in range(24):
        if max_temperature < weather_data['hourly']['temperature_2m'][i]:
            max_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24):
        if min_temperature > weather_data['hourly']['temperature_2m'][i]:
            min_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24):
        if precipitation < weather_data['hourly']['precipitation'][i]:
            precipitation = weather_data['hourly']['precipitation'][i]
            time_precipitation = weather_data['hourly']['time'][i]
            if time_precipitation_start is None:
                time_precipitation_start = weather_data['hourly']['time'][i]
            list_precipitation.append(time_precipitation[-5:])
    if precipitation > 0:
        if precipitation <= 0.5:
            string_precipitation_small = (f"🌦️Ожидаются незначительные осадки, в часы: "
                                          f"{list_precipitation}")
        elif precipitation > 0.5:
            string_precipitation_small = (f"🌧️Ожидаются осадки, в часы: "
                                          f" {list_precipitation}")
    else:
        string_precipitation_small = (f"Осадки не ожидаются\n")
    string_weather = (f"Сегодня температура днем: {max_temperature}\n"
                      f"Температура утром (минимальная): {min_temperature}\n"
                      f"Давление в эти сутки по часам: {pressure_list}\n"
                      f"Видимость {visibility_list} ")

    list_weather.append(string_weather)
    list_weather.append(string_precipitation_small)
    if time_precipitation != None:
        list_weather.append(f'Начнутся после {time_precipitation_start[-5:]}')
    finish_string = "\n".join(list_weather)
    await message.answer(finish_string)
    # bot.send_message(message.from_user.id, finish_string)
    list_weather_tm = []
    max_temperature = -40
    min_temperature = 50
    precipitation = 0
    time_precipitation = None
    list_precipitation = []
    for i in range(24, 48):
        if max_temperature < weather_data['hourly']['temperature_2m'][i]:
            max_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24, 48):
        if min_temperature > weather_data['hourly']['temperature_2m'][i]:
            min_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24, 48):
        if precipitation < weather_data['hourly']['precipitation'][i]:
            precipitation = weather_data['hourly']['precipitation'][i]
            if time_precipitation is None:
                time_precipitation = weather_data['hourly']['time'][i]
                list_precipitation.append(time_precipitation[11:16])
            # list_weather_tm.append(f'Осадки начнуться примерно в {time_precipitation[-5:]}')
    if precipitation > 0:
        if precipitation <= 0.5:
            string_precipitation_small_tm = (f"🌦️Ожидаются незначительные осадки, в часы: "
                                             f" {list_precipitation}")
        elif precipitation > 0.5:
            string_precipitation_small_tm = (f"🌧️Ожидаются осадки, в часы: "
                                             f"{list_precipitation}")
    else:
        string_precipitation_small_tm = (f"Осадки не ожидаются\n")
    string_weather_tomorrow = (f"Завтра температура днем: {max_temperature}\n"
                      f"Температура утром (минимальная): {min_temperature}")

    list_weather_tm.append(string_weather_tomorrow)
    list_weather_tm.append(string_precipitation_small_tm)
    if time_precipitation != None:
        list_weather_tm.append(f'Начнутся после {list_precipitation}')
    finish_string_tm = "\n".join(list_weather_tm)
    id = message.from_user.id
    with open('file.txt', 'a', encoding='utf-8') as f:
        f.write(f"{city}  ")
        f.write(f"{datetime.datetime.now()}  ")
        f.write(f"{id}  ")
        f.write("\n")
    await message.answer(finish_string_tm)
    # bot.send_message(message.from_user.id, finish_string_tm)
    await state.clear()
    list_precipitation = []
    visibility_list = []

@router.message(Town.name_town)
async def get_town_save(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш город {data['name']}")
    city = data['name']
    url_lat_lon = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=ru&format=json'
    # Парси JSON
    result = requests.get(url_lat_lon).json()
    lat = result['results'][0]['latitude']
    lon = result['results'][0]['longitude']
    # # формируем запрос
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,' \
          f'precipitation_probability,precipitation,cloud_cover_low,wind_speed_10m&models=best_match'
    # отправляем запрос на сервер и сразу получаем результат
    weather_data = requests.get(url).json()
    list_weather = []
    max_temperature = -40
    min_temperature = 50
    precipitation = 0
    time_precipitation = None
    for i in range(24):
        if max_temperature < weather_data['hourly']['temperature_2m'][i]:
            max_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24):
        if min_temperature > weather_data['hourly']['temperature_2m'][i]:
            min_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24):
        if precipitation < weather_data['hourly']['precipitation'][i]:
            precipitation = weather_data['hourly']['precipitation'][i]
            if time_precipitation is None:
                time_precipitation = weather_data['hourly']['time'][i]
    if precipitation > 0:
        if precipitation <= 0.5:
            string_precipitation_small = (f"🌦️Ожидаются незначительные осадки")
        elif precipitation > 0.5:
            string_precipitation_small = (f"🌧️Ожидаются осадки")
    else:
        string_precipitation_small = (f"Осадки не ожидаются\n")
    string_weather = (f"Сегодня температура днем: {max_temperature}\n"
                      f"Температура утром (минимальная): {min_temperature}")

    list_weather.append(string_weather)
    list_weather.append(string_precipitation_small)
    if time_precipitation != None:
        list_weather.append(f'Начнутся после {time_precipitation[-5:]}')
    finish_string = "\n".join(list_weather)
    await message.answer(finish_string)
    # bot.send_message(message.from_user.id, finish_string)
    list_weather_tm = []
    max_temperature = -40
    min_temperature = 50
    precipitation = 0
    time_precipitation = None
    for i in range(24, 48):
        if max_temperature < weather_data['hourly']['temperature_2m'][i]:
            max_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24, 48):
        if min_temperature > weather_data['hourly']['temperature_2m'][i]:
            min_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24, 48):
        if precipitation < weather_data['hourly']['precipitation'][i]:
            precipitation = weather_data['hourly']['precipitation'][i]
            if time_precipitation is None:
                time_precipitation = weather_data['hourly']['time'][i]
            # list_weather_tm.append(f'Осадки начнуться примерно в {time_precipitation[-5:]}')
    if precipitation > 0:
        if precipitation <= 0.5:
            string_precipitation_small_tm = (f"🌦️Ожидаются незначительные осадки")
        elif precipitation > 0.5:
            string_precipitation_small_tm = (f"🌧️Ожидаются осадки")
    else:
        string_precipitation_small_tm = (f"Осадки не ожидаются\n")
    string_weather_tomorrow = (f"Завтра температура днем: {max_temperature}\n"
                               f"Температура утром (минимальная): {min_temperature}")
    list_weather_tm.append(string_weather_tomorrow)
    list_weather_tm.append(string_precipitation_small_tm)
    if time_precipitation != None:
        list_weather_tm.append(f'Начнутся после {time_precipitation[-5:]}')
    finish_string_tm = "\n".join(list_weather_tm)
    id = message.from_user.id
    with open('file.txt', 'a', encoding='utf-8') as f:
        f.write(f"{city}  ")
        f.write(f"{datetime.datetime.now()}  ")
        f.write(f"{id}  ")
        f.write("\n")
    await message.answer(finish_string_tm)
    # bot.send_message(message.from_user.id, finish_string_tm)
    await state.clear()


@router.message(F.text)
async def how_are_you(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f"Ваш город {data['name']}")
    city = data['name']
    url_lat_lon = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=ru&format=json'
    # Парси JSON
    result = requests.get(url_lat_lon).json()
    lat = result['results'][0]['latitude']
    lon = result['results'][0]['longitude']
    # # формируем запрос
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,' \
          f'precipitation_probability,precipitation,cloud_cover_low,wind_speed_10m&models=best_match'
    # отправляем запрос на сервер и сразу получаем результат
    weather_data = requests.get(url).json()
    list_weather = []
    max_temperature = -40
    min_temperature = 50
    precipitation = 0
    time_precipitation = None
    for i in range(24):
        if max_temperature < weather_data['hourly']['temperature_2m'][i]:
            max_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24):
        if min_temperature > weather_data['hourly']['temperature_2m'][i]:
            min_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24):
        if precipitation < weather_data['hourly']['precipitation'][i]:
            precipitation = weather_data['hourly']['precipitation'][i]
            if time_precipitation is None:
                time_precipitation = weather_data['hourly']['time'][i]
    if precipitation > 0:
        if precipitation <= 0.5:
            string_precipitation_small = (f"🌦️Ожидаются незначительные осадки")
        elif precipitation > 0.5:
            string_precipitation_small = (f"🌧️Ожидаются осадки")
    else:
        string_precipitation_small = (f"Осадки не ожидаются\n")
    string_weather = (f"Сегодня температура днем: {max_temperature}\n"
                      f"Температура утром (минимальная): {min_temperature}")

    list_weather.append(string_weather)
    list_weather.append(string_precipitation_small)
    if time_precipitation != None:
        list_weather.append(f'Начнутся после {time_precipitation[-5:]}')
    finish_string = "\n".join(list_weather)
    await message.answer(finish_string)
    # bot.send_message(message.from_user.id, finish_string)
    list_weather_tm = []
    max_temperature = -40
    min_temperature = 50
    precipitation = 0
    time_precipitation = None
    for i in range(24, 48):
        if max_temperature < weather_data['hourly']['temperature_2m'][i]:
            max_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24, 48):
        if min_temperature > weather_data['hourly']['temperature_2m'][i]:
            min_temperature = weather_data['hourly']['temperature_2m'][i]
    for i in range(24, 48):
        if precipitation < weather_data['hourly']['precipitation'][i]:
            precipitation = weather_data['hourly']['precipitation'][i]
            if time_precipitation is None:
                time_precipitation = weather_data['hourly']['time'][i]
            # list_weather_tm.append(f'Осадки начнуться примерно в {time_precipitation[-5:]}')
    if precipitation > 0:
        if precipitation <= 0.5:
            string_precipitation_small_tm = (f"🌦️Ожидаются незначительные осадки")
        elif precipitation > 0.5:
            string_precipitation_small_tm = (f"🌧️Ожидаются осадки")
    else:
        string_precipitation_small_tm = (f"Осадки не ожидаются\n")
    string_weather_tomorrow = (f"Завтра температура днем: {max_temperature}\n"
                               f"Температура утром (минимальная): {min_temperature}")
    list_weather_tm.append(string_weather_tomorrow)
    list_weather_tm.append(string_precipitation_small_tm)
    if time_precipitation != None:
        list_weather_tm.append(f'Начнутся после {time_precipitation[-5:]}')
    finish_string_tm = "\n".join(list_weather_tm)
    id = message.from_user.id
    with open('file.txt', 'a', encoding='utf-8') as f:
        f.write(f"{city}  ")
        f.write(f"{datetime.datetime.now()}  ")
        f.write(f"{id}  ")
        f.write("\n")
    await message.answer(finish_string_tm)
    # bot.send_message(message.from_user.id, finish_string_tm)
    await state.clear()
