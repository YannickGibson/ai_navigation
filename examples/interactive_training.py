"""Interactive AI training example with manual car control.

Demonstrates TrainSimulation with all visualization options enabled including:
- Active fitness checkpoint visualization
- Car vision sensor display
- All fitness lines visible
- Champion highlighting
- Manual driving alongside AI cars

This configuration is useful for observing and understanding how the AI learns
to navigate the track over generations.
"""

from ai_navigation.src.simulation.train_simulation import TrainSimulation

if __name__ == "__main__":
    conf = {
        "road_index": 3,
        "show_active_fitness_lines": True,
        "show_car_vision": True,
        "show_all_fitness_lines": True,
        "show_parent": True,
        "save_best_genome": False,
        "reverse_fitness_lines": True,
        "let_me_drive": True,
        "max_frames_elapsed": 1000,
        "no_progress_frames_elapsed": 50,
    }
    ai_simulation = TrainSimulation(**conf)
    ai_simulation.run()
