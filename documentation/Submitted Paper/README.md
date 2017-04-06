Journal X -- reproducing Figure 3b
===

This is an example of application of ABBAS that reproduces the first result shown in Figure 3 from our [recent paper](https://www.researchgate.net/publication/315096594_Task_allocation_and_site_fidelity_jointly_influence_foraging_regulation_in_honey_bee_colonies) (currently under review). We will go through the process of running a [sample script](./Sample_script.py) and plot the result without assuming expert knowledge in Python.

We assume that Python is installed, as well as the dependencies described in [here](https://github.com/VandroiyLabs/ABBAS). We will update this section with more details as soon as our paper is accepted.


Setting up the simulation parameters
---

In the [sample script](./Sample_script.py), between lines 8 and 16 the model parameters are defined. However, you will not need to change the code itself. They will be defined when you run this script. The more general idea is:
```
python Sample_script.py <TotalForagers> <NumScouts> <PerScouts> <PerRec> <NumPatches>
```
where 
* ```<TotalForagers>``` = Total number of foragers in the hive
* ```<NumScouts>``` = Number of scouts
* ```<PerScouts>``` = Persistence of scouts
* ```<PerRec>``` = Persistence of recruits
* ```<NumPatches>``` = Number of patches to be explored

For instance, if you want to simulate a hive with 300 foragers, with 30 scouts (i.e., 10% of foragers are scouts), setting the persistence of all foragers to 1 and 3 patches, all you need to do is to run the script using the following command:
```
python Sample_script.py 300 30 1 1 3
```

Running a few simulations
---

By default, the sample script will create ```nreps``` ( = 20 by default for this example) files. Each file contains the results of a completely independent simulation using the same parameters. This allows you to estimate with enough accuracy to study the time evolution of the total amount of food retrieved by the foragers. Each line of the log files represent the measures of various variables as a function of time. 

To reproduce Figure 3b, you will need to run three simulations:
```
python Sample_script.py 300 30 20 20 3
python Sample_script.py 300 150 20 20 3
python Sample_script.py 300 270 20 20 3
```
This may take a few minutes in a personal computer. 


Plotting results
---

After the simulation is finished, you should have a folder with 60 log files. 
