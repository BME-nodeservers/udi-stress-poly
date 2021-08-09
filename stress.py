#!/usr/bin/env python3
"""
Polyglot v3 node server Volumio Media Server control.
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

class StressNode(udi_interface.Node):
    id = 'stress'
    drivers = [
            {'driver': 'ST', 'value': 1, 'uom': 2},
            {'driver': 'GV0', 'value': 0, 'uom': 56},
            {'driver': 'GV1', 'value': 0, 'uom': 56},
            {'driver': 'GV2', 'value': 0, 'uom': 56},
            {'driver': 'GV3', 'value': 0, 'uom': 56},
            {'driver': 'GV4', 'value': 0, 'uom': 56},
            {'driver': 'GV5', 'value': 0, 'uom': 56},
            {'driver': 'GV6', 'value': 0, 'uom': 56},
            {'driver': 'GV7', 'value': 0, 'uom': 56},
            {'driver': 'GV8', 'value': 0, 'uom': 56},
            {'driver': 'GV9', 'value': 0, 'uom': 56},
            {'driver': 'GV10', 'value': 0, 'uom': 56},
            {'driver': 'GV11', 'value': 0, 'uom': 56},
            {'driver': 'GV12', 'value': 0, 'uom': 56},
            {'driver': 'GV13', 'value': 0, 'uom': 56},
            {'driver': 'GV14', 'value': 0, 'uom': 56},
            {'driver': 'GV15', 'value': 0, 'uom': 56},
            {'driver': 'GV16', 'value': 0, 'uom': 56},
            {'driver': 'GV17', 'value': 0, 'uom': 56},
            {'driver': 'GV18', 'value': 0, 'uom': 56},
            {'driver': 'GV19', 'value': 0, 'uom': 56},
            {'driver': 'GV20', 'value': 0, 'uom': 56},
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

    validNodes = False
    configured = False
    Parameters.load(params)
    Notices.clear()

    if Parameters['Nodes'] is not None:
        ncount = int(Parameters['Nodes'])
        if ncount > 0 and ncount < 128:
            validNodes = True
        else:
            LOGGER.error('Invalid number of nodes {}, must be between 1 and 127'.format(ncount))
    else:
        LOGGER.error('Missing node count')

    if validNodes:
        for i in range(0, ncount):
            address = 'stress_{}'.format(i)
            node = StressNode(polyglot, address, address, address)
            polyglot.addNode(node)
            wait_for_node_event()

        configured = True
    else:
        Notices['nodecount'] = 'Enter the number of nodes to create'

def poll(polltype):
    global configured
    global count

    if configured:
        nodes = polyglot.getNodes()
        for n in nodes:
            nodes[n].setDriver('GV0', count, True, True)
            nodes[n].setDriver('GV1', count, True, True)
            nodes[n].setDriver('GV2', count, True, True)
            nodes[n].setDriver('GV3', count, True, True)
            nodes[n].setDriver('GV4', count, True, True)
            nodes[n].setDriver('GV5', count, True, True)
            nodes[n].setDriver('GV6', count, True, True)
            nodes[n].setDriver('GV7', count, True, True)
            nodes[n].setDriver('GV8', count, True, True)
            nodes[n].setDriver('GV9', count, True, True)
            nodes[n].setDriver('GV10', count, True, True)
            nodes[n].setDriver('GV11', count, True, True)
            nodes[n].setDriver('GV12', count, True, True)
            nodes[n].setDriver('GV13', count, True, True)
            nodes[n].setDriver('GV14', count, True, True)
            nodes[n].setDriver('GV15', count, True, True)
            nodes[n].setDriver('GV16', count, True, True)
            nodes[n].setDriver('GV17', count, True, True)
            nodes[n].setDriver('GV18', count, True, True)
            nodes[n].setDriver('GV19', count, True, True)
            nodes[n].setDriver('GV20', count, True, True)
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

        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        

