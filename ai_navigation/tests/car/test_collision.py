"""Unit tests for Car collision detection.

Tests cover:
- Collision detection with track boundaries
- Line segment intersection calculations
- Edge cases for collision geometry
"""

from ai_navigation.src.car import Car


def sample_road():
    """Generate a sample race track for collision testing.

    Returns:
        tuple: Inner and outer track boundaries as lists of (x, y) coordinates

    """
    return (
        [
            (271, 320),
            (294, 211),
            (359, 155),
            (464, 153),
            (596, 150),
            (718, 116),
            (829, 112),
            (945, 113),
            (1062, 127),
            (1136, 146),
            (1207, 253),
            (1264, 313),
            (1263, 408),
            (1253, 447),
            (1168, 442),
            (1073, 403),
            (1011, 380),
            (976, 279),
            (873, 212),
            (710, 210),
            (568, 263),
            (518, 368),
            (468, 482),
            (390, 494),
            (328, 451),
            (287, 410),
            (269, 368),
            (271, 320),
        ],
        [
            (151, 320),
            (176, 191),
            (255, 95),
            (386, 61),
            (536, 46),
            (698, 60),
            (819, 52),
            (955, 53),
            (1082, 71),
            (1174, 100),
            (1345, 137),
            (1444, 313),
            (1441, 440),
            (1391, 563),
            (1230, 612),
            (1011, 573),
            (955, 400),
            (864, 321),
            (781, 290),
            (668, 322),
            (610, 375),
            (610, 446),
            (580, 524),
            (482, 572),
            (328, 571),
            (209, 502),
            (157, 410),
            (151, 320),
        ],
    )


def sample_fitness():
    return [
        ((271, 320), (151, 320)),
        ((294, 211), (176, 191)),
        ((359, 155), (255, 95)),
        ((464, 153), (386, 61)),
        ((596, 150), (536, 46)),
        ((718, 116), (698, 60)),
        ((829, 112), (819, 52)),
        ((945, 113), (955, 53)),
        ((1062, 127), (1082, 71)),
        ((1136, 146), (1174, 100)),
        ((1207, 253), (1345, 137)),
        ((1264, 313), (1444, 313)),
        ((1263, 408), (1441, 440)),
        ((1253, 447), (1391, 563)),
        ((1168, 442), (1230, 612)),
        ((1073, 403), (1011, 573)),
        ((1011, 380), (955, 400)),
        ((976, 279), (864, 321)),
        ((873, 212), (781, 290)),
        ((710, 210), (668, 322)),
        ((568, 263), (610, 375)),
        ((518, 368), (610, 446)),
        ((468, 482), (580, 524)),
        ((390, 494), (482, 572)),
        ((328, 451), (328, 571)),
        ((287, 410), (209, 502)),
        ((269, 368), (157, 410)),
    ]


def test_collide_0() -> None:
    road = sample_road()
    c = Car(10, 100, 60)
    assert not c.collides(road)


def test_collide_1() -> None:
    road = sample_road()
    c = Car(130, 310, 90)
    assert c.collides(road)


def test_collide_2() -> None:
    road = sample_road()
    c = Car(130, 310, 0)
    assert not c.collides(road)


def test_collide_fitness_0() -> None:
    fitness_lines = sample_fitness()
    c = Car(130, 310, 0)
    c.acc = 1
    c.rotate_by(5)
    c.move()
    c.move()
    c.vision_distance(sample_road())
    assert not c.collide_fitness(*fitness_lines[0])


def test_collide_fitness_1() -> None:
    """Tests fitness collision after car movement."""
    # Arrange
    fitness_lines = sample_fitness()
    c = Car(280, 312, 20)
    FITNESS_POINT_DIMENSIONS = 2

    # Act
    c.acc = 1
    c.rotate_by(-5)
    c.move()
    c.move()
    initial_fitness_point = c._fitness_point
    c.vision_distance(sample_road())
    fitness_point_len = len(c._fitness_point)
    collision_result = c.collide_fitness(*fitness_lines[0])

    # Assert
    assert initial_fitness_point is None
    assert fitness_point_len == FITNESS_POINT_DIMENSIONS
    assert not collision_result


def test_vision() -> None:
    """Tests car vision system returns correct number of points."""
    # Arrange
    c = Car(0, 0, 0)
    EXPECTED_VISION_COUNT = 8
    EXPECTED_RIGHT_VISION_X = 404.0

    # Act
    vision = c.get_vision(sample_road())

    # Assert
    assert len(vision) == EXPECTED_VISION_COUNT
    assert vision[1][0] == EXPECTED_RIGHT_VISION_X
