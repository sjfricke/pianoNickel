import sys
import os
from mido import MidiFile, tempo2bpm, tick2second

def parse_midi_to_c_array(midi_file_path, output_file_path="midi_data.h"):
    """
    Parses a MIDI file and generates a C header file with timing constants
    and 12-byte event entries:
    [code(1), channel(1), note(1), volume(1), time_abs[4], duration[4]]

    The time and duration values are encoded as 4-byte little-endian integers
    representing time in MIDI ticks.
    """
    try:
        mid = MidiFile(midi_file_path)
    except FileNotFoundError:
        print(f"Error: MIDI file not found at {midi_file_path}")
        return
    except Exception as e:
        print(f"Error loading MIDI file: {e}")
        return

    # --- 1. Extract Timing Constants from MIDI File ---

    # Ticks Per Beat (PPQ) is stored in the MIDI header
    ticks_per_beat = mid.ticks_per_beat

    # Default Tempo: 120 BPM = 500,000 us/beat
    microseconds_per_beat = 500000

    # Search for the first 'set_tempo' meta message across all tracks
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                microseconds_per_beat = msg.tempo
                break  # Found the tempo, stop searching this track
        if microseconds_per_beat != 500000:
            break # Found the tempo, exit outer loop

    print(f"Detected Ticks/Beat (PPQ): {ticks_per_beat}")
    print(f"Detected Tempo (us/beat): {microseconds_per_beat}")

    # --- 2. Event Extraction and Calculation (as before) ---

    NOTE_ON_CODE = 0x00
    NOTE_OFF_CODE = 0x01
    open_notes = {}
    midi_array_data = []
    current_time_ticks = 0

    print(f"Processing MIDI file: {os.path.basename(midi_file_path)}")

    # First Pass: Extracting and Calculating Events
    for i, track in enumerate(mid.tracks):
        print(f"  Processing Track {i+1}...")
        current_time_ticks = 0

        for msg in track:
            current_time_ticks += msg.time

            # Handle Note-On Events
            if msg.type == 'note_on' and msg.velocity > 0:
                key = (msg.channel, msg.note)

                # Close any re-triggered note first
                if key in open_notes:
                    start_ticks, volume = open_notes.pop(key)
                    duration_ticks = current_time_ticks - start_ticks

                    duration_bytes = duration_ticks.to_bytes(4, byteorder='little')
                    time_bytes = start_ticks.to_bytes(4, byteorder='little')

                    midi_array_data.append([
                        NOTE_OFF_CODE, msg.channel, msg.note, volume,
                        *time_bytes, *duration_bytes
                    ])

                # Store and record the new Note-On event
                open_notes[key] = (current_time_ticks, msg.velocity)
                time_bytes = current_time_ticks.to_bytes(4, byteorder='little')
                duration_bytes = (0).to_bytes(4, byteorder='little')

                midi_array_data.append([
                    NOTE_ON_CODE, msg.channel, msg.note, msg.velocity,
                    *time_bytes, *duration_bytes
                ])

            # Handle Note-Off Events
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                key = (msg.channel, msg.note)

                if key in open_notes:
                    start_ticks, volume = open_notes.pop(key)
                    duration_ticks = current_time_ticks - start_ticks

                    # Store the completed Note-Off event
                    duration_bytes = duration_ticks.to_bytes(4, byteorder='little')
                    time_bytes = start_ticks.to_bytes(4, byteorder='little')

                    midi_array_data.append([
                        NOTE_OFF_CODE, msg.channel, msg.note, volume,
                        *time_bytes, *duration_bytes
                    ])


    # Clean up any open notes at the end of the file
    for (channel, note), (start_ticks, volume) in open_notes.items():
        duration_ticks = current_time_ticks - start_ticks

        duration_bytes = duration_ticks.to_bytes(4, byteorder='little')
        time_bytes = start_ticks.to_bytes(4, byteorder='little')

        midi_array_data.append([
            NOTE_OFF_CODE,
            channel,
            note,
            volume,
            *time_bytes,
            *duration_bytes
        ])

    # Sort the final array by absolute time (time_abs)
    midi_array_data.sort(key=lambda x: int.from_bytes(x[4:8], 'little'))

    # --- 3. Generate C Array Code ---

    ENTRY_SIZE = 12
    total_bytes = len(midi_array_data) * ENTRY_SIZE

    # Format the data into C-style hex strings, 12 bytes per line
    c_array_lines = []
    for entry in midi_array_data:
        if len(entry) != ENTRY_SIZE:
            raise ValueError(f"Entry size is {len(entry)}, expected {ENTRY_SIZE}.")

        line = "   " + ", ".join([f"0x{b:02x}" for b in entry]) + ","
        c_array_lines.append(line)

    # Write the C header file
    with open(output_file_path, 'w') as f:
        f.write("// This file was auto-generated by midi_parser.py\n")
        f.write("// Each line is a 12-byte event: \n")
        f.write("// [code(1), channel(1), note(1), volume(1), time_abs[4,LE], duration[4,LE]]\n\n")

        f.write(f"const uint32_t TICKS_PER_BEAT = {ticks_per_beat}; // Ticks per Quarter Note (PPQ)\n")
        f.write(f"const uint32_t MICROSECONDS_PER_BEAT = {microseconds_per_beat}; // Tempo: Microseconds per Beat\n\n")
        f.write(f"const uint32_t MIDI_CONTENT_SIZE = {total_bytes};\n")
        f.write(f"const uint32_t MIDI_EVENT_COUNT = {len(midi_array_data)};\n")
        f.write(f"const uint32_t EVENT_SIZE_BYTES = 12;\n")
        f.write(f"const float TICK_TIME_MS = (float)MICROSECONDS_PER_BEAT / (float)TICKS_PER_BEAT / 1000.0f;\n")
        f.write(f"\n")
        f.write(f"const uint8_t midi_content[{total_bytes}] PROGMEM = {{\n")

        # Write all lines EXCEPT the last one, with a newline
        for line in c_array_lines[:-1]:
            f.write(line + "\n")

        # Write the LAST line WITHOUT the trailing comma
        if c_array_lines:
            last_line_no_comma = c_array_lines[-1][:-1]
            f.write(last_line_no_comma + "\n")

        f.write("};\n")

    print(f"\nSuccessfully generated {output_file_path} with {len(midi_array_data)} events ({total_bytes} bytes).")
    print("Remember to include this file and use PROGMEM on Arduino.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python midi_parser.py <path_to_midi_file>")
        sys.exit(1)

    midi_file = sys.argv[1]
    parse_midi_to_c_array(midi_file)
