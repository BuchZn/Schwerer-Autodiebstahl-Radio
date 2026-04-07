from PIL import Image
from io import BytesIO
import struct

def create_buffer(img_path):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((240, 240))
    pixels = img.load()
    
    # Erstellen einen leeren Daten-Puffer
    buffer = bytearray()
    
    # Jeden einzelnen Pixel durchgehen und in den Puffer packen
    for y in range(240):
        for x in range(240):
            r, g, b = pixels[x, y]
            
            # Die Farben für das Display in das 16-Bit Format (RGB565) umrechnen
            color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            
            # Die 2 Bytes des Pixels an den Puffer anhängen
            buffer.extend(struct.pack('<H', color))

    with open("output.bin", "wb") as f:
        f.write(buffer)
    return 0


def main():
    create_buffer("./Loading_Screen.jpg")
    

# Main Loop
if __name__ == "__main__":
    main()