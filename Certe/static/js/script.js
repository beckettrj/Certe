function loadData() {
    const scheduleDiv = document.getElementById('schedule');
    
    // Fetch today's games
    fetch('/todays_games')
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                console.error('Error:', result.error);
                return;
            }
            displayGames(result);
        })
        .catch(error => console.error('Error:', error));
}

function displayGames(data) {
    const scheduleDiv = document.getElementById('schedule');
    
    // Add date header
    const dateHeader = document.createElement('h2');
    dateHeader.textContent = data.date;
    dateHeader.className = 'schedule-date';
    
    // Create table
    const table = document.createElement('table');
    table.className = 'games-table';
    
    // Add header row
    const headerRow = document.createElement('tr');
    ['Countdown', 'Teams', 'Arena'].forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);
    
    // Add game rows
    data.games.forEach(game => {
        const row = document.createElement('tr');
        row.className = 'game-row';
        row.setAttribute('data-tooltip', game.tooltip);
        
        // Countdown cell
        const countdownCell = document.createElement('td');
        countdownCell.className = 'countdown';
        countdownCell.dataset.startTime = game.datetime;
        row.appendChild(countdownCell);
        
        // Teams cell
        const teamsCell = document.createElement('td');
        teamsCell.className = 'teams';
        teamsCell.textContent = game.teams;
        row.appendChild(teamsCell);
        
        // Arena cell
        const arenaCell = document.createElement('td');
        arenaCell.className = 'game-arena';
        arenaCell.textContent = game.arena;
        row.appendChild(arenaCell);
        
        table.appendChild(row);
    });
    
    // Clear and update schedule div
    scheduleDiv.innerHTML = '';
    scheduleDiv.appendChild(dateHeader);
    scheduleDiv.appendChild(table);
    
    // Start countdown updates
    updateCountdowns();
    if (!window.countdownInterval) {
        window.countdownInterval = setInterval(updateCountdowns, 1000);
    }
}

function updateCountdowns() {
    document.querySelectorAll('.countdown').forEach(countdown => {
        const startTime = new Date(countdown.dataset.startTime);
        const now = new Date();
        const diff = startTime - now;
        
        if (diff < 0) {
            countdown.textContent = 'Started';
            countdown.classList.add('started');
            return;
        }
        
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        countdown.textContent = days > 0 
            ? `${days}d ${hours}h ${minutes}m`
            : `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    });
}

// Load games when page loads
document.addEventListener('DOMContentLoaded', loadData);
