"""Manual car control demonstration without AI.

Provides a simple example of MovementSimulation where the user can manually
drive a car around the track using WASD controls. Useful for:
- Testing car physics and controls
- Understanding track layouts
- Debugging collision detection
- Demonstrating basic functionality
"""

from ai_navigation.src.simulation.movement_simulation import MovementSimulation


def main() -> None:
    """Run the manual movement simulation on track 0."""
    ts = MovementSimulation(road_index=0)
    ts.run()


if __name__ == "__main__":
    main()
