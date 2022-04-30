from app.src.simulation.ai import AiSimulation



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
        "no_progress_frames_elapsed": 50

    }
    ai_simulation = AiSimulation(**conf)
    ai_simulation.run();
    

