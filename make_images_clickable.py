#!/usr/bin/env python3
"""
Make product images clickable (link to payment page) and reduce their size
"""
import re
from pathlib import Path

file_path = Path(r'c:\Users\pc\Desktop\peptide 2\index.html')
content = file_path.read_text(encoding='utf-8')

# First, reduce image height from 200px to 160px
content = content.replace('height: 200px;', 'height: 160px;')

# Extract all payment links to map them to their images
# Find patterns like: <img ...> followed by <a href="payment.html?...">
pattern = r'<img src="([^"]+)" alt="([^"]+)"[^>]*?style="([^"]*)">\s*<a href="(payment\.html\?[^"]+)"'

# Function to create wrapped image
def wrap_image(match):
    src = match.group(1)
    alt = match.group(2)
    style = match.group(3)
    link = match.group(4)
    
    # Add cursor: pointer to make it obvious it's clickable
    style_with_cursor = style.replace('height: 160px;', 'height: 160px;')
    
    return f'<a href="{link}" style="display: block; text-decoration: none; cursor: pointer;"><img src="{src}" alt="{alt}" style="{style}"></a>\n                    <a href="{link}"'

# Apply the wrapping
new_content = re.sub(pattern, wrap_image, content, flags=re.MULTILINE)

# Verify the replacement worked
if len(re.findall(r'<a href="payment\.html\?', new_content)) > len(re.findall(r'<a href="payment\.html\?', content)):
    file_path.write_text(new_content, encoding='utf-8')
    
    # Count results
    image_links = len(re.findall(r'<a href="payment\.html\?[^"]*"[^>]*><img', new_content))
    total_payment_links = len(re.findall(r'<a href="payment\.html\?', new_content))
    height_160 = len(re.findall(r'height: 160px;', new_content))
    
    print(f"✓ Images made clickable: {image_links}")
    print(f"✓ Total payment links: {total_payment_links}")
    print(f"✓ Images resized to 160px: {height_160}")
    print("✓ File updated successfully!")
else:
    print("Regex replacement approach not working, trying simpler method...")
    
    # Simple replacement approach
    content = file_path.read_text(encoding='utf-8')
    content = content.replace('height: 200px;', 'height: 160px;')
    
    # Replace pattern: <img ...> with <a href="..."><img ...></a>
    # This is more straightforward
    pattern = r'(<img src="[^"]*" alt="[^"]*" style="[^"]*height: 160px;[^"]*">)\s*(\n\s*<a href="payment\.html\?[^"]*")'
    replacement = r'<a href="\2" style="display: block; text-decoration: none; cursor: pointer;">\1</a>\2'
    
    # More reliable: just wrap img in a with the next link's href
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this line has an img tag
        if '<img' in line and 'image1_files' in line:
            # Get the payment link from the next meaningful line
            j = i + 1
            while j < len(lines) and '<a href="payment.html' not in lines[j]:
                j += 1
            if j < len(lines):
                # Extract href from the <a> tag
                href_match = re.search(r'href="([^"]+)"', lines[j])
                if href_match:
                    href = href_match.group(1)
                    # Wrap the img tag with an <a> tag
                    new_line = line.replace('<img', f'<a href="{href}" style="display: block; text-decoration: none; cursor: pointer;"><img').replace('>', ' style="cursor: pointer; transition: opacity 0.2s;">></a>')
                    # Actually, let me do this more carefully
                    new_line = f'<a href="{href}" style="display: block; text-decoration: none;">{line.rstrip()}</a>'
                    new_lines.append(new_line)
                    i += 1
                    continue
        new_lines.append(line)
        i += 1
    
    new_content = '\n'.join(new_lines)
    file_path.write_text(new_content, encoding='utf-8')
    print("✓ File updated with simpler approach")
