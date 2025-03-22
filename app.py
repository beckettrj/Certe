import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from pyxlsb import open_workbook
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pytz
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
DEFAULT_FILE = os.path.join('certe_fresh', 'Certe Beta 1.2.xlsb')
DEFAULT_START_CELL = 'G1'
DEFAULT_END_CELL = 'K5'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def parse_cell_reference(cell_ref):
    # Convert Excel column letters to numbers (e.g., 'A' -> 0, 'B' -> 1)
    column = ""
    row = ""
    for char in cell_ref:
        if char.isalpha():
            column += char
        else:
            row += char
    
    col_num = 0
    for i, char in enumerate(reversed(column.upper())):
        col_num += (ord(char) - ord('A') + 1) * (26 ** i)
    return int(row) - 1, col_num - 1

def read_excel_data(filepath, start_cell, end_cell):
    start_row, start_col = parse_cell_reference(start_cell)
    end_row, end_col = parse_cell_reference(end_cell)
    
    data = []
    if filepath.endswith('.xlsb'):
        with open_workbook(filepath) as wb:
            sheet = wb.get_sheet(1)
            rows = sheet.rows()
            # Skip to start_row
            for _ in range(start_row):
                next(rows, None)
            # Read the required rows
            for row_idx in range(start_row, end_row + 1):
                try:
                    row = next(rows)
                    row_data = []
                    for col_idx in range(start_col, end_col + 1):
                        cell = row[col_idx] if col_idx < len(row) else None
                        cell_info = {
                            'value': str(cell.v) if cell and cell.v is not None else '',
                            'type': getattr(cell, 't', ''),  # Cell type (n=number, s=string, etc.)
                            'style': {
                                'bold': bool(getattr(cell, 'bold', False)),
                                'italic': bool(getattr(cell, 'italic', False)),
                                'align': getattr(cell, 'alignment', 'right'),
                                'format': getattr(cell, 'number_format', 'general')
                            }
                        }
                        
                        # Handle number formatting
                        if cell and cell.v is not None:
                            if isinstance(cell.v, float):
                                if cell_info['style']['format'] == 'general':
                                    cell_info['value'] = f"{cell.v:.2f}"
                                elif '%' in str(cell_info['style']['format']):
                                    cell_info['value'] = f"{cell.v:.1%}"
                                    cell_info['style']['format'] = 'percentage'
                            elif isinstance(cell.v, int):
                                cell_info['value'] = str(cell.v)
                        
                        row_data.append(cell_info)
                    data.append(row_data)
                except StopIteration:
                    break
    else:  # xlsx file
        df = pd.read_excel(filepath)
        for row in range(start_row, end_row + 1):
            row_data = []
            for col in range(start_col, end_col + 1):
                try:
                    value = df.iloc[row, col]
                    cell_info = {
                        'value': str(value) if pd.notna(value) else '',
                        'type': 'n' if isinstance(value, (int, float)) else 's',
                        'style': {
                            'bold': False,
                            'italic': False,
                            'align': 'right',
                            'format': 'general'
                        }
                    }
                    row_data.append(cell_info)
                except:
                    row_data.append({
                        'value': '',
                        'type': 's',
                        'style': {
                            'bold': False,
                            'italic': False,
                            'align': 'right',
                            'format': 'general'
                        }
                    })
            data.append(row_data)
    return data

@app.route('/')
def index():
    logging.info("Index route hit")
    return render_template('index.html', 
                         default_file=os.path.basename(DEFAULT_FILE),
                         default_start_cell=DEFAULT_START_CELL,
                         default_end_cell=DEFAULT_END_CELL)

@app.route('/get_data', methods=['POST'])
def get_data():
    logging.info("Get data route hit")
    start_cell = request.form.get('start_cell', 'A1')
    end_cell = request.form.get('end_cell', 'A1')
    use_default = request.form.get('use_default', 'false') == 'true'
    
    try:
        if use_default:
            if not os.path.exists(DEFAULT_FILE):
                return jsonify({'error': f'Default file not found in {DEFAULT_FILE}'})
            data = read_excel_data(DEFAULT_FILE, start_cell, end_cell)
            return jsonify({'data': data})
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        if not (file.filename.endswith('.xlsb') or file.filename.endswith('.xlsx')):
            return jsonify({'error': 'Please upload an XLSB or XLSX file'})
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            data = read_excel_data(filepath, start_cell, end_cell)
            return jsonify({'data': data})
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        logging.error(f"Error in get_data: {str(e)}")
        return jsonify({'error': str(e)})

@app.route('/certe_fresh/<path:filename>')
def serve_certe_file(filename):
    logging.info(f"Serving file: {filename}")
    return send_from_directory('certe_fresh', filename)

def format_countdown(target_datetime):
    try:
        current_time = datetime.now(pytz.timezone('America/New_York'))
        time_diff = target_datetime - current_time
        days = time_diff.days
        seconds = time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{days}:{hours:02d}:{minutes:02d}:{seconds:02d}"
    except Exception as e:
        logging.error(f"Error formatting countdown: {str(e)}")
        return "0:00:00:00"

@app.route('/todays_games')
def todays_games_route():
    logging.info("Today's games route hit")
    try:
        schedule_file = os.path.join('uploads', 'NBA_Schedule_2024-25.xlsx')
        if not os.path.exists(schedule_file):
            return jsonify({'error': f'Schedule file not found at: {schedule_file}'})
        
        try:
            df = pd.read_excel(schedule_file, engine='openpyxl')
        except Exception as e:
            return jsonify({'error': f'Error reading Excel file: {str(e)}'})
        
        # ... rest of your todays_games_route code ...

    except Exception as e:
        logging.error(f"Error in todays_games_route: {str(e)}")
        return jsonify({'error': f'Error processing schedule: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logging.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)

