
import math
import customtkinter as ctk
import requests

# Настройки цветовой палитры (Спокойный серо-голубой стиль Windows 10)
ctk.set_appearance_mode("light")  # Светлая тема
ctk.set_default_color_theme("blue")  # Синие/голубые акценты


class AirportTrackerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Настройки главного окна Windows 10 стандартного типа
        self.title("IATA Airport Route Distance Tracker")
        self.geometry("500x480")
        self.resizable(True, True)  # Кнопки разворачивания активны

        # Конфигурация сетки для адаптивного layout
        self.grid_columnconfigure(0, weight=1)

        # --- Заголовок ---
        self.label_title = ctk.CTkLabel(
            self,
            text="IATA Distance Analytics Tool",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2A3439",
        )
        self.label_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # --- Блок ввода параметров ---
        self.frame_input = ctk.CTkFrame(self, fg_color="#F0F4F8")
        self.frame_input.grid(
            row=1, column=0, padx=20, pady=10, sticky="ew"
        )
        self.frame_input.grid_columnconfigure((0, 1), weight=1)

        self.label_from = ctk.CTkLabel(
            self.frame_input, text="Departure Airport (IATA):", font=ctk.CTkFont(size=13)
        )
        self.label_from.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        self.entry_from = ctk.CTkEntry(
            self.frame_input, placeholder_text="e.g. SVO", width=140
        )
        self.entry_from.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")

        self.label_to = ctk.CTkLabel(
            self.frame_input, text="Arrival Airport (IATA):", font=ctk.CTkFont(size=13)
        )
        self.label_to.grid(row=0, column=1, padx=15, pady=(10, 5), sticky="w")

        self.entry_to = ctk.CTkEntry(
            self.frame_input, placeholder_text="e.g. DXB", width=140
        )
        self.entry_to.grid(row=1, column=1, padx=15, pady=(0, 15), sticky="w")

        # --- Кнопка расчета ---
        self.btn_calculate = ctk.CTkButton(
            self,
            text="Calculate Distance",
            fg_color="#4A76A8",
            hover_color="#3B5E85",
            command=self.calculate_route,
        )
        self.btn_calculate.grid(row=2, column=0, padx=20, pady=15, sticky="ew")

        # --- Текстовое окно вывода информации (Английский язык) ---
        self.textbox_info = ctk.CTkTextbox(
            self,
            width=460,
            height=180,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="#F8FAFC",
            border_color="#CBD5E1",
            border_width=1,
        )
        self.textbox_info.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(3, weight=1)

        # Вывод приветственного текста
        self.log_info(
            "System initialized.\nReady to process IATA location requests..."
        )

    def log_info(self, text):
        """Безопасный вывод информации в текстовое окно."""
        self.textbox_info.configure(state="normal")
        self.textbox_info.delete("1.0", ctk.END)
        self.textbox_info.insert("1.0", text)
        self.textbox_info.configure(state="disabled")

    def get_airport_data(self, iata_code):
        import json
        clean_code = str(iata_code).strip().upper()
        try:
            with open("airports.json", "r", encoding="utf-8") as f:
                database = json.load(f)
            if clean_code in database:
                data = database[clean_code]
                return {
                    "name": data.get("name"),
                    "city": data.get("city"),
                    "lat": float(data.get("latitude")),
                    "lon": float(data.get("longitude"))
                }
            else:
                return f"Error: Airport code '{clean_code}' not found in local database."
        except FileNotFoundError:
            return "Error: Local database file 'airports.json' is missing."
        except Exception:
            return "Error: Failed to parse local database."

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Расчет расстояния по формуле Гаверсинусов (сферическая геометрия)."""
        r_earth = 6371.0  # Радиус Земли в километрах

        # Перевод в радианы
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        return r_earth * c

    def calculate_route(self):
        code_from = self.entry_from.get()
        code_to = self.entry_to.get()

        if not code_from or not code_to:
            self.log_info(
                "Validation Failed:\nPlease enter both Departure and Arrival IATA codes."
            )
            return

        self.log_info("Fetching data from API... Please wait.")
        self.update_idletasks()  # Обновляем UI, чтобы текст "Please wait" отобразился

        # Получаем данные аэропорта А
        airport_a = self.get_airport_data(code_from)
        if isinstance(airport_a, str):  # Если вернулась строка — это ошибка
            self.log_info(airport_a)
            return

        # Получаем данные аэропорта Б
        airport_b = self.get_airport_data(code_to)
        if isinstance(airport_b, str):
            self.log_info(airport_b)
            return

        # Расчет расстояния
        distance = self.haversine_distance(
            airport_a["lat"], airport_a["lon"], airport_b["lat"], airport_b["lon"]
        )

        # Формируем итоговый аналитический отчет на английском
        report = (
            f"--- ROUTE ANALYTICS REPORT ---\n\n"
            f"DEPARTURE:\n"
            f"  Name: {airport_a['name']}\n"
            f"  Location: {airport_a['city']}\n"
            f"  Coordinates: {airport_a['lat']:.4f}, {airport_a['lon']:.4f}\n\n"
            f"ARRIVAL:\n"
            f"  Name: {airport_b['name']}\n"
            f"  Location: {airport_b['city']}\n"
            f"  Coordinates: {airport_b['lat']:.4f}, {airport_b['lon']:.4f}\n\n"
            f"------------------------------\n"
            f"CALCULATED DISTANCE: {distance:.2f} km\n"
            f"------------------------------"
        )
        self.log_info(report)


if __name__ == "__main__":
    app = AirportTrackerApp()
    app.mainloop()
