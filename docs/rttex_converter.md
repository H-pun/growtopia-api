## Growtopia RTTEX Converter

### Unpack RTTEX
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
#### Parameters

The `rttex_unpack` function accepts the following parameters:

- `rttex_file` (file): The RTTEX file that needs to be converted. This is the primary input file for the conversion process.
- `x` (int, optional): The column location of the item.
- `y` (int, optional): The row location of the item.
- `force_opaque` (bool, optional): A flag indicating whether to force the output image to be opaque. If set to `True`, the alpha channel will be ignored, and the image will be fully opaque.

### Built-in Cropper

If you want to directly crop an item based on its `x` and `y` coordinates in `itemsdat`, you can use the following code:

> [!WARNING]
> Only supports 32x32 tiles. For other sizes, you will need to crop manually.

```python
file_path = "path/to/your/file.rttex"
with open(file_path, "rb") as f:
    image = rttex_unpack(f.read(), x=x, y=y)
```

This will directly crop the image to a 32x32 tile at the specified column and row location.

### Pack RTTEX
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
