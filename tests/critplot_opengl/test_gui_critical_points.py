import pytest


def test_critic2_section(critplot_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    window = critplot_application
    window.menu_open(f_name)
    model = window.models[-1]
    assert len(model.cps) == 11
    assert float(model.cps[0].properties["rho"]) == pytest.approx(4.00665868)
    window.add_cp_to_list()
    assert window.ui.FormCPlist.count() == 0
    window.selected_atom_changed([-1, 1])
    assert window.ui.selectedCP_nuclei.text() == "..."
    window.ui.selectedCP.setText("2")
    window.add_cp_to_list()
    window.add_cp_to_list()
    assert window.ui.FormCPlist.item(0).text() == "2"
    window.ui.FormCPlist.setCurrentRow(0)
    assert window.ui.FormCPlist.count() == 1
    window.delete_cp_from_list()
    assert window.ui.FormCPlist.count() == 0


def test_create_cri_file(critplot_application, tests_path):
    f_name = str(tests_path / 'ref_data' / 'critic2' / "siesta-1-cp.cro")
    window = critplot_application
    window.menu_open(f_name)
    window.ui.selectedCP.setText("1")
    window.add_cp_to_list()
    assert len(window.models[-1].cps) == 11
    window.delete_cp_from_model()
    assert len(window.models[-1].cps) == 10
    window.ui.selectedCP.setText("2")
    window.add_cp_to_list()
    window.leave_cp_in_model()
    assert len(window.models[-1].cps) == 2
