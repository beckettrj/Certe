from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
from datetime import datetime
import pytz

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todays_games')
def todays_games_route():
    try:
        # Look for NBA schedule file in uploads directory
        schedule_file = None
        for file in os.listdir('uploads'):
            if file.startswith('NBA_Schedule') and file.endswith('.xlsx'):
                schedule_file = os.path.join('uploads', file)
                break
                
        if not schedule_file:
            return jsonify({'error': 'NBA Schedule file not found in uploads directory'})
        
        # Read the Excel file
        df = pd.read_excel(schedule_file, engine='openpyxl')
        
        # Map column names
        df = df.rename(columns={
            'Game Date': 'Date',
            'Start (ET)': 'Time',
            'Visitor/Neutral': 'Visitor',
            'Home/Neutral': 'Home'
        })
        
        # Convert date and time
        df['Date'] = pd.to_datetime(df['Date'])
        df['Time'] = df['Time'].apply(lambda x: str(x).strip() if pd.notna(x) else '')
        df['datetime'] = pd.to_datetime(df['Date'].dt.strftime('%Y-%m-%d') + ' ' + df['Time'])
        df['datetime'] = df['datetime'].dt.tz_localize('America/New_York')
        
        # Get current time in ET
        current_time = datetime.now(pytz.timezone('America/New_York'))
        current_date = current_time.date()
        
        # Get today's games
        todays_games = df[df['Date'].dt.date == current_date]
        
        # Format games list
        games_list = []
        for _, game in todays_games.iterrows():
            game_info = {
                'datetime': game['datetime'].isoformat(),
                'start_time': game['Time'],
                'teams': f"{game['Visitor']} @ {game['Home']}",
                'arena': game['Arena'],
                'tooltip': f"Game starts at {game['Time']} ET"
            }
            games_list.append(game_info)
        
        return jsonify({
            'date': current_date.strftime('%A, %B %d, %Y'),
            'games': games_list
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing schedule: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)