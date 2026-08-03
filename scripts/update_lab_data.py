#!/usr/bin/env python3
"""
Script to automatically update lab data from CyberDefenders and other platforms.
This ensures difficulty, retirement status, and MITRE metadata stay current.
Ratings are NOT scraped -- they are frozen in data/labs.json (see fetch_cyberdefenders_lab).
"""

import json
import re
import requests
from bs4 import BeautifulSoup
import time

def extract_json_from_script(html_content, script_id="contextData"):
    """Extract JSON data from script tag in HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', {'id': script_id, 'type': 'application/json'})
    
    if script_tag:
        try:
            return json.loads(script_tag.string)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from {script_id}")
            return None
    return None

def fetch_cyberdefenders_lab(slug):
    """Fetch lab data from CyberDefenders."""
    url = f"https://cyberdefenders.org/blueteam-ctf-challenges/{slug}/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = extract_json_from_script(response.text)
        
        if data and 'lab' in data:
            lab = data['lab']
            # NOTE: 'rating' is deliberately NOT scraped. CyberDefenders capped new
            # votes at 3 stars while keeping the stored average on the old 0-5 field,
            # and exposes no scale/max in the API. Live values are therefore a blend
            # of /5 and /3 votes that only ever decays -- not comparable over time or
            # between labs. Ratings are frozen in data/labs.json with rating_scale +
            # rating_as_of. See architecture.html "Lab Ratings".
            # CyberDefenders "difficulty" is actually player-rated difficulty
            return {
                'player_difficulty': lab.get('difficulty'),  # This is player-rated!
                'is_retired': lab.get('is_retired', False),
                'tactics': [t['title'] for t in lab.get('tactics', [])],
                'categories': [c['title'] for c in lab.get('categories', [])]
            }
    except Exception as e:
        print(f"Error fetching {slug}: {e}")
    
    return None

def update_lab_metadata():
    """Update metadata for labs in the data file."""
    
    # Define labs to update with their platform and slug
    labs_to_update = {
        'WorkFromHome': {
            'platform': 'cyberdefenders',
            'slug': 'workfromhome'
        },
        'ResourcePacks': {
            'platform': 'cyberdefenders',
            'slug': 'resourcepacks'
        },
        'YARA Trap': {
            'platform': 'cyberdefenders',
            'slug': 'yara-trap'
        },
        'Spooler - APT28': {
            'platform': 'cyberdefenders',
            'slug': 'spooler-apt28'
        },
        'Perfect Survey': {
            'platform': 'cyberdefenders',
            'slug': 'perfect-survey'
        },
        'LFI Escalation': {
            'platform': 'cyberdefenders',
            'slug': 'lfi-escalation'
        },
        'KioskExpo7': {
            'platform': 'cyberdefenders',
            'slug': 'kioskexpo7'
        },
        'RoastToRoot': {
            'platform': 'cyberdefenders',
            'slug': 'roasttoroot'
        },
        'RaaS Unfold - RansomHub': {
            'platform': 'cyberdefenders',
            'slug': 'raas-unfold-ransomhub'
        },
        'Recruiter - Hanoi Op': {
            'platform': 'cyberdefenders',
            'slug': 'recruiter-hanoi-op'
        },
        'CodeFreeze': {
            'platform': 'cyberdefenders',
            'slug': 'codefreeze'
        },
        'Satisfaction': {
            'platform': 'cyberdefenders',
            'slug': 'satisfaction'
        },
        'Penumbra': {
            'platform': 'cyberdefenders',
            'slug': 'penumbra'
        }
    }
    
    updated_data = {}
    
    for lab_name, lab_info in labs_to_update.items():
        print(f"Fetching data for {lab_name}...")
        
        if lab_info['platform'] == 'cyberdefenders':
            metadata = fetch_cyberdefenders_lab(lab_info['slug'])
            
            if metadata:
                updated_data[lab_name] = metadata
                print(f"  [OK] Updated: player_difficulty={metadata.get('player_difficulty')}, retired={metadata.get('is_retired')}")
            else:
                print(f"  [FAIL] Failed to fetch data")
        
        # Be nice to the servers
        time.sleep(2)
    
    # Save to JSON file
    with open('data/labs_metadata.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    print(f"\n[OK] Updated metadata for {len(updated_data)} labs")
    return updated_data

if __name__ == '__main__':
    import os
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    update_lab_metadata()