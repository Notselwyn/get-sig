def _yield_common_bytes_from_file(file):
    while True:
        data: bytes = file.readline()
        if data == "":  # fetch new base?
            return
        
        offset_str, _, cb_hex = data.split(",")
        offset = int(offset_str, 16)
        common_bytes = bytes.fromhex(cb_hex)

        yield (offset, common_bytes)

def main():
    INPUT_FILE = open("/dev/stdin")

    for offset, common_bytes in _yield_common_bytes_from_file(INPUT_FILE):
        byte_str = "\\x" + '\\x'.join(f"{b:02x}" for b in common_bytes)
        print(f'memcmp(addr + {hex(offset)}, "{byte_str}", {len(common_bytes)}) == 0 &&')

if __name__ == "__main__":
    main()