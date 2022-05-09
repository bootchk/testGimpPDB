"""
A singleton class that generate permutations, for arguments.

Methods generate from a range.
The range generally tests limits, aka edge cases.

See elsewhere, we might be testing:
- until a first success (shallow test that some normal Gimp code path succeeds )
- the full range (for crashes)

Methods return strings.
When appended to the parameter string, strings become literals.
E.G. '1' appended to the parameter string yields (..., 1, )
To get a string literal in the parameter string, the returned string must be double quoted.
E.G. "'foo'" appended to the parameter string yields (...,'1',)

TODO make this generate permutations in order,
instead of more or less random permutations.

??? If the sequences are all different cardinality, primes,
given enough calls, it would generate all permutations?
"""

from itertools import cycle



class Cycle():

    """
    Iterators that return a different value from a range each call
    and wrap around, cycling over the range.

    Also behaviour is controlled globally.
    Cycling can be on/off.
    When off, always returns the first value of the range.

    Python iterators of kind 'cycle' from itertools.

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

    """
    Ranges start with the least stressful value.
    E.g. 0 is an edge case that test stresses hard.
    """

    """
    TODO negatives
    0, 256 are edge cases, hard
    1 most commonly succeeds, but sometimes is out of range (when only one item)
    0 is out of range for many tested procedures
    """
    intRange = ['1', '0', '2', '3', '4', '256']

    """
    Alternately generate quoted float [0,1] or [1,infinity]
    These are the two most common ranges that PDB procedures allow.
    "999.000001", "0" are edge cases, hard
    999 seems to hang many scripts
    ['1.5', '0.5', "999.000001", "0"]
    """
    floatRange = ['0.5','0.5','0.5','0.5',  '1.5', '1.5', ]
    # '1.5',

    """
    For SF-VALUE, usually wants a quoted numeric.
    Sometimes a filename or dirname.
    Sometimes a name of a GimpItem.

    !!! Double quoted.  One set of quotes will be removed when we append to a string.
    """
    strRange = ["'foo'", "'/tmp'", "'1'", ]

    intIter = cycle(intRange)
    floatIter = cycle(floatRange)
    strIter = cycle(strRange)

    isCycling = False



    @classmethod
    def turnOnCycling(cls):
        cls.isCycling = True

    @classmethod
    def start(cls):
        # Called at the beginning of each test.
        # TODO refresh the iterators
        pass


    @classmethod
    def int(cls):
        if cls.isCycling:
            result = next(cls.intIter)
        else:
            result = cls.intRange[0]
        #print(result)
        return result


    @classmethod
    def float(cls):
        if cls.isCycling:
            result = next(cls.floatIter)
        else:
            result = cls.floatRange[0]
        return result

    @classmethod
    def str(cls):
        if cls.isCycling:
            result = next(cls.strIter)
        else:
            result = cls.strRange[0]
        return result
