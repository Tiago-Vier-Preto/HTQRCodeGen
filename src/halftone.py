from PIL import Image, ImageDraw
import segno
from segno.consts import *

version = 6
pixelSize = 2
blockSize = 3 * pixelSize

def control_blocks(QRCode):
    temp = []
    for row in QRCode.matrix_iter(verbose=True):
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
    grayscale_image = image.convert('L')
    dithered_image = grayscale_image.convert('1', dither=0)
    return dithered_image

def halftoneQR(QRCode, controlBytes, image):
    qr_matrix = list(QRCode.matrix_iter())
    qr_size = len(qr_matrix)
    width, height = qr_size * blockSize, qr_size * blockSize

    # Resize and dither the image
    img_dithered = apply_dithering(image)
    img_dithered = img_dithered.resize((width, height), Image.NEAREST)

    # Criar uma nova imagem para desenhar
    result_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(result_image)

    for row_idx, row in enumerate(qr_matrix):
        for col_idx, cell in enumerate(row):
            x = col_idx * blockSize
            y = row_idx * blockSize

            # Draw the 9-pixel grid from the dithered image
            for i in range(3):
                for j in range(3):
                    pixel_x = x + j * pixelSize
                    pixel_y = y + i * pixelSize
                    pixel_color = img_dithered.getpixel((pixel_x, pixel_y))
                    color = "black" if pixel_color == 0 else "white"
                    draw.rectangle([pixel_x, pixel_y, pixel_x + pixelSize, pixel_y + pixelSize], fill=color)

            # Set the middle block to the QR code value
            mid_x = x + pixelSize
            mid_y = y + pixelSize
            color = "black" if cell else "white"
            draw.rectangle([mid_x, mid_y, mid_x + pixelSize, mid_y + pixelSize], fill=color)

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