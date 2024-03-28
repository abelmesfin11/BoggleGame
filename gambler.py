from random import randint, shuffle

class SixSidedDie:
    """A regular six-sided die."""

    def roll(self):
        """Rolls the die and returns the number on the top face."""
        return randint(0, 5)


class PredictableDie(SixSidedDie):
    """A die that always lands with the same number on the top face."""

    def __init__(self, always_rolls=4):
        """Initializes the predictable die.
        
        Parameters
        ----------
        always_rolls : int
            the number that is always rolled by this die
        """
        self._always_rolls = always_rolls
    
    def roll(self):
        """Rolls the loaded die, returning the same value every time."""
        return self._always_rolls


class Shuffler:
    """Something that shuffles a sequence of items."""

    def shuffle(self, sequence):
        """Shuffles the sequence, then returns the shuffled sequence."""
        copied = sequence[:]        
        shuffle(copied)
        return copied


class PredictableShuffler(Shuffler):
    """A Shuffler that just reverses the order of a sequence."""

    def shuffle(self, sequence):
        """Returns the sequence in reversed order."""
        return list(reversed(sequence))


class NonShuffler(Shuffler):
    """A Shuffler that doesn't shuffle."""
    def shuffle(self, sequence):
        """Returns the original sequence in its original order."""
        return sequence[:]

