import unittest
from datetime import datetime
from P2 import update_meter_data, load_data, save_data, DATA_FILE, HISTORY_FILE

class TestElectricityMeter(unittest.TestCase):

    def setUp(self):
        """Скидає файли даних перед кожним тестом"""
        initial_data = {
            "12345": {"day": 150, "night": 80}
        }
        initial_history = {
            "12345": [{
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "day": 150,
                "night": 80,
                "bill": 0.0
            }]
        }
        save_data(DATA_FILE, initial_data)
        save_data(HISTORY_FILE, initial_history)

    def test_update_existing_meter(self):
        update_meter_data("12345", 200, 120)
        data = load_data(DATA_FILE)
        self.assertEqual(data["12345"], {"day": 200, "night": 120})

    def test_new_meter(self):
        update_meter_data("67890", 200, 100)
        data = load_data(DATA_FILE)
        self.assertIn("67890", data)

    def test_lower_both(self):
        update_meter_data("12345", 250, 160)
        data = load_data(DATA_FILE)
        self.assertEqual(data["12345"], {"day": 250, "night": 160})  # Перевірка оновлених значень

    def test_lower_day(self):
        update_meter_data("12345", 250, 80)
        data = load_data(DATA_FILE)
        self.assertEqual(data["12345"], {"day": 250, "night": 80})  # Перевірка лише дня

    def test_lower_night(self):
        update_meter_data("12345", 150, 160)
        data = load_data(DATA_FILE)
        self.assertEqual(data["12345"], {"day": 150, "night": 160})  # Перевірка лише ночі

if __name__ == "__main__":
    unittest.main()
