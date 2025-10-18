from midiutil import MIDIFile
import os

# These should never need to change
track = 0
channel = 0
volume = 100

def OctaveScale():
    my_midi = MIDIFile(1)
    my_midi.addTempo(track=0, time=0, tempo=120)

    # A4 to G#4
    notes = range(57, 68)

    time = 0
    for note in notes:
        duration = 1  # Note plays for 1 beat
        my_midi.addNote(track, channel, note, time, duration, volume)
        time += 1 # Advance to the next beat

    with open(os.path.join("midi", "middle_octave_scale.midi"), "wb") as output_file:
        my_midi.writeFile(output_file)

def CScale():
    my_midi = MIDIFile(1)
    my_midi.addTempo(track=0, time=0, tempo=120)

    #  C4, D4, E4, F4, G4, A4, B4, C5
    # [60, 62, 64, 65, 67, 69, 71, 72]

    duration = 1  # All notes play for 1 beat

    time = 0
    my_midi.addNote(track, channel, 60, time, duration, volume) # C4
    my_midi.addNote(track, channel, 62, time, duration, volume) # D4
    my_midi.addNote(track, channel, 64, time, duration, volume) # E4

    time = 1
    my_midi.addNote(track, channel, 62, time, duration, volume) # D4
    my_midi.addNote(track, channel, 64, time, duration, volume) # E4
    my_midi.addNote(track, channel, 65, time, duration, volume) # F4

    time = 2
    my_midi.addNote(track, channel, 64, time, duration, volume) # E4
    my_midi.addNote(track, channel, 65, time, duration, volume) # F4
    my_midi.addNote(track, channel, 67, time, duration, volume) # G4

    time = 3
    my_midi.addNote(track, channel, 65, time, duration, volume) # F4
    my_midi.addNote(track, channel, 67, time, duration, volume) # G4
    my_midi.addNote(track, channel, 69, time, duration, volume) # A4

    time = 4
    my_midi.addNote(track, channel, 67, time, duration, volume) # G4
    my_midi.addNote(track, channel, 69, time, duration, volume) # A4
    my_midi.addNote(track, channel, 71, time, duration, volume) # B4

    time = 5
    my_midi.addNote(track, channel, 69, time, duration, volume) # A4
    my_midi.addNote(track, channel, 71, time, duration, volume) # B4
    my_midi.addNote(track, channel, 72, time, duration, volume) # C5

    with open(os.path.join("midi", "middle_c_triads.midi"), "wb") as output_file:
        my_midi.writeFile(output_file)

def JustC():
    my_midi = MIDIFile(1)
    my_midi.addTempo(track=0, time=0, tempo=120)

    for i in range(12):
        my_midi.addNote(track, channel, 60, i * 2, 1, volume)

    with open(os.path.join("midi", "middle_just_c.midi"), "wb") as output_file:
        my_midi.writeFile(output_file)

def AllCs():
    my_midi = MIDIFile(1)
    my_midi.addTempo(track=0, time=0, tempo=120)

    # Set initial time and duration
    time = 0      # Start time in beats
    duration = 1  # Duration in beats (1 beat for each note)

    # MIDI note numbers for all C notes (0, 12, 24, ..., 120)
    # The lowest MIDI note is 0 (C), and the highest C is 120 (C9 or C8)
    # The maximum MIDI note is 127 (G9 or G8)
    for note_number in range(0, 128, 12):
        my_midi.addNote(track, channel, note_number, time, duration, volume)
        # Advance the time for the next note
        time += duration

    with open(os.path.join("midi", "all_c.midi"), "wb") as output_file:
        my_midi.writeFile(output_file)

if __name__ == '__main__':
    OctaveScale()
    CScale()
    JustC()
    AllCs()