from PIL import Image
import struct
import os

def create_buffer(img_path, output_name="output.bin"):
    if not os.path.exists(img_path):
        print(f"Fehler: {img_path} nicht gefunden!")
        return

    img = Image.open(img_path).convert("RGB")
    img = img.resize((240, 240))
    pixels = img.load()
    
    buffer = bytearray()
    
    for y in range(240):
        for x in range(240):
            r, g, b = pixels[x, y]
            
            # RGB565 Konvertierung
            color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            
            # WICHTIG: '>H' für Big-Endian (Standard für die meisten SPI-Displays)
            buffer.extend(struct.pack('>H', color))

    with open(output_name, "wb") as f:
        f.write(buffer)
    
    print(f"Datei {output_name} erfolgreich erstellt ({len(buffer)} Bytes).")


def main():
    create_buffer("./Loading_Screen.jpg")

if __name__ == "__main__":
    main()