import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Дані успішно завантажено!")
        return data
    except Exception as e:
        print(f"Помилка завантаження даних: {e}")
        return None

def preprocess_data(data):
    data['last_updated'] = pd.to_datetime(data['last_updated'], errors='coerce')
    data = data.dropna(subset=['last_updated'])
    data = data.sort_values(by='last_updated')
    print("Дані успішно оброблено!")
    return data

def safe_and_risk_analysis(data):
    data['safety_level'] = np.select(
        [data['air_quality_PM2.5'] <= 50,
         (data['air_quality_PM2.5'] > 50) & (data['air_quality_PM2.5'] <= 100),
         data['air_quality_PM2.5'] > 100],
        ['Безпечно', 'Допустимо', 'Небезпечно'],
        default='Невідомо'
    )
    plt.figure(figsize=(12, 6))
    sns.countplot(data=data, x='safety_level', order=['Безпечно', 'Допустимо', 'Небезпечно'])
    plt.title('Рівень безпеки повітря для алергіків')
    plt.xlabel('Рівень безпеки')
    plt.ylabel('Кількість днів')
    plt.show()
    safe_days = data[data['safety_level'] == 'Безпечно']
    risk_days = data[data['safety_level'] == 'Небезпечно']
    print(f"Кількість безпечних днів: {len(safe_days)}")
    print(f"Кількість небезпечних днів: {len(risk_days)}")

def seasonal_analysis(data):
    data['month'] = data['last_updated'].dt.month
    seasonal_mean = data.groupby('month')['air_quality_PM2.5'].mean()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=seasonal_mean.index, y=seasonal_mean.values)
    plt.title('Сезонна зміна PM2.5')
    plt.xlabel('Місяць')
    plt.ylabel('PM2.5 (мкг/м³)')
    plt.xticks(range(1, 13))
    plt.grid(True)
    plt.show()

def yearly_recommendations(data):
    data['month'] = data['last_updated'].dt.month
    monthly_mean = data.groupby('month')['air_quality_PM2.5'].mean()
    print("\nРекомендації для алергіків на основі середніх показників за рік:")
    for month in range(1, 13):
        avg_pm25 = monthly_mean.get(month, None)
        month_name = datetime(2023, month, 1).strftime('%B')
        if avg_pm25 is None:
            print(f"ℹ️ {month_name}: Даних немає.")
        elif avg_pm25 <= 50:
            print(f"✅ {month_name}: Повітря чисте, можна виходити.")
        elif 50 < avg_pm25 <= 100:
            print(f"⚠️ {month_name}: Допустимий рівень забруднення. Краще обмежити час на вулиці.")
        else:
            print(f"🚫 {month_name}: Високий рівень забруднення, залишайтеся вдома!")

def correlation_analysis(data):
    plt.figure(figsize=(12, 8))
    weather_params = ['temperature_celsius', 'humidity', 'wind_kph', 'pressure_mb',
                      'air_quality_PM2.5', 'air_quality_PM10',
                      'air_quality_us-epa-index', 'air_quality_gb-defra-index']
    correlation_matrix = data[weather_params].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Кореляція між параметрами погоди та якістю повітря')
    plt.show()

def main(file_path):
    data = load_data(file_path)
    if data is not None:
        data = preprocess_data(data)
        safe_and_risk_analysis(data)
        seasonal_analysis(data)
        yearly_recommendations(data)
        correlation_analysis(data)

if __name__ == "__main__":
    file_path = "GlobalWeatherRepository.csv"
    main(file_path)
