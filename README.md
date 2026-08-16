# Task Tracker

A small Flask application for managing daily tasks with a dark, responsive interface and persistent SQLite storage.

## Features

- Add, complete, and delete tasks
- Responsive layout for desktop and mobile devices
- SQLite-backed persistence
- Task statistics and progress tracking
- Simple Flask app structure

## Project Structure

```text
Task-tracker/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
├── models/
│   ├── __init__.py
│   └── task.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   └── index.html
├── .env.example
├── .gitignore
├── cli.py
├── config.py
├── main.py
├── requirements.txt
├── README.md
├── tasks.db
└── venv/
```

## Requirements

- Python 3.11+
- pip

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Open:

```text
http://127.0.0.1:5000
```

## Notes

- The app uses SQLite for storage.
- The database file is created automatically on first run.
- For production, set a secure `SECRET_KEY` and use an environment-specific config.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `main.py`:
```python
app.run(port=5001)  # Use a different port
```

### Database Issues
If you encounter database errors, reset the database:
```bash
# Remove the database file
rm tasks.db  # macOS/Linux
del tasks.db  # Windows

# Restart the application
python main.py
```

### Import Errors
If you see import errors, ensure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please:
- Open an issue on GitHub
- Contact the project maintainers

---

**Happy task tracking! 📝**
