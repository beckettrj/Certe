from flask import Flask, render_template, request, jsonify, send_from_directory
from pyxlsb import open_workbook
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
DEFAULT_FILE = os.path.join('Certe', 'Efficient Meta Count Certe Beta 1.0.xlsb')
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
            with wb.get_sheet(1) as sheet:
                for row in range(start_row, end_row + 1):
                    row_data = []
                    for col in range(start_col, end_col + 1):
                        cell_value = sheet.read_cell(row, col)
                        row_data.append(str(cell_value.v) if cell_value else '')
                    data.append(row_data)
    else:  # xlsx file
        df = pd.read_excel(filepath)
        for row in range(start_row, end_row + 1):
            row_data = []
            for col in range(start_col, end_col + 1):
                try:
                    value = df.iloc[row, col]
                    row_data.append(str(value) if pd.notna(value) else '')
                except:
                    row_data.append('')
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

@app.route('/Certe/<path:filename>')
def serve_certe_file(filename):
    return send_from_directory('Certe', filename)

if __name__ == '__main__':
    app.run(debug=True) 