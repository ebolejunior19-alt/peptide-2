import re, glob
from pathlib import Path
root = Path(r'c:\Users\pc\Desktop\peptide 2')
pattern = re.compile(r"(\.|\")?\/?image1_files\/([^\"'\s>]+?\.(?:jpg|jpeg|png|webp|svg|gif))", re.IGNORECASE)
files = glob.glob(str(root / '*.html')) + glob.glob(str(root / '*.js')) + glob.glob(str(root / '*.css'))
updated_files = []
for fp in files:
    p = Path(fp)
    txt = p.read_text(encoding='utf-8', errors='ignore')
    new_txt, n = pattern.subn(lambda m: (m.group(1) or '') + '/images/' + m.group(2), txt)
    if n:
        p.write_text(new_txt, encoding='utf-8')
        updated_files.append((p.relative_to(root), n))

print('updated', len(updated_files), 'files')
for f,n in updated_files:
    print(f, n)
