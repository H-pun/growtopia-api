### Growtopia RTTEX Converter

To convert Growtopia's `.rttex` file into a PNG format, use the following example:

```python
from growtopia.rttex_converter import rttex_unpack

file_path = "path/to/your/file.rttex"

with open(file_path, "rb") as rttex_file:
    unpacked_png = rttex_unpack(rttex_file)
    output_path = file_path.replace(".rttex", ".png")
    with open(output_path, "wb") as f:
        f.write(unpacked_png)
print(f"Unpacked PNG saved to {output_path}")
```

To convert a PNG image back to an `.rttex` file, use this example:

```python
from growtopia.rttex_converter import rttex_pack

file_path = "path/to/your/file.png"

with open(file_path, "rb") as png_file:
    packed_data = rttex_pack(png_file)
    output_path = file_path.replace(".png", ".rttex")
    with open(output_path, "wb") as f:
        f.write(packed_data)
print(f"Packed RTTEX saved to {output_path}")
```