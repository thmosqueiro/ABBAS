ABBAS
===

Animal behavior based on agents simulation


Relevant papers
---

If you find this useful, please star this repository and/or cite our paper:

Thiago Mosqueiro, Chelsea Cook, Ramon Huerta, Jürgen Gadau, Brian Smith, Noa
Pinter-Wollman. **Task allocation and site fidelity jointly influence foraging
regulation in honey bee colonies.** [Under review.] ()


Sample code
---

As an example of how to use ABBAS can be applied, we provide a sample code that
reproduces Figure 3a from our paper. In this example,

* we set up an environmentwith an initial amount of resources,

* set up the hive (number of foragers, number of scouts, how persistent they are, etc),

* and simulate in parallel instances of the same scenario to estimate how much
* food the bees collected (collective outcome).

We then compile all of these results, estimating the average and standard
deviation of the collected food as a function of time. We finish with a fuzzy
plot of the average amount of resource collected and 1.5 standard deviations as
a function of time.



Dependencies
---

This software uses Python 2.7*. We list below the required Python libraries that
are non-standard:

* numpy 11.*+
* multiprocessing
* subprocess
* pickle


To create the videos:

* matplotlib 1.10+
* ffmpeg 3.0.*


License
---

This software is distributed under the [GPL-3
license](https://choosealicense.com/licenses/gpl-3.0/). Read the full terms are
provided in the
[LICENSE](https://github.com/VandroiyLabs/ABBAS/blob/master/LICENSE) file.

tl;dr version: You **can** run, distribute, study, copy and improve as long as
you keep the original license. If you modify it, you **must** share your
improvements under GPL-3. Just remember **not to sue** us if anything goes wrong
with the code. We would of course appreciate if you leave a star in our original
repository to show your support.


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
this program.  If not, see
[<http://www.gnu.org/licenses/>](http://www.gnu.org/licenses/).
```
