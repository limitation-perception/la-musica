# log_parser.py
import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

LOG_FILE = Path("play_log.json")

def log_play(song_name):
    # Якщо файла нема — створюємо
    if not LOG_FILE.exists():
        LOG_FILE.write_text("[]", encoding="utf-8")

    # Читаємо існуючі логи
    logs = json.loads(LOG_FILE.read_text(encoding="utf-8"))

    # Поточний час
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Додаємо новий запис
    logs.append({
        "song": song_name,
        "time": now
    })

    # Пишемо назад
    LOG_FILE.write_text(
        json.dumps(logs, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

def plot_day_period_pie():
        if not LOG_FILE.exists():
            print("Файл play_log.json не знайдено!")
            return

        logs = json.loads(LOG_FILE.read_text(encoding="utf-8"))

        periods = {
            "Ніч\n00:00–06:00": 0,
            "Ранок\n06:01–12:00": 0,
            "День\n12:01–18:00": 0,
            "Вечір\n18:01–23:59": 0
        }

        for entry in logs:
            if "time" not in entry:
                continue

            dt = datetime.strptime(entry["time"], "%Y-%m-%d %H:%M:%S")
            hour = dt.hour

            if 0 <= hour <= 6:
                periods["Ніч\n00:00–06:00"] += 1
            elif 6 < hour <= 12:
                periods["Ранок\n06:01–12:00"] += 1
            elif 12 < hour <= 18:
                periods["День\n12:01–18:00"] += 1
            elif 18 < hour <= 23:
                periods["Вечір\n18:01–23:59"] += 1

        labels = list(periods.keys())
        values = list(periods.values())

        # Кольори (гарна м’яка палітра)
        colors = ["#87CEFA", "#FFD700", "#90EE90", "#FFB6C1"]

        plt.figure(figsize=(8, 8))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            textprops={"fontsize": 12}
        )

        plt.title("Активність слухання по періодах дня", fontsize=16)
        plt.tight_layout()
        plt.savefig("static/graph1.png", bbox_inches="tight")
        plt.show()