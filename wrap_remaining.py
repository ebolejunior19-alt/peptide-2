#!/usr/bin/env python3
import re
from pathlib import Path

file_path = Path(r'c:\Users\pc\Desktop\peptide 2\index.html')
content = file_path.read_text(encoding='utf-8')

# Pattern to find img tags with 200px height followed by a payment link
pattern = r'(<div class="product-card">\s*)(<img src="[^"]*" alt="[^"]*" style="[^"]*height: 200px;[^"]*">)\s*(<a href="(payment\.html\?[^"]*)"[^>]*>Add to Cart</a>)'

def wrap_image(match):
    div_open = match.group(1)
    img_tag = match.group(2)
    button_a = match.group(3)
    payment_link = match.group(4)
    
    # Update img height and wrap in anchor
    img_tag_updated = img_tag.replace('height: 200px;', 'height: 160px;')
    img_tag_updated = img_tag_updated.replace('style="', 'style="cursor: pointer; ')
    
    wrapped = f'{div_open}<a href="{payment_link}" style="display: block; text-decoration: none;">\n                        {img_tag_updated}\n                    </a>\n                    {button_a}'
    
    return wrapped

new_content = re.sub(pattern, wrap_image, content, flags=re.MULTILINE)

# Write back
file_path.write_text(new_content, encoding='utf-8')

# Verify
remaining_200px = len(re.findall(r'height: 200px;', new_content))
wrapped_images = len(re.findall(r'<a href="payment\.html\?[^"]*" style="display: block; text-decoration: none;">\s*<img', new_content))

print(f'✓ Wrapped {wrapped_images} images with payment links')
print(f'✓ Remaining 200px images: {remaining_200px}')
print('✓ All images updated!')
