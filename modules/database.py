import sqlite3


DB_NAME = "meal_planner.db"


def get_connection():

    conn = sqlite3.connect(DB_NAME)

    return conn


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS accounts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT UNIQUE,

            password TEXT
        )
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS profiles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            account_id INTEGER,

            profile_name TEXT,

            location TEXT,

            food_type TEXT,

            preferred_foods TEXT,
            
            avoided_foods TEXT
        )
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS meal_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            profile_id INTEGER,

            date TEXT,

            meal_type TEXT,

            dish_name TEXT
        )
        '''
    )

    conn.commit()

    conn.close()

def create_profile(
    account_id,
    profile_name,
    location,
    food_type,
    preferred_foods,
    avoided_foods
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO profiles
        (
            account_id,
            profile_name,
            location,
            food_type,
            preferred_foods,
            avoided_foods
        )

        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (
            account_id,
            profile_name,
            location,
            food_type,
            preferred_foods,
            avoided_foods
        )
    )

    conn.commit()

    conn.close()


def get_profiles(account_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT * FROM profiles

        WHERE account_id = ?
        ''',
        (account_id,)
    )

    profiles = cursor.fetchall()

    conn.close()

    return profiles