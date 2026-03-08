# AI Navigation

## Overview
The project lets agents learn to drive through a race track using the natural selection algorithm [*NeuroEvolution of Augmented Topologies (NEAT)*](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies).

The goal of an agent is to travel the most distance in the shortest amount of time without hitting the edges.


## Demonstration
### Learning

https://user-images.githubusercontent.com/57909721/221156472-658bc087-ec96-46c6-9bbf-49ac21720dda.mp4

### A few generations after


https://user-images.githubusercontent.com/57909721/221156559-17dda8a0-479e-408f-ab17-b3ede70fe7da.mp4



## Instalation
Create a virtual environment

Using Anaconda
```bash
conda create -n ai-navigation
conda activate ai-navigation
pip install .
```
Using `virtualenv`
```bash
virtualenv venv
venv/bin/activate
pip install .
```



## Execution
To be able to control an agent in the interactive mode of the app (`interactive_training.py`), the value `let_me_drive` needs to be set to `True` (it is on by default). To test out the movement mechanics alone you can run the  `only_movement.py` file. 
  
Run the a simulation using
```bash
python examples/interactive_training.py
```
or for movement only run the following
```bash
python examples/only_movement.py
```

## Controls
User can control his agent with `WSAD` keys, it is meant only as a demonstration as to how it feels to be an agent.
To skip a generation you can press the `Del` button, meant to manualy speed up the natural selection process (bevare; the next generation is derived from the one that was terminated).
  
# Interactive Config 

- *road_index*
        - index of road pre-saved as a `pickle` 
- *show_active_fitness_lines*
        - shows where is the agent currently earning fitness
- *show_car_vision* 
        - shows how far is the wall (main information inputed into net)
- *show_all_fitness_lines* 
        - shows where all the *fitness lines*
- *show_parent* 
        - highlights most prominent genome (doesn't guarantee reproduction)
- *save_best_genome* 
        - saves the most prominent genome as a `pickle` to `data/genomes` directory 
- *reverse_fitness_lines*
        - makes agents compete in the opposite direction 
- *let_me_drive* 
        - allows user to try what it feels like to be an agent
- *max_frames_elapsed* 
        - determines after how many frames will simulation start a new generation
- *no_progress_frames_elapsed* 
        - determines after how many frames of agents not crossing *fitness lines* in the forward direction will the simulation start a new generation

## Tests
Unit-tests are checking the core functionality of the program and run on majority of functions and methods. Tests can be run with the `pytest` command. Make sure you have the test option installed using `pip install .[test]`.


### Mechanics


https://user-images.githubusercontent.com/57909721/221157183-5c3ab07f-14ad-4eb9-a4e6-bfed62e60cf0.mp4

