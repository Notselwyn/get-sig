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
    CHUNK_SIZE = 4096

    best_chunk_total_len = 0
    best_chunk = []
    curr_chunk_total_len = 0
    curr_chunk = []
    prev_chunk_index = -1

    for offset, common_bytes in _yield_common_bytes_from_file(INPUT_FILE):
        chunk_index = offset // CHUNK_SIZE

        if chunk_index == prev_chunk_index:  # same chunk
            curr_chunk_total_len += len(common_bytes)
            curr_chunk.append((offset, common_bytes))
        else: # prev chunk ended
            if curr_chunk_total_len > best_chunk_total_len:
                best_chunk_total_len = curr_chunk_total_len
                best_chunk = curr_chunk

            curr_chunk_total_len = 1
            curr_chunk = [(offset, common_bytes)]

        prev_chunk_index = chunk_index

    for offset, common_bytes in best_chunk:
        print(f"{hex(offset)},{hex(len(common_bytes))},{common_bytes.hex()}")

if __name__ == "__main__":
    main()