SimuQoS
=======

SimuQoS is a Python QoS simulator with a lot of parameters for trade and preview of peers.

It's consists of two main controllers:

	1. MainController thats run the simulations and store the results
	2. ResultadoController thats get results of simulations, group and plot graphs

If you run Main.py without parameters, the ResultadoController will be called, else MainController

Dependencies
=======
	1. scipy (Ubuntu-like: sudo apt-get install python-scipy)
	2. matplotlib (Ubuntu-like: sudo apt-get install python-matplotlib)
	3. numpy (Ubuntu-like: sudo apt-get install python-numpy)

Usage
=======
There is a example teste.sh file inside teste folder that use the simulator with some parameters and run graphs at the end.

usage: python Main.py Q P L S A C N T R V Y X D

Parameters
=======
    * Q = number of peers (only integer)
    * P = peers playlist size (only integer)
    * L = peers file list size (only integer)
    * S = system file list size (should be bigger than L and integer) 
    * A = size of system files (only A = unitario)
    * C = peers pairing type (only C = aleatorio)
    * N = number of peers trade at each pairing (only integer)
    * T = trade type (only T = sequential ou T = aleatory)
      	* sequential it's trade following the peer playlist order
      	* aleatory it's trade the first playlist file the peer found 
    * X = download rate (only integer 1 - 100)
    * V = number of timeslots (only integer)
    * Y = preview type (only Y = sequential ou Y = aleatory)
       	* sequential it's preview files following playlist's order
       	* aleatory it's preview the first file avalible at playlist
    * R = preview rate (only integer 1 - 100)
    * D = timeslot delay to start preview (only integer) 