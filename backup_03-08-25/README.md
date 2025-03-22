# Backup from March 8, 2025

This backup contains the XLSB/XLSX file viewer web application and all its required files.

## Contents

1. Application Files:
   - `app.py` - Main Flask application
   - `requirements.txt` - Python package dependencies
   - `templates/index.html` - Web interface template

2. Input Files:
   - `02-10-2025-nba-season-team-feed.xlsx` - Default Excel file
   - `1744060.webp` - Background image for the grid display

## Setup Instructions

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure all files are in their correct locations:
   - Excel files and background image should be in the `Certe` folder
   - HTML template should be in the `templates` folder

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the application at: http://localhost:5000

## Notes
- The application supports both .xlsx and .xlsb file formats
- Default file path is configured to read from the Certe folder
- Background image is configured to load from the Certe folder 