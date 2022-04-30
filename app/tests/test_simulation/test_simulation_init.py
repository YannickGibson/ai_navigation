

from app.src.simulation.movement import Simulation


def test_simulation():
    s = Simulation(0)
    assert( 0 == s.car.acc )