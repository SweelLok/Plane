import sqlite3
from connection import get_db_connection


class Airplane:
    def __init__(self, name, base_weight, fuel_per_km, runway_length, food_per_passenger):
        self.name = name
        self.base_weight = base_weight
        self.fuel_per_km = fuel_per_km
        self.runway_length = runway_length
        self.food_per_passenger = food_per_passenger
    def calculate_fuel(self, distance, passengers):
        return self.fuel_per_km * distance * (1 + passengers * 0.002)

    def calculate_food(self, passengers):
        return self.food_per_passenger * passengers

    def total_weight(self, distance, passengers):
        
        passenger_weight = passengers * 80
        fuel_weight = self.calculate_fuel(distance, passengers)
        food_weight = self.calculate_food(passengers)
        return self.base_weight + passenger_weight + fuel_weight + food_weight

    def required_runway(self, passengers):
        return self.runway_length + passengers * 0.1


class Airport:
    def __init__(self, name, runway_length):
        self.name = name
        self.runway_length = runway_length


class FlightCalculator:
    def __init__(self):
        self.airplanes = {}
        self.airports = {}

    def add_airplane(self, airplane):
        self.airplanes[airplane.name] = airplane

    def add_airport(self, airport):
        self.airports[airport.name] = airport

    def calculate_flight(self, airplane_name, distance, passengers, departure_airport_name):
        airplane = self.airplanes.get(airplane_name)
        if not airplane:
            return f"Літак {airplane_name} не знайдено."

        departure_airport = self.airports.get(departure_airport_name)
        if not departure_airport:
            return f"Аеропорт {departure_airport_name} не знайдено."

        fuel_needed = airplane.calculate_fuel(distance, passengers)
        food_needed = airplane.calculate_food(passengers)
        total_weight = airplane.total_weight(distance, passengers)
        required_runway = airplane.required_runway(passengers)


        if departure_airport.runway_length < required_runway:
            return f"Літак {airplane_name} не може взлетіти з аеропорта {departure_airport_name}."

        
        valid_airports = []
        for airport in self.airports.values():
            if airport.runway_length >= required_runway * 0.75:
                valid_airports.append(airport.name)


        result = (
            f"\n{"=" * 50}\n"
            f"📋 РЕЗУЛЬТАТИ РОЗРАХУНКУ ПОЛЬОТУ\n"
            f"{"=" * 50}\n\n"
            f"✈️  Літак: {airplane.name}\n"
            f"👥 Кількість пасажирів: {passengers}\n"
            f"📏 Відстань: {distance} км\n"
            f"\n{"-" * 30}\n"
            f"⛽️ Паливо: {fuel_needed} тонн\n"
            f"🍱 Їжа: {food_needed} тонн\n"
            f"⚖️  Загальна маса: {total_weight} тонн\n"
            f"📏 Необхідна довжина ЗПС: {required_runway} м\n"
            f"\n🛫 Аеропорт вильоту: {departure_airport_name}\n"
            f"🛬 Можливі аеропорти посадки:\n"
            f"   {", ".join(valid_airports)}\n"
            f"{"=" * 50}\n"
        )
        return result


def load_data_to_calculator(calculator):
    try:
        connection = get_db_connection()
        airplanes = connection.execute("SELECT * FROM airplane").fetchall()
        for plane in airplanes:
            calculator.add_airplane(Airplane(
                plane['name'],
                plane['base_weight'],
                plane['fuel_per_km'],
                plane['runway_length'],
                plane['food_per_passenger']
            ))
            
        airports = connection.execute("SELECT * FROM airport").fetchall()
        for airport in airports:
            calculator.add_airport(Airport(
                airport['name'],
                airport['runway_length']
            ))
    except sqlite3.Error as error:
        print("Помилка при завантаженні даних:", error)
    finally:
        if connection:
            connection.close()


def get_all_planes():
    try:
        connection = get_db_connection()
        connection.row_factory = sqlite3.Row
        airplane = connection.execute("SELECT * FROM airplane").fetchall()
        connection.close()
        return airplane
        

    except sqlite3.Error as error:
        print("Помилка при отримані кода:", error)
        return []

    finally:
        if connection:
            connection.close()

def get_all_airports():
    try:
        connection = get_db_connection()
        connection.row_factory = sqlite3.Row
        airport = connection.execute("SELECT * FROM airport").fetchall()
        connection.close()
        return airport
        

    except sqlite3.Error as error:
        print("Помилка при отримані кода:", error)
        return []

    finally:
        if connection:
            connection.close()

def row_to_dict(row):
    return dict(row)
