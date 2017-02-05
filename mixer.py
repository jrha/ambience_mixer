#!/usr/bin/env python2

from pygame import init, mixer, time
from os.path import exists
from sys import stdout
from gcd_lcm import lcm

def load_sounds(sound_files, bpm):
    bps = bpm/60.
    sounds = []
    timings = {}
    for sf in sound_files:
        if exists(sf):
            sound = mixer.Sound(sf)
            if sound:
                sounds.append(sound)
                length = sound.get_length()
                # Round beats to nearest even number
                # (this is generally the right thing to do)
                beats = int(round(length/2. * bps)*2)
                if beats:
                    print 'added sound of length %5.1f seconds => %3d beats' % (length, beats)
                    if beats not in timings:
                        timings[beats] = []
                        timings[beats].append(sound)
                else:
                    print 'E: Skipping %s, zero length' % sf
            else:
                print 'E: Failed to open %s' % sf
        else:
            print 'E: Will not open %s, does not exist' % sf
    return sounds, timings


def main(sound_files, bpm):
    bps = bpm/60.
    init()
    clock = time.Clock()
    sounds, timings = load_sounds(sound_files, bpm)

    max_time = lcm(*timings.keys())

    print '%2d sounds loaded' % len(sounds)

    for timer, soundlist in timings.iteritems():
        print "%2d sounds are %2d beats long" % (len(soundlist), timer)

    print "lowest common loop beat length is", max_time

    ticker = -1
    while True:
        ticker += 1
        stdout.write('%8d |' % ticker)
        clock.tick(bps)
        for timer, sounds in timings.iteritems():
            if ticker % timer == 0:
                for sound in sounds:
                    sound.stop()
                    sound.play()
                    sound.set_volume(0.75)
                    stdout.write('~')
            else:
                stdout.write(' '*len(sounds))
        print '|'

        if ticker >= max_time:
            ticker = 0

if __name__ == '__main__':
    with open('tracklist') as tracklist:
        tracks = tracklist.readlines()
        tracks = [t.strip() for t in tracks]
        mixer.pre_init(frequency=32000)
        main(tracks, 100)
