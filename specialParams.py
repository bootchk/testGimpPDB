

class SpecialParams:
    """
    Knows special, canned params for PDB procedures.

    Special because the dynamic generation of param strings fails.

    For example, when a SF_VALUE is not just a string, but a string that is a list in Scheme
    """


    """
    param string must be a string of form (1, image, drawable, foo, bar), where:
    - 1 is the runmode, optional, 1=>NONINTERACTIVE
    - "image, drawable, " are references to Python vars in scope
    - foo and bar are arguments.

    Case: script-fu-grid-system: two args:
    Each arg is a Scheme quoted list of numerics and character 'g' i.e. "'(1 g 1)'"
    """
    specialParamsMap = {
    "script-fu-grid-system" : """ ( 1, image, drawable, "'(1 g 1)", "'(1 g 1)" ) """,
    }

    @classmethod
    def get(cls, procName):

        if procName in cls.specialParamsMap:
            return cls.specialParamsMap[procName]
        else:
            print(f"Not special {procName}")
            print(cls.specialParamsMap)
            return None
