from pathlib import Path

# Read the downloaded HTML
source_file = Path(r'C:\Users\pc\Downloads\image 3.html')
target_file = Path(r'C:\Users\pc\Desktop\peptide 2\index.html')

print(f"Reading source: {source_file}")
html_content = source_file.read_text(encoding='utf-8', errors='replace')

print(f"Replacing asset paths...")
# Replace all "./image 3_files/" with "./image1_files/"
html_content = html_content.replace('./image 3_files/', './image1_files/')

print(f"Writing to target: {target_file}")
target_file.write_text(html_content, encoding='utf-8')

print(f"File size: {len(html_content)} bytes")
print("Done! index.html has been updated with all images and content.")
