import midi
from collections import namedtuple
from more_itertools import peekable
import json

# moonlight = midi.read_midifile('Beethoven-Moonlight-Sonata.mid')
# bodensee = midi.read_midifile('Die-Fischerin-Von-Bodensee.mid')
# bumble = midi.read_midifile('The-Flight-Of-The-Bumble-Bee.mid')
# mozart = midi.read_midifile('Minuet-in-Mozart.mid')
# dontstopme = midi.read_midifile('dont-stop-me-now.mid')
# # zelda = midi.read_midifile('zelda.mid')
# zelda_dungeon = midi.read_midifile('zelda_dungeon.mid')


TickOffset = namedtuple('TickOffset', 'usec_offset tick_offset tick_duration total_ticks' )
Note = namedtuple('Note', 'usec_offset pitch duration instrument') 

def bpm_to_tick_duration(resolution, bpm):
    return (60 * 1000000 / bpm) / resolution

def get_notes(pattern):
    
    # default per midi spec
    tick_duration = bpm_to_tick_duration(pattern.resolution, 120)

    all_notes = []
    track_infos = [{'events': peekable(track),
                    'tick': 0,
                    'activeNotes': {},
                    'instruments': {},
                    }
                  for track in pattern]

    tick = 0
    usec_offset = 0
    while any(track['events'] for track in track_infos):
        # print tick
        for track in track_infos:
            

            events = track['events']

            while events and track['tick'] + events.peek().tick <= tick:
                event = next(events)
                track['tick'] += event.tick

                active_notes = track['activeNotes']
                
                
                if isinstance(event, midi.events.SetTempoEvent):
                    tick_duration = bpm_to_tick_duration(pattern.resolution, event.bpm)

                elif (isinstance(event, midi.NoteOnEvent) and event.velocity == 0) or isinstance(event, midi.NoteOffEvent):
                    
                    
                    note_key = (event.channel, event.pitch )

                    note = active_notes.get(note_key)
                    if not note:
                        print('warning! no active note found')
                        continue


                    note = note._replace(duration=usec_offset - note.usec_offset)
                    all_notes.append(note)
                    del active_notes[note_key]
                    
                elif isinstance(event, midi.NoteOnEvent):

                    note_key = (event.channel, event.pitch )
                    active_notes[note_key] = Note(usec_offset, event.pitch, None, track['instruments'].get(event.channel))

                elif isinstance(event, midi.ProgramChangeEvent):
                    track['instruments'][event.channel] = event.value

        tick += 1
        usec_offset += tick_duration


    all_notes = [note for note in all_notes if note.instrument is not None]

    return all_notes
        
