#!/usr/bin/env python3
import re
from pathlib import Path

file_path = Path(r'c:\Users\pc\Desktop\peptide 2\index.html')
lines = file_path.read_text(encoding='utf-8').split('\n')

result = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is an img tag with height: 200px
    if '<img src="./image1_files/' in line and 'height: 200px;' in line:
        # Look ahead for the next payment link
        payment_href = None
        for j in range(i + 1, min(i + 5, len(lines))):
            if 'href="payment.html' in lines[j]:
                match = re.search(r'href="([^"]+)"', lines[j])
                if match:
                    payment_href = match.group(1)
                    break
        
        if payment_href:
            # Reduce height from 200 to 160
            new_line = line.replace('height: 200px;', 'height: 160px;')
            new_line = new_line.replace('style="', 'style="cursor: pointer; ')
            
            # Get indentation
            indent = len(line) - len(line.lstrip())
            
            # Create wrapped version
            result.append(' ' * indent + f'<a href="{payment_href}" style="display: block; text-decoration: none;">')
            result.append(new_line)
            result.append(' ' * indent + '</a>')
        else:
            # Just reduce height
            new_line = line.replace('height: 200px;', 'height: 160px;')
            result.append(new_line)
    else:
        result.append(line)
    
    i += 1

new_content = '\n'.join(result)
file_path.write_text(new_content, encoding='utf-8')

# Verify
remaining_200px = len(re.findall(r'height: 200px;', new_content))
resized_to_160 = len(re.findall(r'height: 160px;', new_content))

print(f'✓ Resized {resized_to_160} images to 160px')
print(f'✓ Remaining 200px: {remaining_200px}')
print('✓ Done!')
