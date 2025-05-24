import os
import sqlite3
import json

DB_FILE = 'assets/database.db'

def initialize_database():
    if not os.path.exists(DB_FILE):
        print("Creating SQLite database...")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        try:
            # Create users table
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')

            # Create moods table
            cursor.execute('''
                CREATE TABLE moods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT,
                    mood_result TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

            # Create quotes table
            cursor.execute('''
                CREATE TABLE quotes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quote_text TEXT
                )
            ''')

            # Create questions table with options
            cursor.execute('''
                CREATE TABLE questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    option1 TEXT,
                    option2 TEXT,
                    option3 TEXT,
                    option4 TEXT,
                    option5 TEXT
                )
            ''')

            # Insert sample quotes
            sample_quotes = [
                "Believe in yourself! You are stronger than you think.",
                "Keep going. Everything you need will come to you.",
                "One step at a time, one day at a time."
            ]
            cursor.executemany("INSERT INTO quotes (quote_text) VALUES (?)", [(q,) for q in sample_quotes])

            # Insert questions from JSON if file exists
            if os.path.exists("assets/questions.json"):
                with open("assets/questions.json", "r", encoding="utf-8") as f:
                    questions = json.load(f)
                    for q in questions:
                        # Extract option texts from option dicts
                        option_texts = [opt['text'] for opt in q['options']]
                        # Ensure exactly 5 options (fill with empty string if less)
                        while len(option_texts) < 5:
                            option_texts.append('')
                        cursor.execute('''
                            INSERT INTO questions (question, option1, option2, option3, option4, option5)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (q['question'], *option_texts[:5]))

            conn.commit()
            print("Database and tables created with sample data.")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            conn.close()
    else:
        print("Database already exists.")

def get_connection():
    return sqlite3.connect(DB_FILE)
