# pip install mido python-rtmidi pyserial
import mido
import serial

# Open the Device Manager in Windows (you can search for it in the Start Menu).
# Look under the "Ports (COM & LPT)" section. You'll see your Arduino listed, for example, as Arduino Mega 2560 (COM3). Note this COM port number.
SERIAL_PORT = 'COM3'

# matches code in Arduino
BAUD_RATE = 115200

MIDI_FILE = 'middle_octave_scale.midi'

try:
    # Open the serial port
    with serial.Serial(SERIAL_PORT, BAUD_RATE) as port:
        print(f"Successfully opened port {SERIAL_PORT} at {BAUD_RATE} baud.")

        # Open the MIDI file
        try:
            mid = mido.MidiFile(MIDI_FILE)
            print(f"Playing '{MIDI_FILE}'...")

            # Play the MIDI file, message by message
            for msg in mid.play():
                print(f"Sending: {msg}")
                # Send the message's raw byte data to the Arduino
                port.write(msg.bin())

            print("Finished playing.")

        except FileNotFoundError:
            print(f"Error: MIDI file not found at '{MIDI_FILE}'")
        except Exception as e:
            print(f"An error occurred while playing the MIDI file: {e}")

except serial.SerialException as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    print("Please make sure your Arduino is connected and you have the correct COM port.")


