# HTQRCodeGen

This is a simple Python script that applies dithering to images before embedding them into QR Codes. The script converts an input image into a black-and-white dithered version, then integrates it into a scannable QR Code.

## Features

- Converts images to black-and-white using dithering (Floyd-Steinberg or other methods)
- Generates colorful QR Codes
- Embeds dithered images into QR Codes
- Generates scannable QR Codes

## Requirements

- Python 3.x
- `pillow` (for image processing)
- `segno` (for QR code generation)

You can install dependencies using:

```bash
pip -r requirements.txt
```

## Usage

Run the script with:

```bash
python main.py
```

## License

This project is licensed under the MIT License.