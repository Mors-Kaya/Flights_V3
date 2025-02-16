import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="flights"
        )
    except Error as err:
        print(f"Error: {err}")
        return None

def get_airports_in_range(lat_min, lat_max, lon_min, lon_max):
    db = connect_to_db()
    if db is None:
        return []

    try:
        with db.cursor() as cursor:
            query = """
            SELECT * FROM airports
            WHERE latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s
            """
            cursor.execute(query, (lat_min, lat_max, lon_min, lon_max))
            results = cursor.fetchall()
            return results
    except Error as err:
        print(f"Error executing query: {err}")
        return []
    finally:
        if db is not None and db.is_connected():
            db.close()

def display_airports_table(airports):
    print(f"{'id':<5} {'airport':<50} {'city':<30} {'country':<30} {'latitude':<10} {'longitude':<10}")
    print("=" * 100)
    for airport in airports:
        print(f"{airport[0]:<5} {airport[1]:<30} {airport[2]:<20} {airport[3]:<20} {airport[4]:<10} {airport[5]:<10}")

def main():
    while True:
        print("1. Просмотреть аэропорты в диапазоне координат")
        print("2. Найти аэропорт по городу")
        print("3. Просмотреть все рейсы из города")
        print("4. Просмотреть все прямые рейсы между двумя городами")
        print("5. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            lat_min = float(input("Введите минимальную широту: "))
            lat_max = float(input("Введите максимальную широту: "))
            lon_min = float(input("Введите минимальную долготу: "))
            lon_max = float(input("Введите максимальную долготу: "))

            airports = get_airports_in_range(lat_min, lat_max, lon_min, lon_max)

            if airports:
                display_airports_table(airports)
            else:
                print("Аэропорты не найдены.")

        elif choice == '2':
            city = input("Введите город: ")
            airport = find_airport_by_city(city)
            print(airport if airport else "Аэропорт не найден.")

        elif choice == '3':
            city = input("Введите город: ")
            get_flights_from_city(city)

        elif choice == '4':
            city_from = input("Введите город отправления: ")
            city_to = input("Введите город назначения: ")
            get_direct_flights(city_from, city_to)

        elif choice == '5':
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()