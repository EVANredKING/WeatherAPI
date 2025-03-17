import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Загрузка API ключа из .env файла
load_dotenv()
API_KEY = os.getenv("WEATHERAPI_KEY")

def get_weather(city):
    """Получает данные о погоде для указанного города"""
    base_url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city,
        "lang": "ru"  # Русский язык для описаний
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            return {"error": "Город не найден"}
        elif response.status_code == 401 or response.status_code == 403:
            return {"error": "Неверный API ключ"}
        else:
            return {"error": f"HTTP ошибка: {http_err}"}
    except Exception as err:
        return {"error": f"Произошла ошибка: {err}"}

def display_weather(weather_data):
    """Отображает данные о погоде в удобном формате"""
    if "error" in weather_data:
        print(f"Ошибка: {weather_data['error']}")
        return
    
    # Получение основных данных из нового API
    location = weather_data["location"]
    current = weather_data["current"]
    
    city_name = location["name"]
    country = location["country"]
    temp = current["temp_c"]
    feels_like = current["feelslike_c"]
    description = current["condition"]["text"]
    humidity = current["humidity"]
    pressure = current["pressure_mb"]
    wind_speed = current["wind_kph"] / 3.6  # Конвертация из км/ч в м/с
    
    # Получаем локальное время из API вместо восхода/заката
    local_time = location["localtime"]
    
    # Вывод данных
    print(f"\n{'='*50}")
    print(f"Погода в городе {city_name}, {country}")
    print(f"{'='*50}")
    print(f"Местное время: {local_time}")
    print(f"Температура: {temp}°C")
    print(f"Ощущается как: {feels_like}°C")
    print(f"Описание: {description}")
    print(f"Влажность: {humidity}%")
    print(f"Давление: {pressure} гПа")
    print(f"Скорость ветра: {wind_speed:.1f} м/с")
    print(f"{'='*50}\n")

def main():
    print("Программа прогноза погоды")
    
    if not API_KEY:
        print("Ошибка: API ключ не найден. Создайте файл .env и добавьте WEATHERAPI_KEY=ваш_ключ")
        return
    
    while True:
        city = input("Введите название города (или 'выход' для завершения): ")
        
        if city.lower() in ["выход", "exit", "quit", "q"]:
            print("До свидания!")
            break
        
        weather_data = get_weather(city)
        display_weather(weather_data)

if __name__ == "__main__":
    main() 