from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import moviepy.editor
import json
from collections import namedtuple
import librosa
from pprint import pprint
from av import guess_segments
from parsemidi import get_notes
import midi

# note_vid = VideoFileClip('vids/guitar_notes.mp4')

# note_segments = dict([('E2', (0.47891156462585033, 1.08843537414966)),
#                  ('F2', (1.3554648526077098, 1.9998185941043083)),
#                  ('F#2', (2.284263038548753, 2.980861678004535)),
#                  ('G2', (3.2856235827664397, 3.8922448979591837)),
#                  ('G#2', (4.118639455782313, 4.821043083900227)),
#                  ('A2', (5.073560090702948, 5.744036281179138)),
#                  ('A#2', (6.025578231292517, 6.7628117913832195)),
#                  ('B2', (6.942766439909297, 7.650975056689342)),
#                  ('C3', (7.883174603174603, 8.544943310657596)),
#                  ('C#3', (8.785850340136054, 9.401179138321995)),
#                  ('D3', (9.682721088435374, 10.231292517006803)),
#                  ('D#3', (10.533151927437642, 11.180408163265307)),
#                  ('E2', (11.421315192743764, 12.167256235827665)),
#                  ('F3', (12.34140589569161, 13.0118820861678)),
#                  ('F#3', (13.212154195011339, 13.992925170068027)),
#                  ('G3', (14.100317460317461, 14.706938775510205)),
#                  ('G#3', (14.988480725623583, 15.783764172335601)),
#                  ('A3', (15.836009070294784, 16.33233560090703)),
#                  ('A#3', (16.61968253968254, 17.33079365079365)),
#                  ('B3', (17.574603174603176, 18.207346938775512)),
#                  ('C4', (18.416326530612245, 19.092607709750567)),
#                  ('C#4', (20.195555555555554, 20.889251700680273)),
#                  ('D4', (21.086621315192744, 21.73387755102041)),
#                  ('D#4', (21.922539682539682, 22.659773242630386)),
#                  ('E4', (22.796190476190475, 23.40281179138322)),
#                  ('F4', (23.591473922902495, 24.29097505668934)),
#                  ('F#4', (24.450612244897957, 25.1762358276644)),
#                  ('G4', (25.274920634920633, 25.997641723356008)),
#                  ('G#4', (26.171791383219954, 26.816145124716552)),
#                  ('A4', (27.039637188208616, 28.92045351473923))])

# note_segments = dict(
#     [ ('E2', (0.0, 1.3090249433106576)),
#       ('F2', (2.258140589569161, 3.091156462585034)),
#       ('F#2', (5.006802721088436, 5.979138321995465)),
#       ('F2', (5.98204081632653, 5.9878458049886625)),
#       ('G2', (7.740952380952381, 8.73360544217687)),
#       ('G#2', (11.366167800453514, 12.080181405895692)),
#       ('A2', (14.152562358276644, 15.31936507936508)),
#       ('A#2', (19.472834467120183, 20.329070294784582)),
#       ('B2', (22.825215419501134, 23.85560090702948)),
#       ('C3', (25.806077097505668, 26.482358276643993)),
#       ('C#3', (28.609886621315194, 29.320997732426303)),
#       ('D3', (32.33668934240363, 32.87074829931973)),
#       ('D#3', (37.61052154195011, 38.58575963718821)),
#       ('E3', (40.90485260770975, 42.2312925170068)),
#       ('F3', (45.360181405895695, 46.419591836734696)),
#       ('F#3', (48.48907029478458, 49.26984126984127)),
#       ('G3', (51.88789115646259, 53.16498866213152)),
#       ('G#3', (56.41578231292517, 58.0237641723356)),
#       ('A3', (61.55319727891156, 62.80126984126984)),
#       ('A#3', (73.94104308390023, 74.36190476190477)),
#       ('B3', (77.49950113378685, 78.17578231292516)),
#       ('C4', (81.86775510204082, 82.66884353741497)),
#       ('C#4', (85.19691609977325, 86.66267573696145)),
#       ('D4', (88.55510204081632, 90.1340589569161)),
#       ('D#4', (104.28371882086168, 105.31410430839003)),
#       ('E4', (107.5025850340136, 108.61714285714285)),
#       ('F4', (111.45868480725623, 113.04344671201814)),
#       ('F#4', (127.45142857142856, 128.9578231292517)),
#       ('G4', (130.41197278911565, 131.3407709750567)),
#       ('G#4', (133.59020408163266, 134.82086167800455)),
#       ('A4', (137.63337868480727, 138.89886621315193)),
#       # ('D4', (144.93605442176872, 145.57460317460317)),
#     ])





moonlight = get_notes(midi.read_midifile('Beethoven-Moonlight-Sonata.mid'))
bodensee = get_notes(midi.read_midifile('Die-Fischerin-Von-Bodensee.mid'))
bumble = get_notes(midi.read_midifile('The-Flight-Of-The-Bumble-Bee.mid'))
mozart = get_notes(midi.read_midifile('Minuet-in-Mozart.mid'))
dontstopme = get_notes(midi.read_midifile('dont-stop-me-now.mid'))
zelda_dungeon = get_notes(midi.read_midifile('zelda_dungeon.mid'))


def make_test_vid(note_vid, segments, fname):

    t = 0

    clips = []
    padding = 2
    i = 0

    for note, (start, end) in segments:
        clip = note_vid.subclip(start, end)
        clip = clip.set_start(t)
        
        clips.append(clip)

        txt = (TextClip("%d %s" % (i, note),
                        color='white',
                        font='Ubuntu-Bold',
                        fontsize=22)
               .margin(1)
               .margin( top=30,left=30, opacity=0.0)
               .set_pos(('left','top'))
               .set_duration(end - start + padding) 
               .set_start(t))
        clips.append(txt)

        t += (end - start) + padding
        i += 1

        print( t, i)



    full_video = CompositeVideoClip(clips)
    print('full length %f' % full_video.duration)
    full_video.write_videofile(fname,threads=20)



def next_octave(note_name, exponent=1):
    return librosa.hz_to_note(librosa.note_to_hz(note_name)* pow(2, exponent))

def make_vid(fname, note_vid, note_info, note_segments):

    slot_width = int(note_vid.size[0]/4)
    slot_height = int(note_vid.size[1]/4)
    slot_positions = {}
    for slot in range(20):
        x = slot % 4
        y = int(slot/4)
        slot_positions[slot] = (slot_width * x, slot_height* y)

    note_clips = {}
    for note,(start,end) in note_segments.items():
        note_clips[note] = note_vid.subclip(start,end).resize(width=slot_width)


    max_note = librosa.hz_to_note(max(librosa.note_to_hz(x) for x in note_segments))
    min_note = librosa.hz_to_note(min(librosa.note_to_hz(x) for x in note_segments))
    print (min_note, max_note)

    clips = []

    ordered_notes = [(True, i, note.usec_offset, note) for i,note in enumerate(note_info)]
    ordered_notes.extend( (False, i, note.usec_offset + note.duration, note) for i,note in enumerate(note_info
))

    def note_key(x):
        (on, i , t , n) = x
        return t
    ordered_notes.sort(key=note_key)

    active_notes = {}

    for on, i, _, note in ordered_notes:
        if on:

            slot = None
            for s in range(20):
                if s not in active_notes:
                    slot = s
                    break
            else:
                raise Exception('Not enough slots')
            active_notes[slot] = i

            print('clipping note %d' % i)
            closest_note = None
            wanted_note = librosa.midi_to_note(note.pitch)

            closest_note = note_clips.get(wanted_note)
            if not closest_note:
                if librosa.note_to_hz(wanted_note) > librosa.note_to_hz(max_note):
                    dir = -1
                else:
                    dir = 1

                for i in range(10):

                    wanted_note = next_octave(wanted_note,dir)
                    closest_note = note_clips.get(wanted_note)
                    if closest_note:
                        break

                else:
                    raise Exception("couldn't find note for " + librosa.midi_to_note(note.pitch))

            fudge = 0.28
            note_duration_seconds = note.duration/1e6 + fudge
            if note_duration_seconds < closest_note.duration:

                closest_note = closest_note.subclip(0,note_duration_seconds)
                print ('clipping %f to %f' % (note_duration_seconds, closest_note.duration))
            closest_note = closest_note.set_start(note.usec_offset / 1e6)
            print(slot_positions[slot])
            closest_note = closest_note.set_position(slot_positions[slot])

            clips.append(closest_note)
            print ( closest_note.start, closest_note.duration)
        else:
            slot = None

            for k,v in active_notes.items():
                if v == i:
                    slot = k
                    break
            else:
                raise Exception('Missing active slot')

            del active_notes[k]

    full_video = CompositeVideoClip(clips, size=(slot_width*4, slot_height*5))
    print('full length %f' % full_video.duration)
    full_video.write_videofile(fname,threads=20)


