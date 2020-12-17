

import json

# class data and methods, no instance

class ProceduresDB:

    data = {}

    """
    /work refers to the vagga project directory
    where, in the container, is mounted a development directory.
    !!! TODO This should be relative to the plugin's directory, somehow.
    """

    def pathToPDBJson():
        from pathlib import Path

        # relative to this .py file
        path = Path(__file__).parent / "./testPDB/pdb2_99.json"

        # path = "/work/testGimpPDB/testPDB/pdb.json"
        return path



    def readPDBFromJSON():
        data = {}
        with open(ProceduresDB.pathToPDBJson(), "r") as read_file:
            data = json.load(read_file)
        return data


    def read():
        # get Python dictionary modeled after the PDB

        # Alternatively, get a model of PDB by querying PDB
        ProceduresDB.data = ProceduresDB.readPDBFromJSON()

        # assert ProceduresDB.data is-a dictionary modeled after the PDB


    def sortedNames():
        return ProceduresDB.data.keys()

    def attributeDictionary(procName):
        return ProceduresDB.data[procName]

    def typeof(procName):
        return ProceduresDB.data[procName]["type"]
