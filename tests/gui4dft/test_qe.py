import pytest

from program.qe import alats_from_pwout, atoms_from_pwout, vectors_from_pwout


def test_vectors_from_pwout(tests_path):
    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-scf' / "pw.out")
    vecs = vectors_from_pwout(f_name)
    assert vecs[0][0] == pytest.approx(-2.69880376)

    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-relax' / "pw.out")
    vecs = vectors_from_pwout(f_name)
    assert vecs[0][0] == pytest.approx(-2.69880376)

    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-vc-relax' / "pw.out")
    vecs = vectors_from_pwout(f_name)
    assert vecs[0][0] == pytest.approx(-2.69880376)


def test_alats_from_pwout(tests_path):
    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-scf' / "pw.out")
    a, b, c, alp, bet, gam = alats_from_pwout(f_name)
    assert a == pytest.approx(5.397607527617)

    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-relax' / "pw.out")
    a, b, c, alp, bet, gam = alats_from_pwout(f_name)
    assert a == pytest.approx(5.397607527617999)

    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-vc-relax' / "pw.out")
    a, b, c, alp, bet, gam = alats_from_pwout(f_name)
    assert a == pytest.approx(3.81668479600608)


def test_atoms_from_pwout(tests_path):
    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-scf' / "pw.out")
    models = atoms_from_pwout(f_name)
    assert len(models) == 1

    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-relax' / "pw.out")
    models = atoms_from_pwout(f_name)
    assert len(models) == 5

    f_name = str(tests_path / 'ref_data' / 'qe' / 'si-vc-relax' / "pw.out")
    models = atoms_from_pwout(f_name)
    assert len(models) == 8

