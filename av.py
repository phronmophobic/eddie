from __future__ import print_function

import itertools
from pprint import pprint


# We'll need numpy for some mathematical operations
import numpy as np

# matplotlib for displaying the output
import matplotlib.pyplot as plt
import matplotlib.style as ms
ms.use('seaborn-muted')
# get_ipython().run_line_magic('matplotlib', 'inline')

# and IPython.display for audio output
# import IPython.display

# Librosa for audio
import librosa
# And the display module for visualization
import librosa.display


def guess_note(y, sr):
    r = librosa.autocorrelate(y, max_size=5000)

    midi_hi = 120.0
    midi_lo = 12.0
    f_hi = 700
    f_lo = 75
    t_lo = sr/f_hi
    t_hi = sr/f_lo



    r[:int(t_lo)] = 0
    r[int(t_hi):] = 0


    t_max = r.argmax()

    note = librosa.hz_to_note(float(sr)/t_max)

    return note


def show_spectrogram(y, sr):
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    log_S = librosa.power_to_db(S, ref=np.max)

    # Make a new figure
    plt.figure(figsize=(12,4))

    # Display the spectrogram on a mel scale
    # sample rate and hop length parameters are used to render the time axis
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')

    # Put a descriptive title on the plot
    plt.title('mel power spectrogram')

    # draw a color bar
    plt.colorbar(format='%+02.0f dB')

    # Make the figure layout compact
    plt.tight_layout()
    plt.show()


def onset_detection ():
    # y, sr = librosa.load(librosa.util.example_audio_file())
    S = np.abs(librosa.stft(y))

    # Fit a degree-0 polynomial (constant) to each frame

    p0 = librosa.feature.poly_features(S=S, order=0)

    # Fit a linear polynomial to each frame

    p1 = librosa.feature.poly_features(S=S, order=1)

    # Fit a quadratic to each frame

    p2 = librosa.feature.poly_features(S=S, order=2)

    # Plot the results for comparison

    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(4,1,1)
    plt.plot(p2[2], label='order=2', alpha=0.8)
    plt.plot(p1[1], label='order=1', alpha=0.8)
    plt.plot(p0[0], label='order=0', alpha=0.8)
    plt.xticks([])
    plt.ylabel('Constant')
    plt.legend()
    plt.subplot(4,1,2, sharex=ax)
    plt.plot(p2[1], label='order=2', alpha=0.8)
    plt.plot(p1[0], label='order=1', alpha=0.8)
    plt.xticks([])
    plt.ylabel('Linear')
    plt.subplot(4,1,3, sharex=ax)
    plt.plot(p2[0], label='order=2', alpha=0.8)
    plt.xticks([])
    plt.ylabel('Quadratic')
    plt.subplot(4,1,4, sharex=ax)
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                             y_axis='log')
    plt.tight_layout()
    plt.show()



# y, sr = librosa.load(audio_path)
# oenv = librosa.onset.onset_strength(y=y, sr=sr)
# # Detect events without backtracking
# onset_raw = librosa.onset.onset_detect(onset_envelope=oenv,
#                                        backtrack=False)
# # Backtrack the events using the onset envelope
# onset_bt = librosa.onset.onset_backtrack(onset_raw, oenv)
# # Backtrack the events using the RMS values
# rms = librosa.feature.rms(S=np.abs(librosa.stft(y=y)))
# onset_bt_rms = librosa.onset.onset_backtrack(onset_raw, rms[0])

def to_seconds(r_index, hop_length, sr):
    sample = r_index * hop_length
    sec = sample / sr
    return sec

def guess_segments(audio_path, hop_length=64, plot=False):

    y, sr = librosa.load(audio_path)

    hop_length = 64

    rms = librosa.feature.rms(y=y,hop_length=hop_length)
    r = rms[0]

    threshold = 0.005
    segments = []

    below = True
    segment_start = None
    for i,x in enumerate(r):
        if below:
            if x > threshold:
                below = False
                segment_start = i
        else:
            if x <= threshold:
                below = True
                segments.append((segment_start, i))


    segments_in_seconds = [(to_seconds(start, hop_length, sr),
                            to_seconds(end, hop_length, sr))
                          for start,end in segments]

    segment_notes = []
    for (start, end) in segments:
        start_sample_index = start * hop_length
        end_sample_index = end * hop_length
        note = guess_note(y[start_sample_index:end_sample_index], sr)
        segment_notes.append(note)

    notes = list(zip(segment_notes, segments_in_seconds))

    if plot:

        # Plot the results
        import matplotlib.pyplot as plt
        plt.figure()
        plt.subplot(2,1,1)
        # plt.plot(oenv, label='Onset strength')
        # plt.vlines(onset_raw, 0, oenv.max(), label='Raw onsets')
        # plt.vlines(onset_bt, 0, oenv.max(), label='Backtracked', color='r')
        # plt.legend(frameon=True, framealpha=0.75)

        rdiff = r[1:] - r[:-1]
        plt.plot(rdiff)
        plt.hlines([rdiff.max()*0.15], 0 , len(rdiff))
        plt.subplot(2,1,2)
        plt.plot(rms[0], label='RMS')

        # plt.vlines(onset_bt_rms, 0, rms.max(), label='Backtracked (RMS)', color='r')
        plt.vlines(list(itertools.chain(*segments)), 0, rms.max())

        plt.legend(frameon=True, framealpha=0.75)
        plt.show()

    return notes

        
