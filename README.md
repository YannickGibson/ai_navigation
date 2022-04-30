# AI Bug Race

## Overview
A simulation of a race game using natural selection algorithm *NeuroEvolution of Augmented Topologies*, **NEAT** in short.

The goal of an agent is to travel the most the distance in shortest amount of time in direction of a road without hitting the edges.

## Instalation
- Download or clone the repository
- Navigate to the root of the repository
- Create and activate a virtual environment and install packages (see bellow)

Linux
```ps1
virtualenv venv
venv/bin/activate
pip install -r .\requirements.txt
```
Windows
```ps1
virtualenv venv
venv\Scripts\activate.ps1
pip install -r .\requirements.txt
```


## Execution
A user can freely control an unit if the program is run from `__main_movement__.py` else if the program is run from `__main_ai__.py` you need to make sure that the config value `let_me_drive` is set to  `True`
  
Run the program from the root directory, e.g.:
```ps1 
python __main_ai__.py
```

## Controls
User can control an unit with `WSAD` keys, it's meant only as a demonstration as to how it feels to be an agent.
To skip a generation you can press the `Del` button, meant to manualy speed up the natural selection process (bevare; the next generation is derived from the one that was terminated).

Program can be launched:
- as an AI simulation `__main_ai__.py`
- as a movement simulation `__main_movement__.py`
  
# AI Config 

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
        - saves the most prominent genome as a `pickle` to `utils/genomes` directory 
- *reverse_fitness_lines* 
        - makes agents compete in the opposite direction 
- *let_me_drive* 
        - allows user to try what it feels like to be an agent
- *max_frames_elapsed* 
        - determines after how many frames will simulation start a new generation
- *no_progress_frames_elapsed* 
        - determines after how many frames of agents not crossing *fitness lines* in the forward direction will the simulation start a new generation

## Tests
Unit-tests are checking the core functionality of the program, tests run on majority of functions and methods. Tests can be run with the `pytest` command.