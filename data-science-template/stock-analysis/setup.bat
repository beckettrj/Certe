@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
mkdir data
mkdir .cache
echo Setup complete! Run 'venv\Scripts\activate' to activate the environment