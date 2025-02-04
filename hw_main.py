# 1 import
import sqlite3

# 2 create connector
# create if not exist
conn = sqlite3.connect('02_02_2025.db')

# feature: allow access column by name
# row['order_price'] instead of row[3]
# black-box
conn.row_factory = sqlite3.Row

# 3 create cursor
cursor = conn.cursor()


def print_color(message, color="red"):
    match color:
        case "red":
            COLOR = '\033[31m'
            RESET = '\033[0m'
        case "blue":
            COLOR = '\033[34m'
            RESET = '\033[0m'
        case _:
            COLOR = '\033[31m'
            RESET = '\033[0m'
    print(f"{COLOR}{message}{RESET}")


def execute_query_modify(query: str, params: tuple = tuple()):
    """
    modify query
    :param query: query syntax
    :param params: parameters for the ?
    :return: None
    """
    cursor.execute(query, params)
    # cursor.execute('update users set name="danny"', ("danny",))
    # cursor.execute('update users set name=?, set login_time = ?', ("danny",1))
    conn.commit()


def execute_query_select(query: str, params: tuple = tuple()) -> list[dict]:
    """
    read query
    :param query: query syntax
    :param params: parameters for the ?
    :return: list[dict]
    """
    cursor.execute(query, params)
    rows = cursor.fetchall()
    # 1
    # comp
    # answer = [dict(row) for row in rows]
    # 2
    answer = []
    for row in rows:
        answer.append(dict(row))
    return answer


def get_choice_from_menu():
    while True:
        print('Welcome to our garage:')
        print('1. new car')
        print('2. end treatment')
        print('3. remove car')
        print('4. show cars')
        print('5. quit')
        choice: str = input('what do you wanna do?')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print('choose again ...')


def new_car():
    plate_number: str = input("car's plate number? ")
    problem: str = input("car's problem? ")
    phone: str = input("phone number [to call you when done]? ")
    if not plate_number or not problem or not phone:
        print_color(f'cannot enter car to garage with empty data')
        return
    try:
        execute_query_modify('''
        INSERT INTO GARAGE (car_number, car_problem, owner_ph)
        VALUES (?, ?, ?)
        ''', (plate_number, problem, phone))
        print_color(f'car {plate_number} inserted into the garage', "blue")
    except sqlite3.IntegrityError as e:
        print_color(f'cannot enter car to garage, error: {e}')


def end_treatment():
    plate_number: str = input("car's plate number? ")
    result = execute_query_select('''select * from garage where car_number like ?''',(plate_number,))
    if not result:
        print_color(f'there is no car in the garage with number {plate_number}')
        return
    if result[0]['fixed'] == 1:
        print_color(f'car {plate_number} is already fixed!')
        return
    execute_query_modify('''update garage set fixed = ? where car_number like ?''', (1, plate_number,))
    print_color(f'car {plate_number} is now marked as fixed!', 'blue')


def remove_car() -> None:
    '''
    remove car from the garage
    check if exists
    check if fixed
    :return: None
    '''
    # check if car number exist in the garage
    plate_number: str = input("car's plate number? ")
    result = execute_query_select('''select * from garage where car_number like ?''', (plate_number,))
    if not result:
        # car not in garage
        print_color(f'there is no car in the garage with number {plate_number}')
        return
    # check if car is already fixed
    if result[0]['fixed'] == 0:
        # car not yet fixed
        print_color(f'car {plate_number} is NOT yet fixed!')
        return
    # showing call message and removing car from garage
    print_color(f'calling owner of {plate_number}: ph number: {result[0]['owner_ph']} ...', 'blue')
    execute_query_modify('''delete from garage where car_number like ?''', (plate_number,))
    print_color(f'car {plate_number} is released from the garage!', 'blue')


def show_cars():
    result = execute_query_select('''select * from garage''')
    for car in result:
        print(car)


def run_garage() -> None:
    while True:
        choice: str = get_choice_from_menu()
        match choice:
            case "1":
                new_car()
            case "2":
                end_treatment()
            case "3":
                remove_car()
            case "4":
                show_cars()
            case "5":
                print("bye. come again")
                return
            case _:
                continue


if __name__ == "__main__":
    run_garage()

# 5 close connection
conn.close()
