# Certe NBA Schedule Display

A Flask web application that displays NBA game schedules with live countdowns.

## Features
- Live game countdowns
- Dark theme interface
- Tooltip game information
- Automatic timezone handling (ET)

## Requirements
- Python 3.8+
- Flask
- pandas
- openpyxl
- pytz

## Setup
1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Place NBA schedule file:
- Put `NBA_Schedule_2024-25.xlsx` in the `uploads` folder

3. Run the application:
```bash
python app.py
```

4. Access the site at: http://localhost:5000

## Directory Structure
```
Certe/
├── app.py
├── uploads/
│   └── NBA_Schedule_2024-25.xlsx
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   └── CerteAI_LOGOv1.png
│   └── js/
│       └── script.js
└── templates/
    └── index.html
```

## Deployment

This application is configured for deployment on Railway using Gunicorn. 