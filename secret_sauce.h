const uint8_t PLAY_BUTTON_PIN = 3;

const uint8_t PIANO_CHANNEL = 0;
const uint8_t XYLOPHONE_CHANNEL = 1;
const uint8_t SNARE_DRUM_CHANNEL = 2;
const uint8_t BASS_DRUM_CHANNEL = 3;
const uint8_t WODDEN_BLOCK_CHANNEL = 4;
const uint8_t SYMBOL_CHANNEL = 5;
const uint8_t TRIANGLE_CHANNEL = 6;
const uint8_t TAMBOURINE_CHANNEL = 7;

uint8_t PianoNoteToPin(uint8_t midi_note) {
    switch (midi_note) {
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
        default: return 0;
    }
}

uint8_t XylophoneNoteToPin(uint8_t midi_note) {
    switch (midi_note) {
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
        default: return 0;
    }
}

uint8_t SnareDrumNoteToPin(uint8_t midi_note) {
    switch (midi_note) {
        case 0: return 0;
        case 1: return 0;
        default: return 0;
    }
}

uint8_t BassDrumNoteToPin(uint8_t midi_note) {
    switch (midi_note) {
        case 0: return 0;
        case 1: return 0;
        case 2: return 0;
        default: return 0;
    }
}

uint8_t WoddenBlockNoteToPin() {
    return 0;
}

uint8_t SymbolNoteToPin() {
    return 0;
}

uint8_t TriangleNoteToPin() {
    return 0;
}

uint8_t TambourineNoteToPin() {
    return 0;
}
