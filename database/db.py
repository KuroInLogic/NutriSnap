import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "nutrisnap.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the profile table if it does not already exist."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            height REAL NOT NULL,
            weight REAL NOT NULL,
            activity_level TEXT NOT NULL,
            goal TEXT NOT NULL,
            bmr INTEGER NOT NULL,
            tdee INTEGER NOT NULL,
            calorie_target INTEGER NOT NULL,
            protein_target INTEGER NOT NULL,
            carb_target INTEGER NOT NULL,
            fat_target INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_profile(
    age,
    sex,
    height,
    weight,
    activity_level,
    goal,
    bmr,
    tdee,
    calorie_target,
    protein_target,
    carb_target,
    fat_target
):
    """Save or update the user's nutrition profile."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO profile (
            id,
            age,
            sex,
            height,
            weight,
            activity_level,
            goal,
            bmr,
            tdee,
            calorie_target,
            protein_target,
            carb_target,
            fat_target
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        1,
        age,
        sex,
        height,
        weight,
        activity_level,
        goal,
        bmr,
        tdee,
        calorie_target,
        protein_target,
        carb_target,
        fat_target
    ))

    connection.commit()
    connection.close()


def get_profile():
    """Retrieve the saved nutrition profile."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            age,
            sex,
            height,
            weight,
            activity_level,
            goal,
            bmr,
            tdee,
            calorie_target,
            protein_target,
            carb_target,
            fat_target
        FROM profile
        WHERE id = 1
    """)

    profile = cursor.fetchone()
    connection.close()
    return profile