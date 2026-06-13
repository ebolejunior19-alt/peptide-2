#!/usr/bin/env python3
import re
from pathlib import Path

file_path = Path(r'c:\Users\pc\Desktop\peptide 2\index.html')
content = file_path.read_text(encoding='utf-8')

# Remove all $1< artifacts
content = content.replace('$1<a', '<a')
content = content.replace('$1<h4', '<h4')
content = content.replace('$1<div', '<div')

# Write back
file_path.write_text(content, encoding='utf-8')
print("Cleaned all $1 artifacts")
