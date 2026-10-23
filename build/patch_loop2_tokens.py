# Loop 2.0 tokens on the funnel pages (same values as _funnel_build/build_site.py CSS). Run: python3 _funnel_build/patch_loop2_tokens.py <files...>
import sys,re
OLD="--bg:#ffffff; --hero:#f6f6ff; --foot:#f4f4f4; --ink:#2a2a2a; --ink-2:#363636; --body:#505454; --muted:#8a8f8f; --line:#eeeeee;\n  --navy:#313e72; --navy-dark:#26315c; --teal:#33c1b1; --teal-soft:#e6f7f5; --wa:#25d366;"
NEW="--bg:#ffffff; --hero:#f2f9f8; --foot:#fbfaf8; --ink:#14202b; --ink-2:#2b3a48; --body:#4f5d6a; --muted:#8593a0; --line:#e6ecec;\n  --navy:#0f2a3a; --navy-dark:#163b50; --teal:#2fb8ab; --teal-soft:#e3f6f3; --wa:#25d366;"
for f in sys.argv[1:]:
    s=open(f).read(); assert s.count(OLD)==1,(f,s.count(OLD)); s=s.replace(OLD,NEW,1)
    s=s.replace(".card{background:#fff;border:1px solid var(--line);border-radius:20px;padding:20px}",".card{background:#fff;border:1px solid var(--line);border-radius:24px;padding:22px}",1)
    s=s.replace("label.drop{display:block;border:2px dashed var(--teal);border-radius:20px;","label.drop{display:block;border:2px dashed var(--teal);border-radius:24px;",1)
    open(f,'w').write(s); print('tokens patched',f)
