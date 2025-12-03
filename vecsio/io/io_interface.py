import struct
import logging
import numpy as np
from pathlib import Path
from numpy.typing import NDArray, DTypeLike

logger = logging.getLogger("vecsio")

ISIZE = int(np.dtype(np.uint32).itemsize)

def read_vecs_meta(path: Path) -> tuple[int, int]:
    file_size = path.stat().st_size
    with open(path, "rb") as f:
        dim_bytes = f.read(ISIZE)
    dim = int(np.frombuffer(dim_bytes, dtype=np.uint32)[0])
    stride = dim + 1
    assert file_size % (stride * ISIZE) == 0, f"Invalid vec file: size={file_size}, dim={dim}"
    count = file_size // (stride * ISIZE)
    return count, dim

def read_vecs(path: Path) -> NDArray[np.generic]:
    _, dim = read_vecs_meta(path)
    stride = dim + 1
    data = np.fromfile(path, dtype=np.uint32)
    data = data.reshape(-1, stride)
    return data[:, 1:]


def write_vecs(path: Path, arr: NDArray[np.generic], dtype: DTypeLike) -> None:
    if path.exists():
        logger.warning(f"Overwriting existing file at {path}")
    arr = arr.astype(dtype)
    n_rows, dim = arr.shape
    with open(path, 'wb') as f:
        for i in range(n_rows):
            f.write(struct.pack('i', dim))
            f.write(arr[i].tobytes())
