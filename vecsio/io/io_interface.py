import struct
import logging
import numpy as np
from pathlib import Path
from numpy.typing import NDArray, DTypeLike
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("vecsio")

ISIZE = np.dtype(np.uint32).itemsize
CHUNK_BYTES = 1024 * 1024 * 1024  # 1 GB

def read_vecs_meta(path: Path) -> tuple[int, int]:
    file_size = path.stat().st_size
    dim = np.fromfile(path, dtype=np.uint32, count=1)[0]
    stride = dim + 1
    assert file_size % (stride * ISIZE) == 0, f"Invalid vec file: size={file_size}, dim={dim}"
    count = file_size // (stride * ISIZE)
    return count, dim

def read_vecs_parallel(path: Path, dtype: DTypeLike) -> NDArray[np.generic]:
    rows, dim = read_vecs_meta(path)
    stride = dim + 1
    chunk_size = CHUNK_BYTES // (stride * ISIZE)

    def read_chunk(arg: tuple[int, int]) -> NDArray[np.generic]:
        start_idx, end_idx = arg
        offset = start_idx * stride * ISIZE
        count = (end_idx - start_idx) * stride
        with open(path, 'rb') as f:
            f.seek(offset)
            data = np.fromfile(f, dtype=np.uint32, count=count)
        data = data.reshape(-1, stride)
        return data[:, 1:].astype(dtype)

    chunks = [(i, min(i + chunk_size, rows)) for i in range(0, rows, chunk_size)]
    results = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(read_chunk, chunks))

    return np.vstack(results)

def read_vecs(path: Path, dtype: DTypeLike) -> NDArray[np.generic]:
    rows, dim = read_vecs_meta(path)
    stride = dim + 1
    if rows * stride * ISIZE > CHUNK_BYTES:
        return read_vecs_parallel(path, dtype)
    data = np.fromfile(path, dtype=np.uint32)
    data = data.reshape(-1, stride)
    return data[:, 1:].astype(dtype)


def write_vecs(path: Path, arr: NDArray[np.generic], dtype: DTypeLike) -> None:
    if path.exists():
        logger.warning(f"Overwriting existing file at {path}")
    arr = arr.astype(dtype)
    n_rows, dim = arr.shape
    with open(path, 'wb') as f:
        for i in range(n_rows):
            f.write(struct.pack('i', dim))
            f.write(arr[i].tobytes())
