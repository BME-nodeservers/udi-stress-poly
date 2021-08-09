## Configuration

There are two different stress tests that can be configured and run.

1) The driver set/get stress test. On each short poll, set every driver and then get the value of every driver.  Configure the number number of nodes to use and set the number of cycles to zero.  short poll should be about 1 minute for every 10 nodes.

2) The node add/delete stress test. On each short poll, delete all the node and re-add them Cycle number of times. Configure the number of nodes and the number cycles to add/delete.


Key = Nodes
Value = Number of nodes to create

Key = Cycles
Value = Number of node add/delete cycles per poll (0 to disable)
