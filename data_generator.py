#!/usr/bin/env python
# encoding: utf-8

from generator.generator_pos import generate as generate_data

SCALE_FACTOR = 1

def generate():
    options = {
        'scale_factor': SCALE_FACTOR
    }

    generate_data(**options)

if __name__ == '__main__':
    generate()

