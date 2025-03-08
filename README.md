# SLViewer

A web-based viewer for XLSX and XLSB files with customizable cell range selection and background image support.

## Features

- View specific cell ranges from Excel files (XLSX/XLSB)
- Default file support from a specified directory
- Custom file upload capability
- Configurable grid display with background image
- Clean, modern interface with semi-transparent elements

## Prerequisites

- Python 3.8 or higher
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/beckettrj/SLViewer.git
   cd SLViewer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create required directories:
   ```bash
   mkdir -p Certe templates static
   ```

4. Place required files:
   - Put your Excel files in the `Certe` folder
   - Put your background image in the `Certe` folder

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Use the interface to:
   - Select between default or custom file
   - Specify cell range to view
   - View the data with custom background

## File Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/         
│   └── index.html     # Web interface template
└── Certe/             # Default directory for Excel files
    ├── your-excel-file.xlsx
    └── background-image.webp
```

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 