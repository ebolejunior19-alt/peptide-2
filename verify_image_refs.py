import re, glob
from pathlib import Path

root = Path(r'c:\Users\pc\Desktop\peptide 2')
image1 = root / 'image1_files'
refs = set()
for p in glob.glob(str(root / '*.html')) + glob.glob(str(root / '*.js')) + glob.glob(str(root / '*.css')):
    txt = Path(p).read_text(encoding='utf-8', errors='ignore')
    refs.update(re.findall(r'image1_files/([^"\'\s>]+)', txt))

missing = []
for r in sorted(refs):
    if not (image1 / r).exists():
        missing.append(r)

print('total_refs', len(refs))
print('missing_count', len(missing))
for m in missing:
    print(m)
