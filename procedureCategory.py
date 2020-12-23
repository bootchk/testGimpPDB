

from proceduresDB import ProceduresDB

class ProcedureCategory:
    """
    Knows procedure types and subcategories thereof.

    Unique "type" attribute in pdb.JSON
       "GIMP Extension",
       "GIMP Plug-In",
       "Internal GIMP procedure",
       "Temporary Procedure"

    We further divide the "GIMP Plug-in category" by parsing
    procedure names which should follow naming convention.

    Only two Extension? extension-script-fu and extension-gimp-help
    """

    def isScriptFu(procName):
        # ScriptFu is also Temporary Procedure
        return procName.find("script-fu-")==0

    def isPythonFu(procName):
        return procName.find("python-fu-")==0

    def isCPlugin(procName):
        return procName.find("plug-in-")==0

    def isTemporary(procName):
        # Note that all (?) of temporary procedures are omitted later anyway ???
        return ProceduresDB.typeof(procName) == "Temporary Procedure"



    def isPlugin(procName):
        # Relies on procedure canonical names
        # TODO test procedure type?
        # file-foo-save is a plug-in also
        # file-foo-load TODO
        return (procName.find("plug-in-")==0
            or ProcedureCategory.isScriptFu(procName)
            or ProcedureCategory.isPythonFu(procName)
            or ProcedureCategory.isCPlugin(procName)
            or (procName.find("file-")==0
               and procName.find("-save")>0)
            )

    def isDeleting(procName):
        """ We don't test procedures that might delete our test data. """
        return procName.find("-delete")>0

    def isLoadSave(procName):
        """
        Does procedure save/load images?

        Note is another plugin in github bootch/testGimpExportImport
        will better test such procedures (using a test set of file formats.)

        Typically name file-<foo>-save and -load
        """
        if (procName.startswith('file')):
            return True
        return False

    def doesGimpFuHideRunMode(procName):
        # TODO keep in correspondence with gimpfu/gimpprocedure.py should_insert_runmode_arg()
        return ProcedureCategory.isPythonFu(procName)
