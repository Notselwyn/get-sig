import sys

def _yield_common_indices(indices: tuple[int], base_arr: bytes, cmp_arr: bytes):
    for index in indices:
        if index >= len(cmp_arr):  # file content ran out
            return

        if base_arr[index] == cmp_arr[index]:
            yield index

def _yield_stacked_common_arr_indices(indices: list[int], base_arr: list[int]) -> tuple[int, tuple[int]]:
    prev = -1
    cnt = 0

    for index in indices:
        if index - prev == 1:  # stack neighbors
            prev = index
            cnt += 1
            continue

        start_offset = prev-cnt+1
        yield (start_offset, bytearray(base_arr[p] for p in range(start_offset, prev+1)))
        
        # reset neighbors
        prev = index
        cnt = 1


def _yield_common_indices_from_files(files, chunk_size: int):
    while True:
        base_chunk: bytes = files[0].read(chunk_size)
        if base_chunk == b"":  # fetch new base?
            return

        same_indices = range(len(base_chunk))

        for f in files[1:]:
            chunk: list[int|None] = f.read(chunk_size)
            if chunk == b"":  # file ran out?
                return

            same_indices = _yield_common_indices(same_indices, base_chunk, chunk)
        
        yield (same_indices, base_chunk)

def generate_raw(filenames: list[str]):
    CHUNK_SIZE = 1 << 19  # 512KiB
    files = [open(fn, "rb") for fn in filenames]

    for p, (common_chunk_indices, base_chunk) in enumerate(_yield_common_indices_from_files(files, CHUNK_SIZE)):
        stacked_common_chunk_bytes = _yield_stacked_common_arr_indices(common_chunk_indices, base_chunk)
        for (stack_start, stack_bytes) in stacked_common_chunk_bytes:
            print(f"{hex(CHUNK_SIZE * p + stack_start)},{hex(len(stack_bytes)*2)},{stack_bytes.hex()}")

def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <file1> [file2] [file3] ...")
        print("stdout: offset (hex),content len (hex),content (hex)")
        exit(1)

    generate_raw(sys.argv[1:])

if __name__ == "__main__":
    main()