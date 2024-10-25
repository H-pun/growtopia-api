import struct
import zlib
from PIL import Image
from io import BytesIO

def get_lowest_power_of_2(n):
    lowest = 1
    while lowest < n:
        lowest <<= 1
    return lowest

def rttex_pack(file: bytes) -> BytesIO:
    # Read and process the PNG image using Pillow & BytesIO
    with BytesIO(file) as byte_stream:    
        with Image.open(byte_stream) as img:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            width, height = img.size
            img_raw = img.convert("RGBA").tobytes()  # Use raw RGBA bytes for consistency

    # Create the RTTEX Header (124 bytes)
    rttex_header = bytearray(124)
    rttex_header[:6] = b"RTTXTR"
    
    struct.pack_into('<I', rttex_header, 8, get_lowest_power_of_2(height))
    struct.pack_into('<I', rttex_header, 12, get_lowest_power_of_2(width))
    struct.pack_into('<I', rttex_header, 16, 5121)  # Format (GL_UNSIGNED_BYTE)
    struct.pack_into('<I', rttex_header, 20, height)
    struct.pack_into('<I', rttex_header, 24, width)
    rttex_header[28] = 1  # Channels
    rttex_header[29] = 0  # Padding
    struct.pack_into('<I', rttex_header, 32, 1)  # Mipmaps
    struct.pack_into('<I', rttex_header, 100, height)
    struct.pack_into('<I', rttex_header, 104, width)
    struct.pack_into('<I', rttex_header, 108, len(img_raw))  # Raw data length
    struct.pack_into('<I', rttex_header, 112, 0)  # Padding

    # Compress using zlib
    compressed_data = zlib.compress(rttex_header + img_raw)

    # Create the RTPACK Header (32 bytes)
    rtpack_header = bytearray(32)
    rtpack_header[:6] = b"RTPACK"
    struct.pack_into('<I', rtpack_header, 8, len(compressed_data))  # Compressed size
    struct.pack_into('<I', rtpack_header, 12, 124 + len(img_raw))  # Uncompressed size
    rtpack_header[16] = 1  # Flag

    return BytesIO(rtpack_header + compressed_data)

def rttex_unpack(file: bytes, *, x: int = None, y: int = None, force_opaque: bool = False) -> BytesIO:
    if file[:6] == b'RTPACK':
        file = zlib.decompress(file[32:])

    if file[:6] == b'RTTXTR':
        width = struct.unpack_from('<I', file, 12)[0]
        height = struct.unpack_from('<I', file, 8)[0]
        channels = 3 + file[28]  # 3 channels + alpha

        # Extract raw image data and convert to PNG using Pillow
        img_data = file[124:]
        img = Image.frombytes('RGBA' if channels == 4 else 'RGB', (width, height), img_data)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        # Remove transparency in non background pixels
        if channels == 4 and force_opaque:
            img.putdata([
                (r, g, b, 255) if a != 0 else (255, 255, 255, 0)
                for r, g, b, a in img.getdata()
            ])

        if x is not None and y is not None:
            img = img.crop((x * 32, y * 32, x * 32 + 32, y * 32 + 32))

        # Save as PNG
        output = BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        return output
    else:
        print("This is not a RTTEX file")
        return None
