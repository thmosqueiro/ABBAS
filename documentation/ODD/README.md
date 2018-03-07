# ODD: Simulation of honey bees foraging

This description of a model of honey bees foraging published in the paper [Mosqueiro et al. (under review) 2017.](https://www.researchgate.net/publication/315096594_Task_allocation_and_site_fidelity_jointly_influence_foraging_regulation_in_honey_bee_colonies) follows the **O**verview, **D**esign Concepts and **D**etails (ODD) protocol. To write this document, we followed the guidelines presented in [Grimm et al. (Ecological Modelling 2010)](http://linkinghub.elsevier.com/retrieve/pii/S030438001000414X). We have been including questions that colleagues and interested researchers have asked us as we receive them to make this ODD document as complete and useful as possible.

The source code of our implementation is available in this GitHub repository. Comments and suggestions are welcome. Feel free to open an [Issue](https://github.com/VandroiyLabs/ABBAS/issues) or create a Pull Request.

> **Reference paper:** Mosqueiro, Cook, Huerta, Gadau, Smith, Pinter-Wollman. **Task allocation and site fidelity jointly influence foraging regulation in honey bee colonies.**  [Published in Royal Society Open Science (2017).](https://www.researchgate.net/publication/315096594_Task_allocation_and_site_fidelity_jointly_influence_foraging_regulation_in_honey_bee_colonies)

### Table of contents

* [**Overview**](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#overview)
  * [Purpose](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#purpose)
  * [For whom is this model designed?](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#for-whom-is-this-model-designed)
  * [What kind of entities are in this model?](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#what-kind-of-entities-are-in-this-model)
  * [How is space included in this model?](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#how-is-space-included-in-this-model)
  * [By what attributes are these agents characterised?](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#by-what-attributes-are-these-agents-characterised)
  * [Units](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#units)
  * [Implementation](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#implementation)
  * [Process overview and scheduling](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#process-overview-and-scheduling)  
* [**Design concepts**](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#design-concepts)
  * [Basic principles]()
  * [Adaptation](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#adaptation)
  * [Prediction](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#prediction)
  * [Sensing](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#sensing)
  * [Interaction](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#interaction)
  * [Stochasticity](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#stochasticity)
  * [Collectives](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#collectives)
  * [Observation](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#observation)
* [**Details**](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#details)
  * [How was the model implemented?](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#how-was-the-model-implemented)
  * [Initialization](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#initialization)
  * [Input data](https://github.com/thmosqueiro/ABBAS/blob/master/documentation/ODD/README.md#input-data)


<br />

# Overview

## Purpose

The purpose of this model is to study the impact of colony-level distribution among tasks and behavioral persistence of individuals on the collective tradeoff between exploring for new resources and exploiting familiar ones. With this model, we can generate new hypotheses for further empirical work on the regulation of collective behavior and its response to various environment conditions.

We have prepared a video with our model in action. Click in the image below to watch it on YouTube.

[![Animated gif from the video](https://raw.githubusercontent.com/VandroiyLabs/ABBAS/master/documentation/ODD/video.gif)](https://www.youtube.com/watch?v=_hZGlT_luLI)

We have animations rendered for some of the scenarios explored in our paper, however we are still uploading those.


## For whom is this model designed?

This model was designed for ecologists and computational biologists interested in foraging behavior of honey bee colonies. We chose design principles that allow anyone with minimal knowledge in Python to reproduce our results and create their own simulations.


## What kind of entities are in this model?

Entities (or agents) are honey bee foragers, divided into two groups: scouts and recruits. Scouts spontaneously leave the hive and explore the environment. Once a food patch is discovered, scouts report its location to recruits which then may choose to leave the hive to exploit that food patch.


## How is space included in this model?

The environment is a square, bidimensional, continuous space of sides 36m (or 1.3 km2 in total area). The hive was always positioned at the origin of the space. Bees were free to fly throughout the entire arena, however when they reached the borders, they were brought back to the hive. The position of the resource points was stored in a grid to simplify computations.


## By what attributes are these agents characterised?

The following variables characterized each agent. The values introduced below match the software implementation of this model.

* Position, given by a vector (x,y). The position is measured with respect to the hive, located at the (0,0).

* Drifting vector, which defines the preferred direction of movement in flight.

* Location of a previously visited resource.

* Each bee is permanently assigned as either scout or recruit.


## Units

All units were chosen to fit 7h of total simulation and an total area of 36 x 36 m2.

* 1 unit of space is approximately 70cm.

* 1 unit of time is approximately 1.2s

* Each bee carries one unit of resource, which is converted to 1 mililitter of sucrose.


## Implementation

ABBAS is implemented to support parallelization and evaluates statistics of the simulated system the on-the-fly to define stopping criteria.


#### Is the model implementation accessible to anyone?

Yes, the source code of our model can be found on [Github](./). You can also find an example that reproduces one of our figures of our paper [here](./).

#### Are special libraries needed?

Because we used Python and popular libraries (such as numpy, scipy and matplotlib), the core of this implementation is independent of platform and should run on most computers with Python. It was, however, never tested in Windows machines. We are currently working to upload a newer version that offers automatic dependency checking with pip. If you have feedback, feel free to create Issues or Pull Requests in the main repository.


## Process overview and scheduling

Although time is considered continuous, we used the Euler–Maruyama method to synchronously solve the stochastic differential equation that defined the flight dynamics for each bee. We summarize below how bees behaved.

#### Scouts with persistence P.

1. Leave the hive with a randomized drifting vector.

2. If a resource is found, grab one unit of resource (1ml of succrose) and return to the hive

3. Remain in the hive for 50 time steps. During this period, this bee is reporting the position of that resource to available recruits.

4. Go back to the same resource spot P times.

5. Go back to step (1).


#### Recruits with persistence P

1. Stay in the hive.

2. Randomly decide to leave the hive to exploit a particular resource (see section Interactions for details).

3. Choose one of the reported locations as its new drifting vector.

4. Leave the hive to look for that resource spot for P+1 times.

5. Each time, grab a unit of resource and bring it back to the hive.

5. Go back to step (1).


#### How is time modeled?

Time is continuous. Flight dynamics follow a diffusion process modeled by a [Wiener process](https://en.wikipedia.org/wiki/Wiener_process), integrated using the Euler–Maruyama method.


#### In what sequence are model entities processed?

In each time step, all entities (foragers) are updated at the same time and synchronously.


#### When are state variables updated?

Depending on each state variable, they are updated in different moments.

* Positions of each bees are updated every time step.

* Drifting vector of each bee is only updated when they leave the hive to exploit a particular resource spot for the first time.

* Task assignment (scout vs. recruit) is never changed throughout the simulations.

* The average velocity of scouts is updated to that of recruits whenever it is exploiting a particular resource.


<br />

<br />

# Design concepts

## Basic principles

This model explores the joint impact of task allocation and behavioral persistence in the foraging performance of the colony. Each group of foragers (scouts and recruits) perform different tasks, each contributing to exploration and exploitation. Our model incorporates how scouts communicate to recruits the direction, distance, and quality of newly found resources ([waggle dance](https://en.wikipedia.org/wiki/Waggle_dance)). This strategy reduces waste of energy spent when searching for food, and also prevent dangers such as predation. Behavioral persistence changes how many trips foragers will make back and forth to a resource spot. This model also incorporates flight precision observed in field experiments.


#### How was recruitment taken into account?

Honey bees recruit foragers using the [waggle dance](https://en.wikipedia.org/wiki/Waggle_dance). You can see honey bees performing the waggle dance in [this video](https://www.youtube.com/watch?v=bFDGPgXtK-U), published by Georgia Tech College of Computing. In our model, this mechanism was modeled by making a recruiting forager (scout or recruit) communicate the location where a resource was found to a new recruit. This recruit will then set its drifting vector to that location and leave the hive.


#### Will the model provide insights about the basic principles themselves?

The model predicts that behavioral persistence and task allocation jointly influence the performance of a honey bee colony during foraging. In particular, for each value of persistence, there is a ratio between scouts and recruits that optimize the foraging performance of a colony. The model also predicts that changing the persistence of recruits induces a stronger impact in the colony performance.


## Adaptation

#### What adaptive traits do the individuals have?

Recruits and scouts that are returning to a particular resource spot had lower dispersion than that of scouts exploring the environment. This difference takes into account that bees that are exploiting a resource patch are familiar with its location, and thus faster and more precise than those that are exploring the environment. Values used follow previous experiments and theoretical works.

#### Do these traits explicitly seek to increase some measure of individual success regarding its objectives?

The adaptive precision described in the previous question increases the chances of a bee to find new resource spots when exploring the environment, while also increasing the chances of bees returning to the same location with resources available. However, a remarkable precision in the flight patterns of recruited bees is empirically observed in many contexts, with errors of 5% over distances of 4km.


## Prediction

No predictive models were employed in the decision-making processes involved in our model. For instance,

* recruits decide to leave the hive randomly;
* foragers decide to quit exploiting resources according to their persistence, which is fixed.


## Sensing

#### What state variables of which other individuals can an individual perceive?

When a forager reports to other recruits the location of a resource spot, recruits that decide leave the hive and exploit that spot then have access to ("perceive," in an ODD language) the location of that spot.

#### How do honey bees sense the resources?

Once a honey bee is within 1 unit of distance (~70cm) from a resource spot, it was able to sense it and, therefore, grab 1 unit of food (1ml of sucrose).


## Interaction

#### What kinds of interactions among agents are assumed?

Bees only interact by during the recruitment process.


#### If the interactions involve communication, how are such communications represented?

The drifting vector of recruits that decide leave the hive and exploit a spot reported by another forager is set to the location of that spot, provided by the reporting forager.


## Stochasticity

There are four stochasticity elements in this model: assignment of the drifting vector, the flight dynamics, how recruits decide to exploit resources, and how the environment is created.

#### The angle of the drifting vector of scouts was assigned uniformly.

Because the drifting vector of model bees define their preferred direction of flight, by drawing their angle from a uniform distribution between 0 and 2pi then all the area was eventually covered. The magnitude of the vector was always the same to guarantee the same average velocity.

#### The flight dynamics follows a diffusion process.

Each bee follows a . This diffusion process is usually referred to as [Wiener process](https://en.wikipedia.org/wiki/Wiener_process), which is a particular case of a Random Walk. On top of this diffusion process, bees had a preferred direction of movement determined by their drifting vectors. The final dynamics is shown in the figure below.

#### Recruits decides stochastically to start foraging

Each recruit independently decided to leave the hive with a probability rate of p(t)/dt, where p(t) is a probability that varies with time.

* p(t) = 0  &nbsp;&nbsp;&nbsp; if no forager are dancing at time t.

* p(t) = K / Nr &nbsp;&nbsp;&nbsp; otherwise, where Nr is the number of available recruits and K is a free parameter.

By defining p(t) this way, then the number of recruits that each forager recruited per trip is approximately K x Td, where Td is the time each forager remained dancing (50 unit steps). The effect of K on the colony outcome was studied in our  Supplemental Material (Figure S3).

#### Recruits stochastically decide which recruiting forager to follow.

After decided to leave the hive to forage, recruits chose randomly which of the reported resource locations, with equal likelihood to each possible location.


#### The environment is created with a stochastic process.

In all experiments reported, we used an environment with three patches of resources. Each patch was composed of points uniformly distributed along a square area (see figure below). All patches were equally distant from the hive.  The effect of a larger number of patches was explored in the Supplemental Material (Figure S6).


## Collectives

#### Do the individuals form or belong to aggregations that affect, and are affected by, the individuals?

All bees belong to a hive. Foraging performance is calculated as the total amount of resources collected by all bees, regardless of their assignment as scout/recruit.

#### Is a particular collective an emergent property of the individuals?

No, each bee is assigned a task (scout/recruit) and will behave accordingly throughout the whole simulation.


## Observation

#### What data are collected from the ABM for testing, understanding, and analyzing it?

The data collected from the model is the total amount of resources collected by all bees throughout the whole simulation.


#### How and when is the total amount of resources collected?

The total amount of resources collected was calculated as simply the total number of resources collected throughout the whole simulation. Each bee was allowed to bring back to the hive 1 unit of resource per trip. Because bees usually retrieve about 1ml of sucrose per trip in experiments, this total amount of resources collected is measured in milliliters without any need for conversion.

#### Are all output data freely used, or are only certain data sampled and used?

All data was used.


<br />

<br />

# Details

## How was the model implemented?

The model was implemented using a parallel framework developed in Python which we refer to as ABBAS.


## Initialization

#### Do all honey bees always start at the same location?

Yes, the simulation starts with all honey bees inside the hive. In the first iteration, random drifting vectors are assigned to each scout. All recruits remain in the hive until become recruited by a scout.

#### Is the environment exactly the same?
No. Given a fixed number of patches, each patch is formed by a Poisson Point Process and thus changes. The average number of resource points in each patch can be easily evaluated.



## Input data

For each simulation, there is no need for any data other than the following parameters:

* Persistence of each bee (or group of foragers)

* Total time of simulation

* Spatial distribution of the resources

* Number of foragers and number of scouts
