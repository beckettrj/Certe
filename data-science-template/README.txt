Data Science Template Project
===========================

Installation Instructions
------------------------

There are two ways to install the required dependencies:

1. Direct pip install from requirements.txt:
   ```
   pip install -r requirements.txt
   ```

2. Install each package individually:
   ```
   pip install pandas>=1.3.0
   pip install matplotlib>=3.4.0
   pip install yfinance>=0.2.0
   pip install numpy>=1.21.0
   pip install seaborn>=0.11.0
   pip install pytest>=6.2.0
   pip install python-dotenv>=0.19.0
   pip install setuptools>=58.0.4
   pip install wheel>=0.37.0
   pip install pip>=21.3.1
   ```

Note: It's recommended to use a virtual environment before installing dependencies.
To create and activate a virtual environment:

On Windows:
```
python -m venv venv
venv\Scripts\activate
```

On Linux/Mac:
```
python -m venv venv
source venv/bin/activate
```

PATH Configuration
----------------
After installation, some Python packages may install scripts to:
`C:\Users\<username>\AppData\Roaming\Python\Python3xx\Scripts`

To add this to your PATH on Windows:
1. Open System Properties (Win + Pause/Break)
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", find and select "Path"
5. Click "Edit"
6. Click "New"
7. Add the path: `C:\Users\becke\AppData\Roaming\Python313\Scripts`
8. Click "OK" to close all dialogs

This ensures you can use tools like f2py.exe and numpy-config.exe from any terminal.

Running the Project
-----------------
To run the main analysis pipeline:

```
cd C:\Users\becke\StarLogic\data-science-template
python src/main.py
```

For specific analysis modules:
```
cd C:\Users\becke\StarLogic\data-science-template
python src/analysis/[module_name].py
```

To run tests:
```
cd C:\Users\becke\StarLogic\data-science-template
pytest tests/
```

To run a specific test file:
```
cd C:\Users\becke\StarLogic\data-science-template
pytest tests/test_[module_name].py

cd scripts
streamlit run app.py
```
