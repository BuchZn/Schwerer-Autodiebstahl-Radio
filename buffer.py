from PIL import Image
import struct
import os

def create_buffer(img_path, output_name="output.bin"):
    if not os.path.exists(img_path):
        print(f"Fehler: {img_path} nicht gefunden!")
        return

    img = Image.open(img_path).convert("RGB")
    img = img.resize((240, 240),Image.Resampling.LANCZOS)
    pixels = img.load()
    
    buffer = bytearray()
    
    for y in range(240):
        for x in range(240):
            r, g, b = pixels[x, y]
            
            # RGB565 Konvertierung

            color = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            # WICHTIG: '>H' für Big-Endian (Standard für die meisten SPI-Displays)
            buffer.extend(struct.pack('<H', color))

    with open(output_name, "wb") as f:
        f.write(buffer)
    
    print(f"Datei {output_name} erfolgreich erstellt ({len(buffer)} Bytes).")

images = {
    'blc':     '/home/pi/img/BLC.jpeg',
    'nonstop': '/home/pi/img/NonStopPop.jpg',
    'blueark': '/home/pi/img/BlueArk.jpeg',
    'channelx': '/home/pi/img/ChannelX.jpeg',
    'eastlostfm': '/home/pi/img/EastLostFm.jpeg',
    'eastlosantos': '/home/pi/img/EastLosantos.jpeg',
    'radiomirrow': '/home/pi/img/RadioMirrow.jpeg',
    'rebelradio': '/home/pi/img/RebelRadio.jpeg',
    'rockradio': '/home/pi/img/RockRadio.jpeg',
    'soulwaxfm': '/home/pi/img/SoulwaxFM.jpeg',
    'spacefm': '/home/pi/img/SpaceFM.jpeg',
    'thelowlay': '/home/pi/img/Thelowlay.jpeg',
    'vineyard': '/home/pi/img/Vineyard.jpeg',
    'wctr': '/home/pi/img/WCTR.jpeg',
    'westcoastclassic': '/home/pi/img/WCclassics.jpeg',
    'worldwidefm': '/home/pi/img/WorldWideFM.jpg',
    'flylofm': '/home/pi/img/FlyloFM.jpeg',
    'losu': '/home/pi/img/LosSantosU.jpg',
    'lap': '/home/pi/img/LapR.jpg',
    'blonde': '/home/pi/img/Blonded_Radio.jpeg',
    'loading': '/home/pi/img/Loading_Screen.jpg',
}

def main():
    for name, path in images.items():
        buf = create_buffer(path,name)
        print(f"Gespeichert: {name}.bin")

if __name__ == "__main__":
    main()