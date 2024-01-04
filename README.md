# get-sig

Quick n' dirty Python script to generate signatures of data, by extracting common bytes at common addresses. 

## usage

The usage from `get-sig` is quite simple. Just provide xxd samples to generate signatures from. 
The repository has example samples for the first bytes of the code segment of recent Linux kernels at runtime and at rest.
In order to generate a signature of these overlapping bytes, we run:

```bash
$ python3 main.py samples/*
[*] overlap in original data:
00200000: 488d 2551 3f█0 0█48 8d3d f2ff ffff b901  H.%Q?█.H.=......
00200010: 0100 c048 8b05 █e██ ██0█ 48c7 c200 0000  ...H..███.H.....
00200020: 8█48 29d0 4801 f848 89c2 48c1 ea20 0f30  .H).H..H..H.. .0
00200030: 56e8 █a0█ 0000 5e██ ████ ████ ████ ██0█  V.█...^█.██...█.
00200040: 5███ ██48 8███ ████ ████ ████ ██e8 █e0█  ██.H..█.█████...
00200050: 0000 488d 3da7 ffff ff56 e8█1 0█00 005e  ..H.=....V.....^
00200060: 48██ █0█0 ████ ███b ███f ███0 0000 0000  H..███..........
00200070: e8█b 0000 0048 8b04 25█8 ████ 8█48 ███0  .....H..%███.H..
00200080: █0██ ██0█ ████ ████ ████ ████ █000 00██  .█..██..██......
00200090: ████ ████ 0███ ████ ████ ████ ████ ████  ████.███.███....
002000a0: 0█0█ ████ ████ ████ ████ ████ █8██ ████  ..████.███████..

[*] stripping data from xxd format:
488d25513f█00█488d3df2ffffffb9010100c0488b05█e████0█48c7c20000008█4829d04801f84889c248c1ea200f3056e8█a0█00005e████████████████0█5█████488█████████████████e8█e0█0000488d3da7ffffff56e8█10█00005e48███0█0███████b███f███000000000e8█b000000488b0425█8████8█48███0█0████0██████████████████00000██████████0███████████████████████0█0██████████████████████8██████

[*] generating memcmp() for signature:
memcmp(pud_area + i * 0x1000 + 0x0, "\x48\x8d\x25\x51\x3f", 5) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x7, "\x48\x8d\x3d\xf2\xff\xff\xff\xb9\x01\x01\x00\xc0\x48\x8b\x05", 15) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x1a, "\x48\xc7\xc2\x00\x00\x00", 6) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x21, "\x48\x29\xd0\x48\x01\xf8\x48\x89\xc2\x48\xc1\xea\x20\x0f\x30\x56\xe8", 17) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x34, "\x00\x00\x5e", 3) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x43, "\x48", 1) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x4d, "\xe8", 1) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x50, "\x00\x00\x48\x8d\x3d\xa7\xff\xff\xff\x56\xe8", 11) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x5d, "\x00\x00\x5e\x48", 4) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x6c, "\x00\x00\x00\x00\xe8", 5) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x72, "\x00\x00\x00\x48\x8b\x04\x25", 7) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x7d, "\x48", 1) == 0 &&
memcmp(pud_area + i * 0x1000 + 0x8d, "\x00\x00", 2) == 0 &&
```
