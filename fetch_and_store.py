import requests
import psycopg2
from datetime import datetime

# Cấu hình API
API_KEY = "c6d22b4de3bed891334db4f9fb805b3b"  
CITY = "Hanoi"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Cấu hình kết nối PostgreSQL
DB_PARAMS = {
    "dbname": "weather_db",
    "user": "postgres",
    "password": "Trung.110103",  
    "host": "localhost",
    "port": "5432"
}

# Hàm lấy dữ liệu thời tiết
def fetch_weather():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": CITY,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return weather_info
    else:
        print(f"Error: {response.status_code}")
        return None

# Hàm lưu dữ liệu vào PostgreSQL
def store_weather(data):
    print("Data to insert:", data)
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_data (city, timestamp, temperature, humidity, description)
        VALUES (%s, %s, %s, %s, %s)
    """, (data["city"], data["timestamp"], data["temperature"], data["humidity"], data["description"]))
    conn.commit()
    cur.close()
    conn.close()
    print("Data stored successfully!")

# Chạy thử
if __name__ == "__main__":
    weather_data = fetch_weather()
    if weather_data:
        store_weather(weather_data)
