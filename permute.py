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

    # shared by many generators
    # generally only one generator is used at a time?
    # else this will not be truly stochastic, a generator would repeat a single value
    flip = True

    intIter = cycle(['1', '0', '256'])
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
        #cls.flip = not cls.flip
        return result


    @classmethod
    def float(cls):
        """
        Alternately generate quoted float [0,1] or [1,infinity]
        These are the two most common ranges that PDB procedures allow.
        """
        result = next(cls.floatIter)
        return result
