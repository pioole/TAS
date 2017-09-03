Topology Aware Scheduling Simulator

Created in order to evaluate the 3D packing algorithm developed by Kangkang Li, and its possible modifications.

master: [![Build Status](https://travis-ci.org/pioole/TAS.svg?branch=master)](https://travis-ci.org/pioole/TAS)
development: [![Build Status](https://travis-ci.org/pioole/TAS.svg?branch=develop)](https://travis-ci.org/pioole/TAS)

prerequisites:

    python2.7.x installed with according pip
    In project root:
    $ pip install -r requirements  # matplotlib module was tested with TkAgg backend
    $ cd src
    $ export PYTHONPATH=$(pwd)/..:PYTHONPATH

running:

    $ python Simulation.py

configurability:

    To configure simulation options use the defined values in Simulation.py file accordingly:

    CLUSTER_SIDE_LENGTH
        defaults to 24, defines the length of the single cluster side
    LOGGING_LEVEL
        defaults to logging.INFO, logger level, choose from: CRITICAL, ERROR, WARNING, INFO, DEBUG
    CROP
        defaults to 3000, it's the maximum size of generated job. if set to 100, there will be no job created bigger than 100.
    BACKFILLING_LEVEL = 1
        choose from {1, 0}, turns on backfilling
    FITTING_STRATEGY = Cluster.FittingStrategy.best_fit
        Tasks to bins fitting strategy. Choose from Cluster.FittingStrategy.biggest_fit, Cluster.FittingStrategy.smallest_fit, Cluster.FittingStrategy.best_fit
    MAX_JOB_SIZE
        Maximum size of the job elligible for backfilling, defaults to 500
    BUFFER_SIZE
        Size of the job buffer available for backfilling, defaults to 1100
    ITERATIONS
        Number of iterations to run
    PLOTTING
        Choose from True, False. Enables visualization.

