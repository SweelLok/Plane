import sqlite3
from connection import get_db_connection, create_table
from clas_funct import FlightCalculator, Airplane, Airport, get_all_planes, load_data_to_calculator, row_to_dict, get_all_airports


create_table()
calculator = FlightCalculator()
load_data_to_calculator(calculator)


while True:
    print("=" * 50)
    print("🛫 СИСТЕМА УПРАВЛІННЯ ПОЛЬОТАМИ 🛬")
    print("=" * 50)
    print("1️⃣  Додати аеропорт")
    print("2️⃣  Додати літак")
    print("3️⃣  Подивитися список літаків")
    print("4️⃣  Подивитися список аеропортів")
    print("5️⃣  Розрахувати можливість польоту")
    print("6️⃣  Закінчити роботу")
    print("=" * 50)
    
    try:
        choice = input("Оберіть опцію (1-6) >>> ")
        if not choice.isdigit():
            raise ValueError("Введене значення не є числом")
        choice = int(choice)
        if choice < 1 or choice > 6:
            raise ValueError("Число повинно бути від 1 до 6")
            

        if choice == 6:
            print("\n👋 Дякуємо за використання системи!")
            break
            

        elif choice == 5:
            print("\n📊 РОЗРАХУНОК ПОЛЬОТУ")
            print("-" * 30)
            airplane_name = input("✈️  Назва літака >>> ")
            distance = float(input("📏 Дистанція (км) >>> "))
            passengers = int(input("👥 Кількість пасажирів >>> "))
            departure_airport_name = input("🛫 Аеропорт вильоту >>> ")
            result = calculator.calculate_flight(airplane_name, distance, passengers, departure_airport_name)
            print(result)


        elif choice == 4:
            print("\n📍 СПИСОК АЕРОПОРТІВ")
            print("-" * 30)
            airports = get_all_airports()
            for airport in airports:
                airport_data = row_to_dict(airport)
                print(f"🏢 Назва: {airport_data['name']}")
                print(f"📏 Довжина ЗПС: {airport_data['runway_length']} м")
                print("-" * 30)


        elif choice == 3:
            print("\n✈️  СПИСОК ЛІТАКІВ")
            print("-" * 30)
            planes = get_all_planes()
            for plane in planes:
                plane_data = row_to_dict(plane)
                print(f"📝 Назва: {plane_data['name']}")
                print(f"⚖️  Базова вага: {plane_data['base_weight']} тонн")
                print(f"⛽️ Паливо/км: {plane_data['fuel_per_km']} тонн")
                print(f"📏 Потрібна ЗПС: {plane_data['runway_length']} м")
                print(f"🍱 Їжа/пасажир: {plane_data['food_per_passenger']} тонн")
                print("-" * 30)


        elif choice == 2:
            print("\n✈️  ДОДАВАННЯ НОВОГО ЛІТАКА")
            print("-" * 30)
            name = input("📝 Назва літака >>> ")
            base_weight = float(input("⚖️  Базова вага (тонн) >>> "))
            fuel_per_km = float(input("⛽️ Витрати палива на км >>> "))
            runway_length = float(input("📏 Потрібна довжина ЗПС >>> "))
            food_per_passenger = float(input("🍱 Їжа на пасажира >>> "))

            try:
                connection = get_db_connection()
                insert_query = """
                INSERT INTO airplane
                (name, base_weight, fuel_per_km, runway_length, food_per_passenger)
                VALUES (?, ?, ?, ?, ?);"""
                connection.execute(insert_query, (name, base_weight, fuel_per_km, runway_length, food_per_passenger)) 
                connection.commit()
                calculator.add_airplane(Airplane(name, base_weight, fuel_per_km, runway_length, food_per_passenger))
                print("\n✅ Новий літак успішно додано!")

            except sqlite3.IntegrityError:
                print("\n❌ Помилка: літак з такою назвою вже існує.")
            except sqlite3.Error as error:
                print("\n❌ Помилка при роботі з базою даних:", error)
            finally:
                if connection:
                    connection.close()


        elif choice == 1:
            print("\n🏢 ДОДАВАННЯ НОВОГО АЕРОПОРТУ")
            print("-" * 30)
            name = input("📝 Назва аеропорту >>> ")
            runway_length = float(input("📏 Довжина ЗПС (м) >>> "))

            try:
                connection = get_db_connection()
                insert_query = """
                INSERT INTO airport
                (name, runway_length)
                VALUES (?, ?);"""
                connection.execute(insert_query, (name, runway_length)) 
                connection.commit()
                calculator.add_airport(Airport(name, runway_length))
                print("\n✅ Новий аеропорт успішно додано!")

            except sqlite3.IntegrityError:
                print("\n❌ Помилка: аеропорт з такою назвою вже існує.")
            except sqlite3.Error as error:
                print("\n❌ Помилка при роботі з базою даних:", error)
            finally:
                if connection:
                    connection.close()
                    
    except ValueError:
        print("\n❌ Помилка: введіть правильне число!")
