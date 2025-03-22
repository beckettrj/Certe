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
            for _ in range(start_row):
                next(rows, None)
            for row_idx in range(start_row, end_row + 1):
                try:
                    row = next(rows)
                    row_data = []
                    for col_idx in range(start_col, end_col + 1):
                        cell = row[col_idx] if col_idx < len(row) else None
                        cell_info = {
                            'value': str(cell.v) if cell and cell.v is not None else '',
                            'type': getattr(cell, 't', ''),
                            'style': {
                                'bold': bool(getattr(cell, 'bold', False)),
                                'italic': bool(getattr(cell, 'italic', False)),
                                'align': getattr(cell, 'alignment', 'right'),
                                'format': getattr(cell, 'number_format', 'general')
                            }
                        }
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
    else:
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

@app.route('/nba_games')
def nba_games():
    try:
        today = datetime.today().date()
        now = datetime.now()
        next_day = today + timedelta(days=1)

        schedule_file = os.path.join('uploads', 'NBA_Schedule.xlsb')
        if not os.path.exists(schedule_file):
            return jsonify({'error': 'NBA_Schedule.xlsb not found'})

        df = pd.read_excel(schedule_file, engine='pyxlsb')
        df['GameDate'] = pd.to_datetime(df['GameDate']).dt.date
        df['GameTime'] = pd.to_datetime(df['GameTime']).dt.time

        todays_games = df[df['GameDate'] == today]
        games = todays_games if not todays_games.empty else df[df['GameDate'] == next_day]

        games = games.sort_values(by='GameTime')

        games_list = []
        for _, row in games.iterrows():
            game_datetime = datetime.combine(row['GameDate'], row['GameTime'])
            countdown = (game_datetime - now).total_seconds()
            games_list.append({
                'teams': f"{row['AwayTeam']} @ {row['HomeTeam']}",
                'datetime': game_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'countdown': max(int(countdown), 0)
            })

        return jsonify(games_list)

    except Exception as e:
        logging.error(f"Error in nba_games route: {str(e)}")
        return jsonify({'error': f'Error processing NBA games: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logging.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)
