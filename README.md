# VecsIO

**VecsIO** is a lightweight Python library designed for efficient reading and writing of vector data files (commonly used in vector search benchmarks like `.fvecs`, `.ivecs`, etc.).

## Features

- **Efficient I/O**: Fast reading and writing of binary vector formats.
- **User Friendly**: Quickly get started with encapsulated interfaces.
- **Metadata Inspection**: Quickly retrieve the number of vectors and dimensions without loading the entire file.
- **NumPy Integration**: Seamlessly works with NumPy arrays.

## File Format

The library handles the standard vector file format where each vector is preceded by its dimension as a 4-byte integer.
The format is commonly used in vector search benchmarks with file extension like `.fvecs` and `.ivecs`.

Structure: `[dim][vector_data][dim][vector_data]...`

## Usage

### Reading Vectors

```python
from pathlib import Path
import numpy as np
from vecsio.io.io_interface import read_vecs, read_vecs_meta

file_path = Path("data.ivecs")

# Get metadata (count, dimension)
count, dim = read_vecs_meta(file_path)
print(f"Count: {count}, Dimension: {dim}")

# Read vectors into a NumPy array
data = read_vecs(file_path, dtype=np.int32)
print(data.shape)
```

### Writing Vectors

```python
from pathlib import Path
import numpy as np
from vecsio.io.io_interface import write_vecs

# Create dummy data
data = np.random.randint(0, 100, size=(1000, 128)).astype(np.int32)
output_path = Path("output.ivecs")

# Write to file
write_vecs(output_path, data, dtype=np.int32)
```
