import sys
from perf import Router, check, bridge_chains, hname
from design import build
from manual import apply
from route import ascii_map

d = build()
pe = d.check_placement()
r = Router(d)
errs = apply(r)
print('placement:', pe)
print('route errors:', len(errs))
for e in errs:
    print('  ', e)
print('check:', check(d, r.wires))
w = r.wires
print(f'bridges {len(w.bridges)} top {len(w.tops)} jumps {len(w.jumps)}')
print('chains >5:', [c for c in bridge_chains(w) if c[1] > 5])
print(ascii_map(d, r))
