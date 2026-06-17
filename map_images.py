from pathlib import Path
import re, shutil, glob

root = Path(r"c:\Users\pc\Desktop\peptide 2")
images_dir = root / 'images'
image1_dir = root / 'image1_files'
image1_dir.mkdir(exist_ok=True)

def collect_refs():
    refs = set()
    patterns = ['*.html','*.js','*.css']
    for pat in patterns:
        for p in glob.glob(str(root / pat)):
            try:
                txt = Path(p).read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            refs.update(re.findall(r'image1_files/([^"\'\s>)+]+)', txt))
            refs.update(re.findall(r"image1_files/([^\"\'\s>]+)", txt))
    return refs

def build_candidate_map():
    if not images_dir.exists():
        return {}
    cmap = {}
    for f in images_dir.iterdir():
        if f.is_file():
            cmap[f.name.lower()] = f
    return cmap

def main():
    refs = collect_refs()
    cmap = build_candidate_map()
    fallback = images_dir / 'image.jpg'
    if not fallback.exists():
        # pick any png/jpg in images as fallback
        for e in ['image.png','image_1.jpg']:
            if (images_dir / e).exists():
                fallback = images_dir / e
                break

    created = []
    missing = []
    for name in refs:
        target = image1_dir / name
        if target.exists():
            continue
        lname = name.lower()
        if lname in cmap:
            shutil.copy2(cmap[lname], target)
            created.append(name)
            continue
        # try matching by basename without extension
        base = Path(name).stem.lower()
        found = None
        for k,f in cmap.items():
            if base in k:
                found = f
                break
        if found:
            shutil.copy2(found, target)
            created.append(name)
            continue
        if fallback.exists():
            shutil.copy2(fallback, target)
            created.append(name)
        else:
            missing.append(name)

    print('created_count', len(created))
    if missing:
        print('missing_count', len(missing))
        for m in missing:
            print(m)
    else:
        print('all references satisfied')

if __name__ == '__main__':
    main()
