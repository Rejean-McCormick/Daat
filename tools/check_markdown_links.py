"""Validate relative Markdown links in source docs (not GitHub Wiki aliases)."""
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]
LINK=re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
def main():
    count=0; missing=[]
    for p in ROOT.rglob('*.md'):
        if '/wiki/' in p.as_posix() or '/.git/' in p.as_posix():continue
        for target in LINK.findall(p.read_text(encoding='utf-8')):
            target=target.split('#',1)[0].strip()
            if not target or target.startswith(('https:','http:','mailto:','data:','/')):continue
            count+=1
            loc=(p.parent/target).resolve()
            if not loc.is_relative_to(ROOT) or not (loc.is_file() or loc.is_dir()):
                missing.append((p.relative_to(ROOT).as_posix(),target))
    if missing:
        for path,target in missing:print('Broken link',path,target,file=sys.stderr)
        return 1
    print('Source Markdown relative links validated:',count)
    return 0
if __name__=='__main__':sys.exit(main())
