from simulation import AiSimulation



if __name__ == "__main__":
    conf = {
        "road_index": 2,
        "show_active_fitness_lines": True,
        "show_car_vision": False,
        "show_all_fitness_lines": False,
        "show_parent": True,
        "save_best_genome": False,
        "reverse_fitness_lines": True,
    }
    ai_simulation = AiSimulation(**conf)
    ai_simulation.run();
    

