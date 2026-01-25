import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_injury_report():
    """Scrapes ESPN injury report and returns DataFrame"""
    espn_url = "https://www.espn.com/nba/injuries"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(espn_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize lists to store data
    player_names = []
    teams = []
    injury_statuses = []
    
    # ESPN organizes injuries by team
    # Find all injury tables
    injury_sections = soup.find_all('div', class_='ResponsiveTable')
    
    for section in injury_sections:
        # Get team name (usually in a header above the table)
        team_header = section.find_previous('div', class_='Table__Title')
        team_name = team_header.get_text(strip=True) if team_header else 'Unknown'
        
        # Find the table body
        tbody = section.find('tbody')
        if not tbody:
            continue
        
        # Get all rows
        rows = tbody.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 4:  # Need at least 4 cells
                player_name = cells[0].get_text(strip=True)
                
                # Status is in cell 3, inside a span tag
                status_cell = cells[3]
                status_span = status_cell.find('span')
                status = status_span.get_text(strip=True) if status_span else status_cell.get_text(strip=True)
                
                player_names.append(player_name)
                teams.append(team_name)
                injury_statuses.append(status)
    
    # Create DataFrame
    injury_df = pd.DataFrame({
    'PLAYER_NAME': player_names,
    'TEAM': teams,
    'INJURY_STATUS': injury_statuses
    })
    
    return injury_df

if __name__ == '__main__':
    injuries = get_injury_report()
    print(f"Found {len(injuries)} injured players")
    print(injuries.head(10))