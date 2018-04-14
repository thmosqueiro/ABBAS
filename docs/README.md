[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.843517.svg)](http://dx.doi.org/10.5281/zenodo.843517)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
<img src="https://img.shields.io/badge/Python-_2.7-brightgreen.svg">

To examine the impact of individual variations in foraging behaviors, we
developed a spatially-explicit Agent-Based Model. ABBAS (Animal Behavior Based
on Agents Simulations) is a free software that simulates honey bees foraging in
a bidimensional space using Python's standard numerical libraries. It implements
a detailed flight dynamics based on stochastic diffusion processes, parametrized
following a wide range of experiments (see below for more details), and a
recruitment mechanism that mimics the [waggle dance in honey
bees](https://en.wikipedia.org/wiki/Waggle_dance). Foragers were divided into
two groups, scouts and recruits, with each group having their own properties.
ABBAS provides an API to control the properties of each group easily and
schedule batches of simulations.


[![Animated gif from the video](video.gif)](https://www.youtube.com/watch?v=_hZGlT_luLI)

The current version of this software (v1.0) was used in a [recent
paper](https://github.com/VandroiyLabs/ABBAS#relevant-papers) was used to study
the joint impact of task allocation and behavioral persistence on collective
behavior.


#### We also [provide here](ODD/README.md) a description of our model using the Overview, Design concepts, and Details (ODD) protocol.


<br />

## Relevant publications

If you find this useful, please [star this repository](https://github.com/thmosqueiro/ABBAS/stargazers) and/or cite our paper:

* Mosqueiro, Cook, Huerta, Gadau, Smith, Pinter-Wollman **Task allocation and site fidelity jointly influence foraging regulation in honeybee colonies.** [Royal Society Open Science 4:170344 (2017). DOI: 10.1098/rsos.170344](http://rsos.royalsocietypublishing.org/content/4/8/170344) (there was a [preprint](https://www.researchgate.net/publication/315096594_Task_allocation_and_site_fidelity_jointly_influence_foraging_regulation_in_honey_bee_colonies) available too).

* **Dataset:** Cook, Mosqueiro, Huerta, Gadau, Smith, Pinter-Wollman **Task allocation and site fidelity jointly influence foraging regulation in honeybee colonies.** [Available on FigSahre. DOI: m9.figshare.3619779.v1](https://figshare.com/articles/Task_allocation_and_site_fidelity_jointly_influence_foraging_regulation_in_honey_bee_colonies/3619779).


<br />

## Sample code

As an example of how to use ABBAS, [we provide a sample code that
reproduces Figure 3a from our
paper](https://github.com/VandroiyLabs/ABBAS/tree/master/documentation/Submitted%20Paper).
In this example,

* we set up an environmentwith an initial amount of resources,

* set up the hive (number of foragers, number of scouts, how persistent they are, etc),

* and simulate in parallel instances of the same scenario to estimate how much
* food the bees collected (collective outcome).

We then compile all of these results, estimating the average and standard
deviation of the collected food as a function of time. We finish with a fuzzy
plot of the average amount of resource collected and 1.5 standard deviations as
a function of time.


<br />

## Dependencies

This software uses Python 2.7*. We list below the required Python libraries that
are non-standard:

* numpy 11.*+
* multiprocessing
* subprocess
* pickle


To create the videos:

* matplotlib 1.10+
* ffmpeg 3.0.*


## License

This software is distributed under the [GPL-3
license](https://choosealicense.com/licenses/gpl-3.0/). Read the full terms are
provided in the
[LICENSE](https://github.com/VandroiyLabs/ABBAS/blob/master/LICENSE) file.

tl;dr version: You **can** run, distribute, study, copy and improve as long as
you keep the original license. If you modify it, you **must** share your
improvements under GPL-3. Just remember **not to sue** us if anything goes wrong
with the code. We would, of course, appreciate if you leave a star in our
original repository to show your support.


For a summary (boilerplate):

```
ABBAS (Animal Behavior Based on Agents Simulations) simulates honey bees
foraging as agents in a two-dimensional space.
Copyright (C) 2016  Thiago Mosqueiro, Noa Pinter-Wollman, Ramon Huerta,
Chelsea Cook, Jürgen Gadau, Brian Smith

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
```
