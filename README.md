# Robbie Bobbie's Midi Library
Sup nerds,

This is a homemade MIDI python library (still in production).

The goal is to create layers of abstraction 
(->): Composed of 

MIDI File -> Tracks -> Event objects

The readMidiFile() function will take a file location and immediatly start the decompression process and output a MidiFile object.
