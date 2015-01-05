#!/usr/bin/env python
# encoding: utf-8

from generator.generator_simple import generate as generate_data

def main():
    options = {
        'scale_factor': 10
    }

    generate_data(**options)

if __name__ == '__main__':
    main()