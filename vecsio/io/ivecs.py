import numpy as np
from pathlib import Path
from .io_interface import read_vecs, write_vecs

IVECS_SUFFIX = ".ivecs"

def read_ivecs(path: Path | str, append_suffix: bool = True) -> np.typing.NDArray[np.int32]:
    if isinstance(path, str):
        path = Path(path)
    if append_suffix and not path.suffix == IVECS_SUFFIX:
        path = path.with_suffix(IVECS_SUFFIX)
    if not path.exists():
        raise FileNotFoundError(f"No such file: '{path.name}'")
    return read_vecs(path).view(np.int32)

def write_ivecs(path: Path | str, arr: np.typing.NDArray[np.int32], append_suffix: bool = True) -> None:
    if isinstance(path, str):
        path = Path(path)
    if append_suffix and not path.suffix == IVECS_SUFFIX:
        path = path.with_suffix(IVECS_SUFFIX)
    path.parent.mkdir(parents=True, exist_ok=True)
    arr = arr.view(np.int32).reshape(-1, arr.shape[-1])
    write_vecs(path, arr, np.int32)