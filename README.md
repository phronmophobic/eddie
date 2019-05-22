


# Step 1: Create a video of yourself playing every note

- make sure you can see the part of the instrument that you use to change notes! eg. on a guitar, you want to see the fret board. on a piano, you want to be able to see the keys
- make funny faces
- notes duration should be at least 2 seconds
- pause at least 1-2 seconds in between notes
- make it easier on yourself by playing notes in order (chromatically). this will come in handy when you need to label the notes.
- background noise is the worst. make sure there is as little background noise as possible


# Step 2: Extract the audio portion of your video

You can do this with ffmpeg using the following command

`ffmpeg -i notes.mp4 audio.wav` 

# Step 3: Label the segments of the video with each note

This step is not fully automatic, but hopefully won't be too bad. 

Edit the bottom of clip.py and add:

```
segments = guess_segments('audio.wav')
make_test_vid(VideoFileClip('notes.mp4'), segments, 'test.mp4' )
```

This will attempt to automatically determine the segment clip times for each note played. The guessed note and its index will be displayed in the top left corner. Make a list of which notes are mislabelled by the program.

I like to `pprint(list(enumerate(segments)` and then manually edit the segments by commenting out the notes that were mislabelled. 

Next, if you played note notes in order, you can check to make sure that the notes pitches were guessed correctly by making sure they go in order. Double check that the octave is correct since that is the most common form of error.

# Step 4: Create a video

Here's the final code for creating edited video

```
segments = [(0, ('E2', (0.0, 1.3090249433106576))),
 (1, ('F2', (2.258140589569161, 3.091156462585034))),
 (2, ('F#2', (5.006802721088436, 5.979138321995465))),
 (3, ('F2', (5.98204081632653, 5.9878458049886625))),
 (4, ('G2', (7.740952380952381, 8.73360544217687))),
 (5, ('G#2', (11.366167800453514, 12.080181405895692))),
 (6, ('A2', (14.152562358276644, 15.31936507936508))),
 (7, ('A#2', (19.472834467120183, 20.329070294784582))),
 (8, ('B2', (22.825215419501134, 23.85560090702948))),
 (9, ('C3', (25.806077097505668, 26.482358276643993))),
 (10, ('C#3', (28.609886621315194, 29.320997732426303))),
 (11, ('D3', (32.33668934240363, 32.87074829931973))),
 (12, ('D#3', (37.61052154195011, 38.58575963718821))),
 (13, ('E3', (40.90485260770975, 42.2312925170068))),
 (14, ('F3', (45.360181405895695, 46.419591836734696))),
 (15, ('F#3', (48.48907029478458, 49.26984126984127))),
 (16, ('G3', (51.88789115646259, 53.16498866213152))),
 (17, ('G#3', (56.41578231292517, 58.0237641723356))),
 (18, ('A3', (61.55319727891156, 62.80126984126984))),
 (19, ('A#3', (73.94104308390023, 74.36190476190477))),
 (20, ('B3', (77.49950113378685, 78.17578231292516))),
 (21, ('C4', (81.86775510204082, 82.66884353741497))),
 (22, ('C#4', (85.19691609977325, 86.66267573696145))),
 (23, ('D4', (88.55510204081632, 90.1340589569161))),
 (24, ('D#4', (104.28371882086168, 105.31410430839003))),
 (25, ('E4', (107.5025850340136, 108.61714285714285))),
 (26, ('F4', (111.45868480725623, 113.04344671201814))),
 (27, ('F#4', (127.45142857142856, 128.9578231292517))),
 (28, ('G4', (130.41197278911565, 131.3407709750567))),
 (29, ('G#4', (133.59020408163266, 134.82086167800455))),
 (30, ('A4', (137.63337868480727, 138.89886621315193)))]

# you need to remove the indexes
segments = [x for i, x in segments]

# the make_vid function expects a dictionary
note_segments = dict(segments)

midi_notes = get_notes(midi.read_midifile('dont-stop-me-now.mid'))

# create the video
# this takes forever
# you probably want to use note_segments[:20] instead of the full midi_notes list the first
# time just to make sure everything is setup correctly
make_vid('song.mp4', VideoFileClip('notes.mp4'), midi_notes, note_segments)

```


