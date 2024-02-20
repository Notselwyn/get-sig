# get-sig

Quick n' dirty Python script to generate signatures of data, by extracting common bytes at common addresses. 

## usage

The usage from `get-sig` is quite simple. Just provide some sample blobs to use.
In order to generate a memcmp statement for a signature of Linux kernel memory which do not match with userland pages, we run:

```python
$ time python3 get_common_bytes.py samples/kernel_runtime_1/* | python3 del_common_bytes.py samples/nonkernel_runtime_1/* | python3 convert_to_memcmp.py 
memcmp(pud_area + 0x0, "\x48\x8d\x25\x51\x3f", 5) == 0 &&
memcmp(pud_area + 0x7, "\x48\x8d\x3d\xf2\xff\xff\xff\xb9\x01\x01\x00\xc0\x48\x8b\x05", 15) == 0 &&
memcmp(pud_area + 0x1a, "\x48\xc7\xc2\x00\x00", 5) == 0 &&
memcmp(pud_area + 0x21, "\x48\x29\xd0\x48\x01\xf8\x48\x89\xc2\x48\xc1\xea\x20\x0f\x30\x56\xe8", 17) == 0 &&
memcmp(pud_area + 0x34, "\x00\x00\x5e\x6a\x10\x48\x8d\x05\x03\x00\x00\x00\x50\x48\xcb\x48\x89\xf7\x56\xe8", 20) == 0 &&
memcmp(pud_area + 0x4c, "\x5e\xe8", 2) == 0 &&
memcmp(pud_area + 0x50, "\x00\x00\x48\x8d\x3d\xa7\xff\xff\xff\x56\xe8", 11) == 0 &&
memcmp(pud_area + 0x5c, "\x02\x00\x00\x5e\x48", 5) == 0 &&
memcmp(pud_area + 0x72, "\x00\x00\x00\x48\x8b\x04\x25", 7) == 0 &&
memcmp(pud_area + 0x2ea, "\x45\x31", 2) == 0 &&
memcmp(pud_area + 0x2ed, "\x45\x31", 2) == 0 &&
memcmp(pud_area + 0x2f0, "\x45\x31", 2) == 0 &&
memcmp(pud_area + 0x2f3, "\x45\x31", 2) == 0 &&
memcmp(pud_area + 0x5f324f, "\x00\x0f\x1f\x44\x00\x00", 6) == 0 &&
python3 get_common_bytes.py samples/kernel_runtime_1/*  1.42s user 0.06s system 99% cpu 1.480 total
python3 del_common_bytes.py samples/nonkernel_runtime_1/*  0.14s user 0.01s system 9% cpu 1.484 total
python3 convert_to_memcmp.py  0.01s user 0.01s system 0% cpu 1.486 total
```
