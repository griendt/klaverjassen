from random import Random


def make_rng(seed: int = None) -> Random:
    """
    Initialize a random number generator.

    :param seed: Optional. If specified, initialized a random number generator with the given seed.
    This is useful for example to recreate specific random rolls.
    :return: The created random generator.
    """
    rng = Random()
    rng.seed(rng.randint(0, 100000000) if seed is None else seed)
    return rng
