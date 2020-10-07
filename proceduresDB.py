

import json


class ProceduresDB:

    data = {}


    def read():
        # get dictionary of PDB attributes
        with open("testPDB/pdb.json", "r") as read_file:
            ProceduresDB.data = json.load(read_file)
            # assert procData is-a dictionary
        if not data:
            print("testPDB/pdb.json not readable.")

    def sortedNames():
        return ProceduresDB.data.keys()

    def attributeDictionary(procName):
        return ProceduresDB.data[procName]

    def typeof(procName):
        return ProceduresDB.data[procName]["type"]
