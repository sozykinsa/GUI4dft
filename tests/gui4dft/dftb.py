from program.dftb import model_to_dftb_d0


def test_model_to_dftb_d0(h2o_model):
    text = model_to_dftb_d0(h2o_model)
    assert len(text) == 160
