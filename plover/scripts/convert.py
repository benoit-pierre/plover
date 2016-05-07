#!/usr/bin/env python2

import sys

from plover.config import CONFIG_FILE, Config
from plover.registry import registry
from plover import system
from plover.dictionary.base import create_dictionary, load_dictionary


def setup():
    config = Config()
    config.target_file = CONFIG_FILE
    with open(config.target_file, 'rb') as f:
        config.load(f)
        registry.load_plugins()
        registry.update()
        system_name = config.get_system_name()
        system.setup(system_name)

def run():
    if len(sys.argv) != 3:
        print 'usage: %s INPUT_DICTIONARY OUTPUT_DICTIONARY' % sys.argv[0]
        return
    setup()
    input = sys.argv[1]
    output = sys.argv[2]
    id = load_dictionary(input)
    od = create_dictionary(output)
    od.update(id)
    od.save()

if '__main__' == __name__:
    run()
