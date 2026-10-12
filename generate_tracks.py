#!/usr/bin/env python3
"""Generate tracks.js manifest from the audio folder."""
import os
import json
import re

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')

def main():
    tracks = {}
    
    for root, dirs, files in os.walk(AUDIO_DIR):
        for f in sorted(files):
            if not f.endswith('.mp3'):
                continue
            rel_path = os.path.relpath(os.path.join(root, f), AUDIO_DIR)
            parts = rel_path.replace('\\', '/').split('/')
            if len(parts) < 3:
                continue
            category = parts[0]
            cd = parts[1]
            filename = parts[2]
            
            # Clean up title
            title = filename.replace('.mp3', '')
            m = re.match(r'^(\d+)\s*-\s*(.+)$', title)
            if m:
                title = m.group(2)
            
            # Use forward slashes for URL
            src = rel_path.replace('\\', '/')
            
            key = f'{category}/{cd}'
            if key not in tracks:
                tracks[key] = []
            tracks[key].append({'title': title, 'src': src})
    
    # Sort tracks within each CD
    for key in tracks:
        tracks[key].sort(key=lambda x: x['title'])
    
    # Sort CD keys
    sorted_tracks = dict(sorted(tracks.items()))
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracks.js')
    with open(output_path, 'w', encoding='utf-8') as fp:
        fp.write('// Auto-generated track manifest\n')
        fp.write('const TRACKS = ' + json.dumps(sorted_tracks, ensure_ascii=False, indent=2) + ';\n')
    
    total = sum(len(v) for v in sorted_tracks.values())
    print(f'Generated {output_path}: {len(sorted_tracks)} CDs, {total} tracks')

if __name__ == '__main__':
    main()
