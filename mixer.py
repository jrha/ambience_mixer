#!/usr/bin/env python2

from os.path import exists, dirname, realpath
from sys import stdout, argv
from gcd_lcm import lcm
from pygame import time
from gst import (
    element_factory_make,
    Format,
    STATE_PLAYING,
    STATE_NULL,
    FORMAT_TIME,
)

def make_channel(channel_number):
    channel = element_factory_make("playbin2", "channel%02d" % channel_number)
    fakesink = element_factory_make("fakesink", "fakesink")
    channel.set_property("video-sink", fakesink)
    bus = channel.get_bus()
    return channel, bus


def make_channels(channel_count):
    channels = []
    buses = {}
    for i in range(channel_count):
        channel, bus = make_channel(i)
        channels.append(channel)
        buses[bus] = channel
    return channels, buses


def load_sounds(sound_files, bpm, channels):
    bps = bpm/60.
    timings = {}
    time_format = Format(FORMAT_TIME)
    for i, sf in enumerate(sound_files):
        if exists(sf):
            channel = channels[i]
            channel.set_property('uri', u'file://%s/%s' % (cwd, sf))
            channel.set_state(STATE_PLAYING)
            channel.get_state()
            length = channel.query_duration(time_format)[0] / 10.**9
            channel.set_state(STATE_NULL)
            channel.get_state()
            # Round beats to nearest even number
            # (this is generally the right thing to do)
            beats = int(round(length/2. * bps)*2)
            if beats not in timings:
                timings[beats] = []
            timings[beats].append(channel)
    return timings


def main(sound_files, bpm):
    bps = bpm/60.
    clock = time.Clock()
    channels, buses = make_channels(len(sound_files))
    timings = load_sounds(sound_files, bpm, channels)

    max_time = lcm(*timings.keys())

    print '%2d sounds loaded' % len(channels)

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
                for channel in sounds:
                    channel.set_state(STATE_NULL)
                    channel.set_state(STATE_PLAYING)
                    channel.set_property('volume', 0.75)
                    stdout.write('~')
            else:
                stdout.write(' '*len(sounds))
        print '|'

        if ticker >= max_time:
            ticker = 0

if __name__ == '__main__':
    cwd = realpath(dirname(argv[0]))
    with open('tracklist') as tracklist:
        tracks = tracklist.readlines()
        tracks = [t.strip() for t in tracks]
        main(tracks, 100)
