[GC3Pie](http://gc3pie.googlecode.com/) is a Python framework for
orchestrating the execution of external commands over diverse computing
resources. You write a description of your workflow using a set of
Python objects, and GC3Pie translates it into commands appropriate for
the accessible computing resources. Currently, **GC3Pie** can execute
processes on cloud-based VMs, batch-queueing clusters, computational
Grids, and -of course- any Linux/UNIX host where you can SSH into.


### For the computational scientist ###

There is often the need in computational science to run massive job
campaigns, e.g., executing the same algorithm over a large number of
inputs, or sweeping an entire parameter set in the search for the
optimal configuration. [GC3Pie](http://gc3pie.googlecode.com/) can ease
rapid development of such analysis scripts, and provides the facilities
you want for production runs, such as checkpoint/restart, load balancing
across resources, retry-on-failure, etc.


### For the Python programmer ###

You can think of [GC3Pie](http://gc3pie.googlecode.com/) as
**[subprocess](http://docs.python.org/2/library/subprocess.html) on
steroids:** where `subprocess` runs an external command on the same
computer where your Python script is running, **GC3Pie** can distribute
execution to several computing resources in parallel, including spawning
cloud-based VMs on demand. In addition, **GC3Pie** provides facilities for
building workflows and specifying dependencies between external
processes, saving computational jobs (or more generally Python objects)
to filesystem-based storage and SQL tables, retrying failed commands on
failure, etc.


### For the high-throughput computing specialist ###

[GC3Pie](http://gc3pie.googlecode.com/) has some distinctive features
over other high-throughput libraries:

  * the description of computational jobs is done via Python objects
  * workflows are created by composing Python objects
  * the same Python code can submit jobs to a wide variety of resources, including cloud-based resources (spawned on demand) and Grid resources
  * support for authentication and checkpoint/restart of workflows is part of the core library

If you are interested, feel free to browse through the tutorial\