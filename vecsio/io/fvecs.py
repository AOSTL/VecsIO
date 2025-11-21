import numpy as np
from pathlib import Path
from .io_interface import read_vecs, write_vecs

FVECS_SUFFIX = ".fvecs"

def read_fvecs(path: Path) -> np.typing.NDArray[np.float32]:
    if not path.suffix == FVECS_SUFFIX:
        path = path.with_suffix(FVECS_SUFFIX)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return read_vecs(path, dtype=np.float32).astype(np.float32)

def write_fvecs(path: Path, arr: np.typing.NDArray[np.float32]) -> None:
    if not path.suffix == FVECS_SUFFIX:
        path = path.with_suffix(FVECS_SUFFIX)
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = arr.astype(np.float32).reshape(-1, arr.shape[-1])
    write_vecs(path, arr, dtype=np.float32)