import sys

overlap = []

for filename in sys.argv[1:]:
    with open(filename) as f:
        fc = f.read()

    if overlap == []:
        overlap = list(fc)
        continue

    for p, b in enumerate(fc):
        if overlap[p] != b:
            overlap[p] = "█"

overlap_str = "".join(overlap)

print(overlap_str)

# assume xxd output
overlapping_bytes = "".join(x[10:51].replace(" ", "") for x in overlap_str.split("\n"))
print(overlapping_bytes, end="\n\n")

streak_sig = []
for p, c in enumerate(overlapping_bytes[::2]):
    byte = c + overlapping_bytes[p*2+1]

    # only want full bytes
    if "█" in byte:
        if streak_sig != []:
            print(f'memcmp(pud_area + i * 0x1000 + {hex(p - len(streak_sig))}, "\\x' + '\\x'.join(streak_sig) + f'", {len(streak_sig)}) == 0 &&')

        streak_sig = []
        continue
    
    streak_sig.append(byte)