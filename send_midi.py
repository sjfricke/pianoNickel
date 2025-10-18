# pip install mido pyserial
import argparse
import glob
import sys
from threading import Thread
import mido
import serial
import time
import os
import tkinter as tk

MIDI_FOLDER = 'midi'
MIDI_FILE = 'middle_octave_scale.midi'

global_serial_port = None

class App(tk.Frame):
    def __init__(self, master, serial_port_obj):
        super().__init__(master)
        self.pack(padx=20, pady=20, fill='both', expand=True)
        self.port = serial_port_obj
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="MIDI Player", font=('Arial', 18, 'bold')).pack(pady=(0, 15))

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill='x', pady=10)
        self.load_midi_files_and_create_buttons()

    def load_midi_files_and_create_buttons(self):
        search_pattern_midi = os.path.join(MIDI_FOLDER, '*.midi')
        search_pattern_mid = os.path.join(MIDI_FOLDER, '*.mid')
        midi_paths = glob.glob(search_pattern_midi) + glob.glob(search_pattern_mid)

        if not midi_paths:
            tk.Label(self.button_frame, text=f"No .mid/.midi files found in ./{MIDI_FOLDER}", fg='red').pack()
            return

        for full_path in midi_paths:
            file_name = os.path.basename(full_path)
            # Use lambda to capture the specific full_path for the button's command
            button = tk.Button(
                self.button_frame,
                text=f"▶ Play: {file_name}",
                # Command wraps the playback function in a thread
                command=lambda p=full_path: self.start_play_thread(p),
                font=('Arial', 11),
                bg='#e0f7fa',
                activebackground='#b2ebf2',
                relief=tk.RAISED
            )
            button.pack(fill='x', pady=5)

    def start_play_thread(self, full_file_path):
        """Starts the PlayMidi logic in a background thread."""
        # Disable all buttons to prevent multiple playbacks
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)

        # Print to console immediately
        print(f"\n--- PLAYBACK STARTED ---")
        print(f"File: {os.path.basename(full_file_path)}")

        # Start the playback in a new thread
        play_thread = Thread(target=self.play_midi_callback, args=(full_file_path,))
        play_thread.start()

    def play_midi_callback(self, full_file_path):
        file_name = os.path.basename(full_file_path)

        try:
            mid = mido.MidiFile(full_file_path)
            # Iterate over messages and send them
            for msg in mid.play():
                if self.port and self.port.is_open:
                    print(f"Sending: {msg}")
                    self.port.write(msg.bin())
                else:
                    print(f"DEBUG Sending: {msg} (No COM port active)")

        except FileNotFoundError:
            print(f"Error: MIDI file not found at '{full_file_path}'")
        except Exception as e:
            print(f"An error occurred while playing the MIDI file: {e}")

        print(f"--- PLAYBACK ENDED ---\n")

        # Re-enable buttons on the main thread once done
        self.master.after(0, self.enable_buttons)

    def enable_buttons(self):
        """Safely re-enables all buttons on the main thread."""
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.NORMAL)

def main(argv):
    global global_serial_port

    parser = argparse.ArgumentParser(description='Send MIDI data to the Arduino')
    parser.add_argument('--debug', action='store_true', help='Debug mode with no COM port')
    args = parser.parse_args(argv)

    root = tk.Tk()
    root.title("Andy Magical Nickelodeon MIDI Sender")
    root.geometry("400x500") # Fixed size for button list

    if args.debug:
        print("DEBUG MODE: Serial communication disabled.")
        global_serial_port = None
    else:
        try:
            COM = 'COM3'
            # Found 115200 is too fast for something
            BAUD_RATE = 31250
            global_serial_port = serial.Serial(COM, BAUD_RATE, timeout=0.1)
            print(f"Successfully connected to {COM}")
            time.sleep(1)  # Give the Arduino time to reset
        except serial.SerialException as e:
            print(f"Error opening serial port {COM}: {e}")
            print("Please make sure your Arduino is connected and you have the correct COM port.")

    app = App(master=root, serial_port_obj=global_serial_port)

    def on_closing():
        print("Closing serial port...")
        if global_serial_port and global_serial_port.is_open:
            global_serial_port.close()
        root.destroy()
        sys.exit(0) # Ensure the main thread terminates cleanly

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
