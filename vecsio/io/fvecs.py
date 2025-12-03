import numpy as np
from pathlib import Path
from .io_interface import read_vecs, write_vecs

FVECS_SUFFIX = ".fvecs"

def read_fvecs(path: Path | str, append_suffix: bool = True) -> np.typing.NDArray[np.float32]:
    if isinstance(path, str):
        path = Path(path)
    if append_suffix and not path.suffix == FVECS_SUFFIX:
        path = path.with_suffix(FVECS_SUFFIX)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return read_vecs(path).view(np.float32)

def write_fvecs(path: Path | str, arr: np.typing.NDArray[np.float32], append_suffix: bool = True) -> None:
    if isinstance(path, str):
        path = Path(path)
    if append_suffix and not path.suffix == FVECS_SUFFIX:
        path = path.with_suffix(FVECS_SUFFIX)
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = arr.view(np.float32).reshape(-1, arr.shape[-1])
    write_vecs(path, arr, dtype=np.float32)