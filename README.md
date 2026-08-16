# Task Tracker

Task Tracker is a simple task management app designed to help you keep track of daily work in a clean, focused way. It lets you add tasks, mark them complete, remove them when they are no longer needed, and see your overall progress at a glance.

The app uses a small Flask backend and a lightweight React frontend. The backend stores tasks in SQLite, while the frontend presents everything in a modern dark interface.

## How it works

The app follows a simple flow:

1. A user types a task into the input field.
2. The frontend sends that task to the Flask API.
3. The backend saves it to the SQLite database.
4. The task list updates immediately.
5. When a task is completed or removed, the database is updated and the interface refreshes.

This keeps the app easy to understand and easy to extend if more features are added later.

## Main features

- Add new tasks quickly
- Mark tasks as complete or incomplete
- Delete tasks
- View totals for all, completed, and pending tasks
- See completion progress as a percentage
- Keep data saved between sessions using SQLite
- Responsive layout for desktop and mobile screens

## Project structure

```text
Task-tracker/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
├── models/
│   ├── __init__.py
│   └── task.py
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── config.py
├── main.py
├── requirements.txt
├── README.md
└── cli.py
```

## Running the app

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the backend

```bash
python main.py
```

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Then open the local URL shown by Vite, usually:

```text
http://localhost:5173
```

## Why this project is organized this way

The backend is responsible for storing and updating task data, while the frontend is responsible for the interface and user interaction. Separating them keeps the app easier to understand and maintain.

This structure also makes it easier to expand later with features such as task editing, filters, categories, or user accounts without having to rebuild the entire project.

## Notes

- The app uses SQLite, so data is stored locally by default.
- The frontend is intentionally simple and lightweight.
- The project is kept minimal so it remains easy to follow and modify.

## What the app gives you

This project is a practical example of a small full-stack app: a clean interface, a working database, and a straightforward workflow that shows how a frontend and backend can work together in real life.
