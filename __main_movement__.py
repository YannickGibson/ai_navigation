from app.src.simulation.movement import MovementSimulation
def main():
    ts = MovementSimulation(road_index=0)
    ts.run()

if __name__ == "__main__":
    main()

