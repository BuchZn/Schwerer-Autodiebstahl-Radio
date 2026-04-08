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
    '/home/pi/img/blc.bin':     '/home/pi/img/BLC.jpeg',
    '/home/pi/img/nonstop.bin': '/home/pi/img/NonStopPop.jpg',
    '/home/pi/img/blueark.bin': '/home/pi/img/BlueArk.jpeg',
    '/home/pi/img/channelx.bin': '/home/pi/img/ChannelX.jpeg',
    '/home/pi/img/eastlostfm.bin': '/home/pi/img/EastLostFm.jpeg',
    '/home/pi/img/eastlosantos.bin': '/home/pi/img/EastLosantos.jpeg',
    '/home/pi/img/radiomirrow.bin': '/home/pi/img/RadioMirrow.jpeg',
    '/home/pi/img/rebelradio.bin': '/home/pi/img/RebelRadio.jpeg',
    '/home/pi/img/rockradio.bin': '/home/pi/img/RockRadio.jpeg',
    '/home/pi/img/soulwaxfm.bin': '/home/pi/img/SoulwaxFM.jpeg',
    '/home/pi/img/spacefm.bin': '/home/pi/img/SpaceFM.jpeg',
    '/home/pi/img/thelowlay.bin': '/home/pi/img/Thelowlay.jpeg',
    '/home/pi/img/vineyard.bin': '/home/pi/img/Vineyard.jpeg',
    '/home/pi/img/wctr.bin': '/home/pi/img/WCTR.jpeg',
    '/home/pi/img/westcoastclassic.bin': '/home/pi/img/WCclassics.jpeg',
    '/home/pi/img/worldwidefm.bin': '/home/pi/img/WorldWideFM.jpg',
    '/home/pi/img/flylofm.bin': '/home/pi/img/FlyloFM.jpeg',
    '/home/pi/img/losu.bin': '/home/pi/img/LosSantosU.jpg',
    '/home/pi/img/lap.bin': '/home/pi/img/LapR.jpg',
    '/home/pi/img/blonde.bin': '/home/pi/img/Blonded_Radio.jpeg',
    '/home/pi/img/loading.bin': '/home/pi/img/Loading_Screen.jpg',
}

def main():
    for name, path in images.items():
        buf = create_buffer(path,name)
        print(f"Gespeichert: {name}.bin")

if __name__ == "__main__":
    main()