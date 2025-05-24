# Mental-health-project


# 🧠 Mental Health Desktop App

Mental Health is a Python-based desktop application designed to promote mental wellness. Built with **Tkinter** for the UI and **SQLite** for the database, it provides a friendly and secure environment to track moods, view motivational content, and maintain mental health reports.

---

## 🛠 Features

- 🔐 **User Login and Registration**
  - Simple user creation
  - Secure login for users
  - Static admin login for reporting

- 📊 **Mood Detector**
  - Daily mood detection using a 30-question quiz
  - Results saved to the local SQLite database
  - Tracks mood trends over time

- 💡 **Motivate Me**
  - Random motivational quotes to uplift users

- 📈 **Admin Dashboard**
  - View mood reports of all users
  - Filter by user and date range
  - Responsive, clean, dark-themed UI

---

## 🧱 Technologies Used

| Component        | Technology        |
|------------------|-------------------|
| UI Framework     | Tkinter (Python)  |
| Database         | SQLite            |
| Language         | Python 3.x        |
| Styling          | Custom Tkinter + ttk Dark Theme |
| File Structure   | Modular Python Files |

---

## 📂 Project Structure

```
mood_detective/
│
├── main.py                  # App launcher
├── login.py                 # Login screen
├── register.py              # User registration
├── admin_main_menu.py       # Admin dashboard menu
├── mood_detector.py         # Mood quiz module
├── motivate_me.py           # Motivation quotes module
├── admin_view_reports.py    # Admin: View mood reports
├── show_result.py           # Display mood after quiz
├── assets/
│   └── questions.json       # 30 mood quiz questions
|   └── database.db          # database file
├── modules/
│   └── database.py          # DB connection helpers
└── README.md                # You're here
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed


### Run the App

```bash
python main.py
```

---

## 📋 Admin Credentials

> These are **hardcoded** for demonstration purposes. Change them in `login.py` for production.

```text
Username: admin
Password: admin123
```

---








