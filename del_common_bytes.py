import sys
import os
import mmap

def _yield_common_bytes_from_file(file):
    while True:
        data: bytes = file.readline()
        if data == "":  # fetch new base?
            return
        
        offset_str, _, cb_hex = data.split(",")
        offset = int(offset_str, 16)
        common_bytes = bytes.fromhex(cb_hex)

        yield (offset, common_bytes)

def _get_file_size(file):
    file.seek(0, os.SEEK_END)
    
    return file.tell()

def _is_bytes_in_file_at_offsets(file, increment_size: int, offset: int, common_bytes: bytes):
    increment_amount = _get_file_size(file) // increment_size
    read_len = len(common_bytes)
    for i in range(increment_amount):
        file.seek(increment_size * i + offset, os.SEEK_SET)
        if file.read(read_len) == common_bytes:
            return True

def main(filenames: list[str]):
    INPUT_FILE = open("/dev/stdin")
    PAGE_SIZE = 4096

    # use mmap io for faster lookup
    files = [open(fn, "r+b") for fn in filenames]
    mmaps = [mmap.mmap(f.fileno(), 0) for f in files]

    unique_bytes_offsets_pass: set[tuple[int, bytes]] = dict()
    for offset, common_bytes in _yield_common_bytes_from_file(INPUT_FILE):
        independent_offset = offset % PAGE_SIZE

        # is this offset with this byte already checked?
        combi = (independent_offset, common_bytes)
        if combi in unique_bytes_offsets_pass:
            if unique_bytes_offsets_pass[combi] is True:
                print(f"{hex(offset)},{hex(len(common_bytes))},{common_bytes.hex()}")
            continue
        
        # check each page of each file if this offset with byte matches
        for m in mmaps:
            if _is_bytes_in_file_at_offsets(m, PAGE_SIZE, independent_offset, common_bytes):
                unique_bytes_offsets_pass[combi] = False
                break
        else:
            unique_bytes_offsets_pass[combi] = True
            print(f"{hex(offset)},{hex(len(common_bytes))},{common_bytes.hex()}")


if __name__ == "__main__":
    main(sys.argv[1:])