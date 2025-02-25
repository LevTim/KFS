import json
from datetime import datetime

# Константи тарифів і накрутки
DAY_TARIFF = 1.5  # грн за 1 кВт
NIGHT_TARIFF = 0.9  # грн за 1 кВт
DAY_OVERCHARGE = 100  # кВт
NIGHT_OVERCHARGE = 80  # кВт

# Файл для збереження історії
DATA_FILE = "meter_data.json"
HISTORY_FILE = "history.json"


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def calculate_bill(previous, current):
    day_usage = current["day"] - previous["day"]
    night_usage = current["night"] - previous["night"]
    return max(day_usage, 0) * DAY_TARIFF + max(night_usage, 0) * NIGHT_TARIFF


def update_meter_data(meter_id, new_day, new_night):
    data = load_data(DATA_FILE)
    history = load_data(HISTORY_FILE)

    if meter_id in data:
        prev_day, prev_night = data[meter_id]["day"], data[meter_id]["night"]
        print(f"Поточні показники для {meter_id}: День - {prev_day}, Ніч - {prev_night}")
    else:
        print(f"Новий лічильник {meter_id}, додано у базу.")
        data[meter_id] = {"day": new_day, "night": new_night}
        history[meter_id] = [{
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "day": new_day,
            "night": new_night,
            "bill": 0.0
        }]
        save_data(DATA_FILE, data)
        save_data(HISTORY_FILE, history)
        return

    # Якщо нові показники менші за попередні, додаємо накрутку
    if new_day < prev_day:
        new_day = prev_day + DAY_OVERCHARGE
    if new_night < prev_night:
        new_night = prev_night + NIGHT_OVERCHARGE

    bill = calculate_bill(data[meter_id], {"day": new_day, "night": new_night})

    if meter_id not in history:
        history[meter_id] = []
    history[meter_id].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "day": new_day,
        "night": new_night,
        "bill": bill
    })

    data[meter_id] = {"day": new_day, "night": new_night}

    save_data(DATA_FILE, data)
    save_data(HISTORY_FILE, history)

    print(f"Оновлені показники для {meter_id}: День - {data[meter_id]['day']}, Ніч - {data[meter_id]['night']}")


def manual_input():
    while True:
        meter_id = input("Введіть номер лічильника (або 'exit' для виходу): ")
        if meter_id.lower() == 'exit':
            break
        data = load_data(DATA_FILE)
        if meter_id in data:
            print(f"Поточні показники для {meter_id}: День - {data[meter_id]['day']}, Ніч - {data[meter_id]['night']}")
        try:
            new_day = int(input("Введіть денні показники: "))
            new_night = int(input("Введіть нічні показники: "))
            update_meter_data(meter_id, new_day, new_night)
        except ValueError:
            print("Помилка! Введіть числові значення.")


if __name__ == "__main__":
    manual_input()
