#!/usr/bin/env python3
"""
Polyglot v3 node server test (negative values)
Copyright (C) 2021 Robert Paauwe
"""
import udi_interface
import sys
import time

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom
polyglot = None
configured = False
Parameters = None
Notices = None
n_queue = []
count = 0

class TestNode(udi_interface.Node):
    id = 'test'
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},
            {'driver': 'GV0', 'value': 0, 'uom': 56},
            {'driver': 'GV1', 'value': 0, 'uom': 56},
            ]

    def noop(self):
        LOGGER.info('Discover not implemented')

    commands = {'DISCOVER': noop}

def node_queue(data):
    n_queue.append(data['address'])

def wait_for_node_event():
    while len(n_queue) == 0:
        time.sleep(0.1)
    n_queue.pop()

def discover(params):
    global configured
    global Notices
    global Parameters


def poll(polltype):
    global configured
    global count

    node = polyglot.getNode('controller')
    node.setDriver('GV0', count, True, True)
    node.setDriver('GV1', (count * -1), True, True)
    Notices['count'] = 'Current count is {}'.format(count))
    count += 1

def stop():
    nodes = polyglot.getNodes()
    for n in nodes:
        nodes[n].setDriver('ST', 0, True, True)
    polyglot.stop()

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start()

        Parameters = Custom(polyglot, 'customparams')
        Notices = Custom(polyglot, 'notices')

        polyglot.subscribe(polyglot.CUSTOMPARAMS, discover)
        polyglot.subscribe(polyglot.ADDNODEDONE, node_queue)
        polyglot.subscribe(polyglot.STOP, stop)
        polyglot.subscribe(polyglot.POLL, poll)

        polyglot.ready()
        polyglot.setCustomParamsDoc()
        polyglot.updateProfile()

        node = TestNode(polyglot, 'controller', 'controller', 'TestNode')
        polyglot.addNode(node)
        wait_for_node_event()

        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        

