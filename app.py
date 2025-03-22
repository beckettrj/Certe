from flask import Flask, render_template, request, jsonify, send_from_directory
from pyxlsb import open_workbook
import pandas as pd
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pytz
import logging

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
    return render_template('index.html', 
                         default_file=os.path.basename(DEFAULT_FILE),
                         default_start_cell=DEFAULT_START_CELL,
                         default_end_cell=DEFAULT_END_CELL)

@app.route('/get_data', methods=['POST'])
def get_data():
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
        return jsonify({'error': str(e)})

@app.route('/certe_fresh/<path:filename>')
def serve_certe_file(filename):
    return send_from_directory('certe_fresh', filename)

def format_countdown(target_datetime):
    try:
        # Get current time in ET
        current_time = datetime.now(pytz.timezone('America/New_York'))
        
        # Calculate time difference
        time_diff = target_datetime - current_time
        
        # Extract days, hours, minutes, seconds
        days = time_diff.days
        seconds = time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        # Format as Days: HH:MM:SS
        return f"{days}:{hours:02d}:{minutes:02d}:{seconds:02d}"
    except Exception as e:
        print(f"Error formatting countdown: {str(e)}")
        return "0:00:00:00"

def parse_game_time(time_str):
    # Convert time like '7:30p' to proper datetime.time object
    try:
        # Remove any spaces and ensure 'p' or 'a' is followed by 'm'
        time_str = time_str.strip()
        # Handle special case where 'p' or 'a' is at the end
        if time_str.endswith('p') or time_str.endswith('a'):
            time_str = time_str[:-1] + ('pm' if time_str.endswith('p') else 'am')
        return datetime.strptime(time_str, '%I:%M%p').strftime('%H:%M')
    except Exception as e:
        print(f"Error parsing time {time_str}: {str(e)}")
        return None

def get_next_game():
    try:
        schedule_file = os.path.join('certe_fresh', 'NBA_Schedule_2024-25.xlsx')
        if not os.path.exists(schedule_file):
            return None
            
        try:
            df = pd.read_excel(schedule_file, engine='openpyxl')
        except Exception as e:
            return None
        
        # Map the actual column names
        df = df.rename(columns={
            'Game Date': 'Date',
            'Start (ET)': 'Time',
            'Visitor/Neutral': 'Visitor',
            'Home/Neutral': 'Home'
        })
        
        # Convert date and time columns to datetime
        try:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Time'] = df['Time'].apply(parse_game_time)
            df['datetime'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d') + ' ' + df['Time'])
            df['datetime'] = df['datetime'].dt.tz_localize('America/New_York')
        except Exception as e:
            return None
        
        # Get current time
        current_time = datetime.now(pytz.timezone('America/New_York'))
        
        # Find the next game
        next_games = df[df['datetime'] > current_time].sort_values('datetime')
        
        if next_games.empty:
            return None
            
        next_game = next_games.iloc[0]
        game_time = next_game['datetime']
        
        game_info = {
            'countdown': format_countdown(game_time),
            'visitor_team': str(next_game['Visitor']),
            'home_team': str(next_game['Home']),
            'arena': str(next_game['Arena']),
            'game_time': game_time.strftime('%I:%M %p ET'),
            'game_date': game_time.strftime('%A, %B %d, %Y'),
            'start_time': game_time.isoformat()
        }
        return game_info
        
    except Exception as e:
        return None

@app.route('/get_next_game')
def next_game_route():
    game_info = get_next_game()
    if game_info:
        return jsonify(game_info)
    return jsonify({'error': 'No upcoming games found or schedule file missing'})

def format_game_countdown(game_datetime):
    try:
        # Ensure game_datetime is timezone aware
        if game_datetime.tzinfo is None:
            game_datetime = game_datetime.replace(tzinfo=pytz.timezone('America/New_York'))
        
        # Get current time in ET
        current_time = datetime.now(pytz.timezone('America/New_York'))
        
        # Ensure both times are in the same timezone
        if game_datetime.tzinfo != current_time.tzinfo:
            game_datetime = game_datetime.astimezone(current_time.tzinfo)
        
        # Calculate time difference
        try:
            time_diff = game_datetime - current_time
        except Exception as e:
            print(f"Error calculating time difference: {str(e)}")
            return "--:--:--"
        
        # If game is in the past, return "Finished"
        if time_diff.total_seconds() < 0:
            return "Finished"
        
        try:
            # Calculate hours, minutes, and seconds
            total_seconds = int(time_diff.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            # Format as HH:MM:SS
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except Exception as e:
            print(f"Error formatting countdown values: {str(e)}")
            return "--:--:--"
            
    except Exception as e:
        print(f"Error in format_game_countdown: {str(e)}")
        return "--:--:--"

@app.route('/todays_games')
def todays_games_route():
    logging.info("Today's games route hit")
    try:
        schedule_file = os.path.join('uploads', 'NBA_Schedule_2024-25.xlsx')
        if not os.path.exists(schedule_file):
            logging.error(f"Schedule file not found at: {schedule_file}")
            return jsonify({'error': f'Schedule file not found at: {schedule_file}'})
        
        try:
            df = pd.read_excel(schedule_file, engine='openpyxl')
            # Rename columns to match expected names
            df = df.rename(columns={
                'Date': 'date',
                'Start Time (ET)': 'time',
                'Away Team': 'away_team',
                'Home Team': 'home_team'
            })
            
            # Convert date and time to datetime
            df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))
            
            # Filter for today's games
            today = datetime.now(pytz.timezone('America/New_York')).date()
            df['date'] = pd.to_datetime(df['date']).dt.date
            todays_games = df[df['date'] == today].copy()
            
            # Format the output
            games_list = []
            for _, game in todays_games.iterrows():
                game_time = game['datetime'].replace(tzinfo=pytz.timezone('America/New_York'))
                games_list.append({
                    'away_team': game['away_team'],
                    'home_team': game['home_team'],
                    'start_time': game['time'],
                    'countdown': format_countdown(game_time),
                    'tooltip': f"Game starts at {game['time']} ET"
                })
            
            logging.info(f"Found {len(games_list)} games for today")
            return jsonify({'games': games_list})
            
        except Exception as e:
            logging.error(f"Error processing Excel file: {str(e)}")
            return jsonify({'error': f'Error processing Excel file: {str(e)}'})
    
    except Exception as e:
        logging.error(f"Error in todays_games_route: {str(e)}")
        return jsonify({'error': f'Error processing schedule: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Railway's PORT, default to 5000 locally
    app.run(host='0.0.0.0', port=port, debug=False)  # host='0.0.0.0' makes it externally visible 