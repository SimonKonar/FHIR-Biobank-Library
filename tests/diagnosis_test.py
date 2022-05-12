import pytest
from fhir_biobank.diagnosis import Diagnosis


def test_diagnosis_correct_code():
    code = "C42.5"
    diagnosis = Diagnosis(code)
    assert diagnosis.diagnosisCode == code


def test_diagnosis_incorrect_type_code():
    code = 42
    with pytest.raises(TypeError):
        Diagnosis(code)
