

from procedureCategory import ProcedureCategory


class UserFilter:
    """ Understands user choice of tests """

    _shouldTestScriptFu = False
    _shouldTestPythonFu = False
    _shouldTestCPlugin = False
    _shouldTestExportImport = False
    _shouldTestTemporary = False
    _shouldTestOther = False

    def setChoices(shouldTestScriptFu,
                   shouldTestPythonFu,
                   shouldTestCPlugin,
                   shouldTestExportImport,
                   shouldTestTemporary,
                   shouldTestOther):
        UserFilter._shouldTestScriptFu = shouldTestScriptFu
        UserFilter._shouldTestPythonFu = shouldTestPythonFu
        UserFilter._shouldTestCPlugin = shouldTestCPlugin
        UserFilter._shouldTestExportImport = shouldTestExportImport
        UserFilter._shouldTestTemporary = shouldTestTemporary
        UserFilter._shouldTestOther = shouldTestOther

    """
    Divide tests into exclusive subsets.
    Test person chooses from among subsets.
    Note the subsets use naming conventions, not only the declared proc type.
    """
    def userWantsTest(procedure_name):
        result = True

        """
        Temporary is orthogonal.
        A Temporary  script is also ScriptFu, Python, or C.
        So to test a Temporary ScriptFu, user must choose two checkboxes.
        Choosing the Temporary checkbox alone does not test anything.
        """
        if   ProcedureCategory.isScriptFu(procedure_name):
            if not UserFilter._shouldTestScriptFu :
                result = False
        elif   ProcedureCategory.isPythonFu(procedure_name):
            if not UserFilter._shouldTestPythonFu :
                result = False
        elif   ProcedureCategory.isCPlugin(procedure_name):
            if not UserFilter._shouldTestCPlugin :
                result = False
        elif ProcedureCategory.isLoadSave(procedure_name):
            if not UserFilter._shouldTestExportImport :
                result = False
        else:
            """
            Other is: Internal or Extension
            or any procedure not named properly
            TODO allow choice of Internal or Extension
            """
            if not UserFilter._shouldTestOther:
                result = False

        if ProcedureCategory.isTemporary(procedure_name):
            if not UserFilter._shouldTestTemporary :
                result = False

        return result
