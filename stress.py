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
    global Notices
    global Parameters

    validNodes = False
    validCycles = False
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

    if Parameters['Cycles'] is not None:
        cycles = int(Parameters['Cycles'])
        if cycles > 0:
            validCycles = True
        else:
            LOGGER.error('Invalid number of cycles {}, must be > 0'.format(cycles))
            Parameters['Cycles'] = 0
    else:
        LOGGER.error('Missing cycle count')
        Parameters['Cycles'] = 0

    if validNodes:
        for i in range(0, ncount):
            address = 'stress_{}'.format(i)
            node = StressNode(polyglot, address, address, address)
            polyglot.addNode(node)
            wait_for_node_event()

        configured = True
    else:
        Notices['nodecount'] = 'Enter the number of nodes to create'

    if not validCycles:
        Notices['cycles'] = 'Enter the number of cycles to add/delete'

def poll(polltype):
    global configured
    global count

    drivers = [
            'GV0', 'GV1', 'GV2', 'GV3', 'GV4',
            'GV5', 'GV6', 'GV7', 'GV8', 'GV9',
            'GV10', 'GV11', 'GV12', 'GV13', 'GV14',
            'GV15', 'GV16', 'GV17', 'GV18', 'GV19', 'GV20'
            ]


    if configured:
        n_cycles = int(Parameters['Cycles'])
        n_nodes = int(Parameters['Nodes'])

        if n_cycles == 0:
            LOGGER.info('Starting driver stress test')
            nodes = polyglot.getNodes()
            for n in nodes:
                for d in drivers:
                    nodes[n].setDriver(d, count, True, True)

            if Parameters['getDrivers'] is not None and 'TRUE' in Parameters['getDrivers']:
                for n in nodes:
                    for d in drivers:
                        if nodes[n].getDriver(d) != count:
                            LOGGER.error('{} Failed to update driver {}'.format(n, d))

            count += 1
        else:
            LOGGER.info('Starting node add/delete stress test')
            for c in range(0, n_cycles):
                nodes = polyglot.getNodes()
                LOGGER.info('Deleteing nodes cycle {}'.format(c))
                for n in nodes:
                    polyglot.delNode(n)

                LOGGER.info('Adding nodes cycle {}'.format(c))
                for i in range(0, n_nodes):
                    address = 'stress_{}'.format(i)
                    node = StressNode(polyglot, address, address, address)
                    polyglot.addNode(node)
                    wait_for_node_event()



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
        

