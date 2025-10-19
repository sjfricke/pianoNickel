#include "secret_sauce.h"

// When this is "0" it will use the pre-loaded MIDI file
// When this is "1" it will try to read the MIDI from a USB
#define USB_MODE 1

#if USB_MODE
#include <MIDI.h>
MIDI_CREATE_DEFAULT_INSTANCE();
#else
#include <avr/pgmspace.h>
#include "midi_data.h"
#endif

void SolenoidOn(uint8_t pin) {
  if (pin != 0) {
    digitalWrite(pin, HIGH);
  }
}

void SolenoidOff(uint8_t pin) {
  if (pin != 0) {
    digitalWrite(pin, LOW);
  }
}

void PlayPiano(uint8_t note, uint8_t velocity) {
  uint8_t pin = PianoNoteToPin(note);
  SolenoidOn(pin);
}

void StopPiano(uint8_t note) {
  uint8_t pin = PianoNoteToPin(note);
  SolenoidOff(pin);
}

void PlayXylophone(uint8_t note, uint8_t velocity) {
  uint8_t pin = XylophoneNoteToPin(note);
  SolenoidOn(pin);
}

void StopXylophone(uint8_t note) {
  uint8_t pin = XylophoneNoteToPin(note);
  SolenoidOff(pin);
}

void PlaySnareDrum(uint8_t note, uint8_t velocity) {
  uint8_t pin = SnareDrumNoteToPin(note);
  SolenoidOn(pin);
}

void StopSnareDrum(uint8_t note) {
  uint8_t pin = SnareDrumNoteToPin(note);
  SolenoidOff(pin);
}

void PlayBassDrum(uint8_t note, uint8_t velocity) {
  uint8_t pin = BassDrumNoteToPin(note);
  SolenoidOn(pin);
}

void StopBassDrum(uint8_t note) {
  uint8_t pin = BassDrumNoteToPin(note);
  SolenoidOff(pin);
}

void PlayWoodenBlock(uint8_t velocity) {
  uint8_t pin = WoddenBlockNoteToPin();
  SolenoidOn(pin);
}

void StopWoodenBlock() {
  uint8_t pin = WoddenBlockNoteToPin();
  SolenoidOff(pin);
}

void PlaySymbol(uint8_t velocity) {
  uint8_t pin = SymbolNoteToPin();
  SolenoidOn(pin);
}

void StopSymbol() {
  uint8_t pin = SymbolNoteToPin();
  SolenoidOff(pin);
}

void PlayTriangle(uint8_t velocity) {
  uint8_t pin = TriangleNoteToPin();
  SolenoidOn(pin);
}

void StopTriangle() {
  uint8_t pin = TriangleNoteToPin();
  SolenoidOff(pin);
}

void PlayTambourine(uint8_t velocity) {
  uint8_t pin = TambourineNoteToPin();
  SolenoidOn(pin);
}

void StopTambourine() {
  uint8_t pin = TambourineNoteToPin();
  SolenoidOff(pin);
}

void PlayNote(uint8_t channel, uint8_t note, uint8_t velocity) {
  if (channel == PIANO_CHANNEL) {
    PlayPiano(note, velocity);
  } else if (channel == XYLOPHONE_CHANNEL) {
    PlayXylophone(note, velocity);
  } else if (channel == SNARE_DRUM_CHANNEL) {
    PlaySnareDrum(note, velocity);
  } else if (channel == BASS_DRUM_CHANNEL) {
    PlayBassDrum(note, velocity);
  } else if (channel == WODDEN_BLOCK_CHANNEL) {
    PlayWoodenBlock(velocity);
  } else if (channel == SYMBOL_CHANNEL) {
    PlaySymbol(velocity);
  } else if (channel == TRIANGLE_CHANNEL) {
    PlayTriangle(velocity);
  } else if (channel == TAMBOURINE_CHANNEL) {
    PlayTambourine(velocity);
  }
}

void StopNote(uint8_t channel, uint8_t note, uint8_t velocity) {
  if (channel == PIANO_CHANNEL) {
    StopPiano(note);
  } else if (channel == XYLOPHONE_CHANNEL) {
    StopXylophone(note);
  } else if (channel == SNARE_DRUM_CHANNEL) {
    StopSnareDrum(note);
  } else if (channel == BASS_DRUM_CHANNEL) {
    StopBassDrum(note);
  } else if (channel == WODDEN_BLOCK_CHANNEL) {
    StopWoodenBlock();
  } else if (channel == SYMBOL_CHANNEL) {
    StopSymbol();
  } else if (channel == TRIANGLE_CHANNEL) {
    StopTriangle();
  } else if (channel == TAMBOURINE_CHANNEL) {
    StopTambourine();
  }
}

// Ensure any pin we use starts off and as an output
void TurnOnAndResetPin(uint8_t pin) {
  if (pin != 0) {
    pinMode(pin, OUTPUT);
    SolenoidOff(pin);
  }
}

#if USB_MODE
#else
uint32_t ReadUInt32FromProgmem(const uint8_t *addr) {
    uint32_t value = 0;
    value |= ((uint32_t)pgm_read_byte(addr + 0) << 0);
    value |= ((uint32_t)pgm_read_byte(addr + 1) << 8);
    value |= ((uint32_t)pgm_read_byte(addr + 2) << 16);
    value |= ((uint32_t)pgm_read_byte(addr + 3) << 24);
    return value;
}

void PlayEmbeddedMidi() {
  uint32_t playback_start_time = millis();
  uint32_t current_event_index = 0;
  while(1) {
    if (current_event_index >= MIDI_EVENT_COUNT) {
        return;
    }

    const uint8_t *event_ptr = midi_content + (current_event_index * EVENT_SIZE_BYTES);

    uint32_t time_abs_ticks = ReadUInt32FromProgmem(event_ptr + 4);

    // Convert target ticks to target milliseconds from the start of playback
    // Use float calculation to preserve precision
    uint32_t target_time_ms = (uint32_t)(time_abs_ticks * TICK_TIME_MS);

    uint32_t current_time_ms = millis() - playback_start_time;

    if (current_time_ms >= target_time_ms) {
        uint8_t code = pgm_read_byte(event_ptr + 0);
        uint8_t channel = pgm_read_byte(event_ptr + 1);
        uint8_t note = pgm_read_byte(event_ptr + 2);
        uint8_t velocity = pgm_read_byte(event_ptr + 3);

        // 0x00 = Note On, 0x01 = Note Off
        if (code == 0x00) {
            PlayNote(channel, note, velocity);
        } else if (code == 0x01) {
            StopNote(channel, note, velocity);
        }

        current_event_index++;
    }
  }
}
#endif

void setup() {
  uint8_t pin = 0;
  for (uint8_t i = 0; i < 255; i++) {
    pin = PianoNoteToPin(i);
    TurnOnAndResetPin(pin);

    pin = XylophoneNoteToPin(i);
    TurnOnAndResetPin(pin);

    // Could be reduced
    pin = SnareDrumNoteToPin(i);
    TurnOnAndResetPin(pin);

    // Could be reduced
    pin = BassDrumNoteToPin(i);
    TurnOnAndResetPin(pin);
  }

  pin = WoddenBlockNoteToPin();
  TurnOnAndResetPin(pin);

  pin = SymbolNoteToPin();
  TurnOnAndResetPin(pin);

  pin = TriangleNoteToPin();
  TurnOnAndResetPin(pin);

  pin = TambourineNoteToPin();
  TurnOnAndResetPin(pin);

  pinMode(PLAY_BUTTON_PIN, INPUT_PULLUP);

#if USB_MODE
  // Stuff to set up the USB logic
  Serial.begin(31250);
  MIDI.setHandleNoteOn(PlayNote);
  MIDI.setHandleNoteOff(StopNote);
  MIDI.begin(MIDI_CHANNEL_OMNI); // OMNI listens on all MIDI channels.
#endif
}

void loop() {
#if USB_MODE
  MIDI.read();
#else
  bool button_pressed = (digitalRead(PLAY_BUTTON_PIN) == LOW);
  if (button_pressed) {
    PlayEmbeddedMidi();
    // Add a very small delay to prevent the loop from running too fast
    // and potentially starving other necessary operations.
    delay(1);
  }
#endif
}
