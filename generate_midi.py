from midiutil import MIDIFile

my_midi = MIDIFile(1)
my_midi.addTempo(track=0, time=0, tempo=120)

# A4 to G#4
notes = range(57, 68)
track = 0
channel = 0
volume = 100
time = 0

for note in notes:
    duration = 1  # Note plays for 1 beat
    my_midi.addNote(track, channel, note, time, duration, volume)
    time += 1 # Advance to the next beat

with open("middle_octave_scale.midi", "wb") as output_file:
    my_midi.writeFile(output_file)
