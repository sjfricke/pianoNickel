#include <MIDI.h>
MIDI_CREATE_DEFAULT_INSTANCE();

enum Note {
  C = 0, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B
};

// Maps notes to the pin on the board
byte NoteToPin(byte midiNote) {
    switch (midiNote) {
      case 57: return 0;
      case 58: return 0;
      case 59: return 0;
      case 60: return 0;
      case 61: return 0;
      case 62: return 0;
      case 63: return 0;
      case 64: return 0;
      case 65: return 0;
      case 66: return 0;
      case 67: return 0;
      case 68: return 0;
      default: break;
    }
}

void GetMidiNote(Note note, byte octave) {
  // C4 is Middle C (MIDI 60)
  return note + 12 * (octave + 1);
}

void PlayNote(byte channel, byte note, byte velocity) {
  int pin = NoteToPin(note);

  digitalWrite (pin, HIGH);
  delay(50);
  digitalWrite(pin, LOW);
  delay(1000);
}

void StopNote(byte channel, byte note, byte velocity) {
  Serial.print("Note Off: ");
  Serial.println(note);
}

void setup() {
  Serial.begin(115200);  // setup up communication with USB

  // Connect the library's callback functions to your custom functions.
  // The library will automatically call 'PlayNote' when a Note On message is received.
  MIDI.setHandleNoteOn(PlayNote);

  // The library will automatically call 'StopNote' for Note Off messages.
  MIDI.setHandleNoteOff(StopNote);

  // Start listening for incoming MIDI data.
  MIDI.begin(MIDI_CHANNEL_OMNI); // OMNI listens on all MIDI channels.
}

void loop() {
    MIDI.read();
}
