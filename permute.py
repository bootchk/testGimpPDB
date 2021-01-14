"""
A singleton class that generate permutations of arguments.

Methods generate from a range.
The range generally tests limits, aka edge cases.

See elsewhere, we might be testing:
- until a first success (shallow test that some normal Gimp code path succeeds )
- the full range (for crashes)

Methods return quoted strings.

TODO make this generate permutations in order,
instead of more or less random permutations.

??? If the sequences are all different cardinality, primes,
given enough calls, it would generate all permutations?
"""

from itertools import cycle



class Permute():

    """
    Iterators of kind 'cycle'

    Shared by many generators.
    Generally only one generator is used at a time?
    Else this will not be truly stochastic, a generator would repeat a single value.

    !!! The design of the finite sequence is important.
    It CAN include large values to cover edge cases.

    But large values for parameters CAN affect duration of a test.
    For example, if 256 is passed as "number of rows" to script-fu-erase-rows,
    it executes a long time.
    So the sequence should start with many small values so that
    a test is more likely to pass args of small values that succeed,
    before passing large values that might  take a long time.
    """

    intIter = cycle(['1', '0', '2', '3', '4', '256'])
    floatIter = cycle(['1.5', '0.5'])



    @classmethod
    def start(cls):
        # Called at the beginning of each test.
        # TODO refresh the iterators
        pass


    @classmethod
    def int(cls):
        """
        1 most commonly succeeds, but sometimes is out of range (when only one item)
        0 is out of range for many tested procedures
        """
        result = next(cls.intIter)
        #print(result)
        return result


    @classmethod
    def float(cls):
        """
        Alternately generate quoted float [0,1] or [1,infinity]
        These are the two most common ranges that PDB procedures allow.
        """
        result = next(cls.floatIter)
        return result
