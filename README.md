
# Stress Node Server (c) 2021 Robert Paauwe

A simple node server for stress testing Polyglot/ISY

This node server simply creates a user defined number of nodes. Each node
has a status plus 21 raw drivers.

At every poll interval, every driver of every node is updated

## Installation

This is designed to be installed locally and is not available in the 
node server store.  You will need to clone the repository to your Polisy
or other local location and do a local node server installation using your
clone.

### Node Settings
The settings for this node are:

#### Short Poll
   * How often to update the drivers
#### Long Poll
   * Will also update the drivers at this interval

#### Nodes
   * The number of nodes to create


## Requirements

1. Polyglot V3.
2. ISY firmware 5.3.x or later

# Release Notes

- 1.1.0 08/09/2021
   - Add node add/delte stress test
- 1.0.0 08/06/2021
   - Initial version published to github
