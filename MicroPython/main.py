# Wireless Morse code transmitter / receiver
# Press A for dot, press B for dash
# based on http://microbit-micropython.readthedocs.io/en/latest/tutorials/network.html

from microbit import *
import music
import radio
import neopixel

np = neopixel.NeoPixel(pin0, 3)
radio.config(group=17)
radio.on()

# A lookup table of morse codes and associated characters.
MORSE_CODE_LOOKUP = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0",
}

# durations made a bit shorter than 250ms for a dot
# durations made a bit shorter than 500ms for a dash
DOT_DURATION = 230
DASH_DURATION = 470

# detect a new letter if incoming signal is greater than 1000ms.
LETTER_THRESHOLD = 1000

# Holds the incoming Morse signals.
buffer = ""
# Holds the translated Morse as characters.
message = ""
# The time from which the device has been waiting for the next event.
started_to_wait = running_time()


def decode(buffer):
    # Attempts to get the buffer of Morse code data from the lookup table. If
    # it's not there, just return a question mark.
    return MORSE_CODE_LOOKUP.get(buffer, "?")


while True:
    # Work out how long the device has been waiting for a keypress.
    waiting = running_time() - started_to_wait
    signal = radio.receive()
    # Button presses for sending a message
    if button_a.is_pressed():
        display.show(".")
        radio.send(".")
        music.pitch(1200, duration=DOT_DURATION, wait=True)
        sleep(50)  # little sleep added to debounce
        display.clear()
    elif button_b.is_pressed():
        display.show("-")
        radio.send("-")
        music.pitch(1200, duration=DASH_DURATION, wait=True)
        sleep(50)  # little sleep added to debounce
        display.clear()
    # Listen out for dashes and dots over radio
    if signal:
        if signal == ".":
            pin0.write_digital(1)
            buffer += "."
            display.show(".")
            sleep(DOT_DURATION)
            display.clear()
            pin0.write_digital(1)
            np[2] = (255, 0, 0)
            np.show()
        elif signal == "-":
            buffer += "-"
            display.show("-")
            sleep(DASH_DURATION)
            display.clear()
            np[2] = (255, 255, 0)
            np.show()
