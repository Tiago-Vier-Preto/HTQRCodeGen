from PIL import Image, ImageDraw
import segno
from segno.consts import *

version = 6
pixelSize = 2
blockSize = 3 * pixelSize
border = 0

def control_blocks(QRCode):
    temp = []
    for row in QRCode.matrix_iter(verbose=True, border=border):
        res = []
        for col in row:
            if col == TYPE_DATA_DARK or col == TYPE_DATA_LIGHT:
                res.append(None)
            elif col in {TYPE_ALIGNMENT_PATTERN_DARK, TYPE_FINDER_PATTERN_DARK, TYPE_TIMING_DARK, TYPE_FORMAT_DARK, TYPE_VERSION_DARK, TYPE_DARKMODULE}:
                res.append(True)
            elif col in {TYPE_ALIGNMENT_PATTERN_LIGHT, TYPE_FINDER_PATTERN_LIGHT, TYPE_TIMING_LIGHT, TYPE_FORMAT_LIGHT, TYPE_VERSION_LIGHT, TYPE_SEPARATOR, TYPE_QUIET_ZONE}:
                res.append(False)
        temp.append(res)
    return temp

def apply_dithering(image):
    image_1 = image.convert("1", dither=Image.FLOYDSTEINBERG)
    image_2 = image.convert("1", dither=0)
    blended_image = Image.blend(image_1.convert("L"), 
                            image_2.convert("L"), 
                            alpha=0.5)

    # Converter o resultado para preto e branco novamente
    final_image = blended_image.convert("1", dither=Image.NONE)
    return final_image

def halftoneQR(QRCode, controlBytes, image):
    qr_matrix = list(QRCode.matrix_iter(border=border))
    qr_size = len(qr_matrix)
    width, height = qr_size * blockSize, qr_size * blockSize

    # Resize and dither the image
    img_dithered = apply_dithering(image)
    result_image = img_dithered.resize((width, height), Image.NEAREST)

    draw = ImageDraw.Draw(result_image)

    for row_idx, row in enumerate(qr_matrix):
        for col_idx, cell in enumerate(row):
            x = col_idx * blockSize
            y = row_idx * blockSize

            # Set the middle block to the QR code value
            mid_x = x + pixelSize
            mid_y = y + pixelSize
            color = "black" if cell else "white"
            draw.rectangle([mid_x, mid_y, mid_x + 1, mid_y + 1], fill=color)

    # Redraw control blocks on top
    for row_idx, row in enumerate(controlBytes):
        for col_idx, control in enumerate(row):
            if control is not None:
                x = col_idx * blockSize
                y = row_idx * blockSize
                color = "black" if control else "white"
                draw.rectangle([x, y, x + blockSize, y + blockSize], fill=color)

    return result_image

def run(image_path, data_string):
    img = Image.open(image_path)

    # Generate the QR code
    qrcode = segno.make(data_string, version=version, error='h')
    controlBytes = control_blocks(qrcode)

    # Generate halftone QR code
    result = halftoneQR(qrcode, controlBytes, img)

    result.show()