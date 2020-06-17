from random import Random


def make_rng(seed: int = None) -> Random:
    rng = Random()
    rng.seed(rng.randint(0, 100000000) if seed is None else seed)
    return rng
