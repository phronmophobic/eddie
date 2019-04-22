import midi
import intervalmap
from collections import namedtuple
from more_itertools import peekable

moonlight = midi.read_midifile('Beethoven-Moonlight-Sonata.mid')
bodensee = midi.read_midifile('Die-Fischerin-Von-Bodensee.mid')

# pattern = 
# print pattern
# with open('moonlight.txt','w') as f:
#     f.write(str(moonlight))

# with open('bodensee.txt','w') as f:
#     f.write(str(bodensee))


# midi.ControlChangeEvent
# '''This message is sent when a controller value changes. Controllers include devices such as pedals and levers. Controller numbers 120-127 are reserved as "Channel Mode Messages" (below). (ccccccc) is the controller number (0-119). (vvvvvvv) is the controller value (0-127).'''

# midi.EndOfTrackEvent
# midi.KeySignatureEvent
# midi.NoteOffEvent
# midi.NoteOnEvent
# midi.Pattern
# midi.PitchWheelEvent
# midi.PortEvent
# midi.ProgramChangeEvent
# midi.SequencerSpecificEvent
# midi.SetTempoEvent
# # This sets the tempo in microseconds per quarter note. This means a change in the unit-length of a delta-time tick.
# midi.TextMetaEvent
# midi.TimeSignatureEvent
# midi.Track
# midi.TrackNameEvent


# for i, track in enumerate(bodensee):
#     p = midi.Pattern()
#     p.append(track)
#     midi.write_midifile("bodensee"+ str(i) + ".mid", p)



track = moonlight[1]


TickOffset = namedtuple('TickOffset', 'usec_offset tick_offset tick_duration total_ticks' )


def tickDict(resolution, track):


    tick_offsets = intervalmap.intervalmap()
    last_offset = TickOffset(0, 0, 0, 0)
    for event in track:
        
        last_offset = last_offset._replace(total_ticks= last_offset.total_ticks + event.tick)

        is_set_tempo_event = isinstance(event, midi.events.SetTempoEvent)
        is_end_of_track_event = isinstance(event, midi.EndOfTrackEvent)

        if is_set_tempo_event or is_end_of_track_event:
            tick_offsets[last_offset.tick_offset:last_offset.tick_offset + last_offset.total_ticks] = last_offset

            if is_set_tempo_event:
                tick_duration = (60 * 1000000 / event.bpm) / resolution
                offset = TickOffset(last_offset.usec_offset + (last_offset.tick_duration * last_offset.total_ticks),
                                    last_offset.tick_offset + last_offset.total_ticks,
                                    tick_duration,
                                    0)

                last_offset = offset


    return tick_offsets

Note = namedtuple('Note', 'usec_offset pitch duration instrument') 

def bpm_to_tick_duration(resolution, bpm):
    return (60 * 1000000 / bpm) / resolution

def get_notes(pattern):
    
    # default per midi spec
    tick_duration = bpm_to_tick_duration(pattern.resolution, 120)

    all_notes = []
    # track_events [peekable(track) for track in pattern]
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
                event = events.next()
                track['tick'] += event.tick

                active_notes = track['activeNotes']
                
                
                if isinstance(event, midi.events.SetTempoEvent):
                    tick_duration = bpm_to_tick_duration(pattern.resolution, event.bpm)

                elif (isinstance(event, midi.NoteOnEvent) and event.velocity == 0) or isinstance(event, midi.NoteOffEvent):
                    
                    
                    note_key = (event.channel, event.pitch )

                    note = active_notes.get(note_key)
                    if not note:
                        print 'warning! no active note found'
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


    return all_notes
        
