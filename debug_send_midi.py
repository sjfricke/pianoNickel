import mido
import serial
import time

SERIAL_PORT = 'COM3'
BAUD_RATE = 31250
DURATION = 1

note60_on = mido.Message('note_on', note=60, velocity=100)
note60_off = mido.Message('note_off', note=60, velocity=0)

note61_on = mido.Message('note_on', note=61, velocity=100)
note61_off = mido.Message('note_off', note=61, velocity=0)

note62_on = mido.Message('note_on', note=62, velocity=100)
note62_off = mido.Message('note_off', note=62, velocity=0)

# --- Main Script ---
try:
    # Open the serial port
    with serial.Serial(SERIAL_PORT, BAUD_RATE) as port:
        print(f"Successfully opened port {SERIAL_PORT} at {BAUD_RATE} baud.")
        time.sleep(2)  # Give the Arduino time to reset

        print(f"Sending: {note60_on}")
        port.write(note60_on.bin())
        time.sleep(DURATION)

        print(f"Sending: {note60_off}")
        port.write(note60_off.bin())
        time.sleep(1) # Small delay before the next note

        print(f"Sending: {note61_on}")
        port.write(note61_on.bin())
        time.sleep(DURATION)

        print(f"Sending: {note61_off}")
        port.write(note61_off.bin())
        time.sleep(1) # Small delay before the next note

        print(f"Sending: {note62_on}")
        port.write(note62_on.bin())
        time.sleep(DURATION)

        print(f"Sending: {note62_off}")
        port.write(note62_off.bin())
        time.sleep(1) # Small delay before the next note

        print("Finished sending.")

except serial.SerialException as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    print("Please make sure your Arduino is connected and you have the correct COM port.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")