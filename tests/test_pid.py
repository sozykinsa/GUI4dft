from PySide2.QtWidgets import qApp


def test_pid(qtbot):
    print(f"My pid: {qApp.applicationPid()}")
