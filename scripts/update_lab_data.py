#!/usr/bin/env python3
"""
Script to automatically update lab data from CyberDefenders and other platforms.
This ensures difficulty, retirement status, and MITRE metadata stay current.

Ratings are scraped only for labs released on or after RATING_CAP_DATE -- see
fetch_cyberdefenders_lab for why. Older ones are frozen in data/labs.json.
"""

import json
import re
import requests
from bs4 import BeautifulSoup
import time
from datetime import date

# CyberDefenders capped new lab ratings at 3 stars around this date, while leaving the
# stored average on the old 0-5 field and exposing no scale in the API.
#
# Dated from the rating history in git: the last time any lab's rating rose was
# 2026-06-01, and every observation after it is downward.
#
# Labs released BEFORE this are blends of /5 and /3 votes with no valid divisor. They
# only decay, at a rate set by traffic rather than reception, so they are comparable
# neither over time nor between labs -- those stay frozen in data/labs.json and must
# never be written here, because labs_metadata.json wins the render-time merge.
#
# Labs released AFTER it have no legacy votes mixed in. They sit on a clean 0-3 scale,
# which makes them both meaningful and safely convertible, so they are tracked live.
#
# The date is deliberately a week past the 2026-06-01 inflection, because the changeover
# is not instant: ghostconnect-ta583, released exactly on 2026-06-01, still reads 3.1 --
# impossible on a 3-point scale. It banked 5-point votes in its first days and is a blend.
# 2026-06-15 is the earliest release date observed to be cleanly on the new scale.
RATING_CAP_DATE = '2026-06-15'

# A genuine post-cap rating cannot exceed this. Anything higher proves the lab predates
# the changeover regardless of its release date, so it is skipped rather than mislabelled
# -- writing rating_scale 3 against, say, 3.1 would make score5() return 5.17, above the
# 5-point maximum, and rank the lab above every other lab on the site.
RATING_SCALE_POST_CAP = 3

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
            # CyberDefenders "difficulty" is actually player-rated difficulty
            meta = {
                'player_difficulty': lab.get('difficulty'),  # This is player-rated!
                'is_retired': lab.get('is_retired', False),
                'tactics': [t['title'] for t in lab.get('tactics', [])],
                'categories': [c['title'] for c in lab.get('categories', [])]
            }

            # Rating is tracked only for post-cap labs (see RATING_CAP_DATE). Both values
            # are ISO-8601, so a plain string compare orders them correctly.
            #
            # Two guards, both of which drop the rating rather than publish a wrong one --
            # metadata wins the render-time merge, so a bad value here reaches the site:
            #   - a lab with no votes yet reports 0.0, and a transient zero would blank an
            #     existing rating
            #   - a value above the 3-point maximum means the lab is really a pre-cap blend
            #     whatever its release date says
            released = lab.get('released_at') or ''
            rating = lab.get('rating')
            if released >= RATING_CAP_DATE and rating:
                if rating > RATING_SCALE_POST_CAP:
                    print(f"  [WARN] {slug}: rating {rating} exceeds the {RATING_SCALE_POST_CAP}"
                          f"-point maximum; treating as pre-cap and leaving it unset")
                else:
                    meta['rating'] = rating
                    meta['rating_scale'] = RATING_SCALE_POST_CAP
                    meta['rating_as_of'] = date.today().strftime('%Y-%m')

            return meta
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
                rating_note = (f", rating={metadata['rating']}/3" if 'rating' in metadata
                               else ", rating=frozen")
                print(f"  [OK] Updated: player_difficulty={metadata.get('player_difficulty')}, "
                      f"retired={metadata.get('is_retired')}{rating_note}")
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