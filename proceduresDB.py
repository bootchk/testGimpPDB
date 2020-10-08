

import json


class ProceduresDB:

    data = {}

    """
    /work refers to the vagga project directory
    where, in the container, is mounted a development directory.
    !!! TODO This should be relative to the plugin's directory, somehow.
    """
    def read():
        # get dictionary of PDB attributes

        with open("/work/testGimpPDB/testPDB/pdb.json", "r") as read_file:
            ProceduresDB.data = json.load(read_file)
            # assert procData is-a dictionary

    def sortedNames():
        return ProceduresDB.data.keys()

    def attributeDictionary(procName):
        return ProceduresDB.data[procName]

    def typeof(procName):
        return ProceduresDB.data[procName]["type"]
