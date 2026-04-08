import time
import signal
import os
from PIL import Image
import struct
from RPi import GPIO
from PlayRadio import play_radio, init_random_duration
import threading


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CLK  = 5
DT = 6
SW = 26


GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW,GPIO.IN , pull_up_down=GPIO.PUD_DOWN)


#Rotary Encoder Conf
counter = 0
clkLastState = GPIO.input(CLK)   # Initial read of CLK pin
clkState = 0
delayTime = 0.02
dtState = 0
swState = 0
image_index = 1


blc = "/home/pi/img/blc.bin"
nonstop = "/home/pi/img/nonstop.bin"
blueA = "/home/pi/img/blueark.bin"
CHx = "/home/pi/img/channelx.bin"
ELSfm = "/home/pi/img/eastlostfm.bin"
Es = "/home/pi/img/eastlosantos.bin"
Rm = "/home/pi/img/radiomirrow.bin"
RebelR = "/home/pi/img/rebelradio.bin"
RockR = "/home/pi/img/rockradio.bin"
Soulwax = "/home/pi/img/soulwaxfm.bin"
Space = "/home/pi/img/spacefm.bin"
Lowlay = "/home/pi/img/thelowlay.bin"
Vn = "/home/pi/img/vineyard.bin"
WTCr = "/home/pi/img/wctr.bin"
WSc = "/home/pi/img/westcoastclassic.bin"
WWfm = "/home/pi/img/worldwidefm.bin"
Flfm = "/home/pi/img/flylofm.bin"
LosUfm = "/home/pi/img/losu.bin"
LapB = "/home/pi/img/lap.bin"
BlondeB = "/home/pi/img/blonde.bin"
Loading_S = "/home/pi/img/loading.bin"




def bin_to_lcd(path):
#Liest eine Binärdatei und schreibt sie in den Framebuffer fb1
    bin_path = os.path.join(SCRIPT_DIR, path)
    
    if not os.path.exists(bin_path):
        print(f"Bin File not found at: {bin_path}")
        return

    try:
        with open(bin_path, "rb") as fr:
            bibuf = fr.read()
            
        def _write(data):
            try:
                # buffering=0 ist entscheidend für Device-Files!
                with open("/dev/fb1", "wb", buffering=0) as fb:
                    fb.write(data)
                print(f"Bild {path} auf Display geschrieben.")
            except Exception as e:
                print(f"LCD Error: {e}")

        # Schreiben im Hintergrund, um den Encoder nicht zu blockieren
        threading.Thread(target=_write, args=(bibuf,), daemon=True).start()
        
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")

encoder_steps = 0
# Updated callback logic
def ausgabeFunktion(channel):
    global image_index, clkLastState, encoder_steps
    
    # Read current state of CLK
    current_clk = GPIO.input(CLK)
    
    # Only act if the state has actually changed
    if current_clk != clkLastState:
        if GPIO.input(DT) != current_clk:
            encoder_steps += 1
        else:
            encoder_steps -= 1

        # Erst bei jedem 2. Schritt den Index ändern
        if abs(encoder_steps) >= 2:
            if encoder_steps > 0:
                image_index += 1
            else:
                image_index -= 1
            
            encoder_steps = 0  # zurücksetzen

            if image_index > 21: image_index = 1
            if image_index < 1:  image_index = 21


            if(image_index == 1):
                bin_to_lcd(blc)
                play_radio(0, 1)
            elif((image_index > 1) and (image_index <= 2)):
                bin_to_lcd(nonstop)
                play_radio(0, 2)
            elif((image_index > 2) and (image_index <= 3)):
                bin_to_lcd(blueA)
                play_radio(0, 3)
            elif((image_index > 3) and (image_index <= 4)):
                bin_to_lcd(CHx)
                play_radio(0, 4)
            elif((image_index > 4) and (image_index <= 5)):
                bin_to_lcd(ELSfm)
                play_radio(0, 5)
            elif((image_index > 5) and (image_index <= 6)):
                bin_to_lcd(Es)
                play_radio(0, 6)
            elif((image_index > 6) and (image_index <= 7)):
                bin_to_lcd(Rm)
                play_radio(0, 7)
            elif((image_index > 7) and (image_index <= 8)):
                bin_to_lcd(RebelR)
                play_radio(0, 8)
            elif((image_index > 8) and (image_index <= 9)):
                bin_to_lcd(RockR)
                play_radio(0, 9)
            elif((image_index > 9) and (image_index <= 10)):
                bin_to_lcd(Soulwax)
                play_radio(0, 10)
            elif((image_index > 10) and (image_index <= 11)):
                bin_to_lcd(Space)
                play_radio(0, 11)
            elif((image_index > 11) and (image_index <= 12)):
                bin_to_lcd(Lowlay)
                play_radio(0, 12)
            elif((image_index > 12) and (image_index <= 13)):
                bin_to_lcd(Vn)
                play_radio(0, 13)
            elif((image_index > 13) and (image_index <= 14)):
                bin_to_lcd(WTCr)
                play_radio(0, 14)
            elif((image_index > 14) and (image_index <= 15)):
                bin_to_lcd(WSc)
                play_radio(0, 15)
            elif((image_index > 15) and (image_index <= 16)):
                bin_to_lcd(WWfm)
                play_radio(0, 16)
            elif((image_index > 16) and (image_index <= 17)):
                bin_to_lcd(Flfm)
                play_radio(0, 17)
            elif((image_index > 17) and (image_index <= 18)):
                bin_to_lcd(LosUfm)     
                play_radio(0, 18)
            elif((image_index > 18) and (image_index <= 19)):
                bin_to_lcd(BlondeB)     
                play_radio(0, 19)
            elif((image_index > 19) and (image_index <= 20)):
                bin_to_lcd(LapB)     
                play_radio(0, 20)         
            
            print(f"Current Image Index: {image_index}")
        
    clkLastState = current_clk

# Change the event detect to BOTH edges for smoother tracking
GPIO.remove_event_detect(CLK)
GPIO.add_event_detect(CLK, GPIO.BOTH, callback=ausgabeFunktion, bouncetime=5)



def main():
    print("Started Radio. Abbruch mit Strg+C")

    bin_to_lcd("output.bin")
    #write_to_lcd(Loading_S)
    print("Initialization of Random Start Durations")
    init_random_duration()

    try:
        # Use signal.pause() to keep the script running indefinitely
        signal.pause()
    except KeyboardInterrupt:
        print("\nCleaning up...")
    finally:
        GPIO.cleanup()



        

    

# Main Loop
if __name__ == "__main__":
    main()