import re
from pathlib import Path

file_path = Path(r'c:\Users\pc\Desktop\peptide 2\index.html')
content = file_path.read_text(encoding='utf-8')

# Step 1: Replace all height: 200px with height: 160px
content = content.replace('height: 200px;', 'height: 160px;')

# Step 2: For each img tag, find the next payment link and wrap the img
lines = content.split('\n')
result = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this line contains an img tag with image1_files
    if '<img src="./image1_files/' in line and 'payment.html' not in line:
        # Look ahead for the payment link (usually within next 3-4 lines)
        payment_href = None
        for j in range(i + 1, min(i + 5, len(lines))):
            href_match = re.search(r'href="(payment\.html\?[^"]*)"', lines[j])
            if href_match:
                payment_href = href_match.group(1)
                break
        
        if payment_href:
            # Wrap the img tag with an anchor
            indentation = len(line) - len(line.lstrip())
            wrapped_line = ' ' * indentation + f'<a href="{payment_href}" style="display: block; text-decoration: none; cursor: pointer;">'
            result.append(wrapped_line)
            result.append(line)
            result.append(' ' * indentation + '</a>')
        else:
            result.append(line)
    else:
        result.append(line)
    
    i += 1

new_content = '\n'.join(result)
file_path.write_text(new_content, encoding='utf-8')

# Verify changes
clickable_count = len(re.findall(r'<a href="payment\.html\?[^"]*" style="display: block; text-decoration: none; cursor: pointer;"><img', new_content))
height_160_count = len(re.findall(r'height: 160px;', new_content))

print(f'✓ Made {clickable_count} images clickable')
print(f'✓ Resized {height_160_count} images to 160px')
print('✓ All images now link to payment page!')
