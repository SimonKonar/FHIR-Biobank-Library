import pytest
from unittest import mock
from fhir_biobank.condition import ConditionResource
from datetime import date, timedelta

from fhir_biobank.patient import PatientResource


def test_condition_all_correct_values():
    code = "C42"
    condition_date = date(2012, 11, 9)
    with mock.patch("fhir_biobank.patient.PatientResource.identifier",
                    new_callable=mock.PropertyMock) as mock_identifier:
        mock_identifier.return_value = "2441"
        mock_patient = PatientResource("0", "2441")
        condition = ConditionResource("0", code, condition_date, mock_patient)
        assert condition.conditionCode == code \
               and condition.startingDateCondition == condition_date \
               and condition.patient == mock_patient


def test_condition_incorrect_type_code():
    incorrect_code = 42
    condition_date = date(2012, 11, 9)
    mock.patch("patient.PatientResource")
    with pytest.raises(TypeError):
        ConditionResource("0", incorrect_code, condition_date,
                          PatientResource("0", "2441"))


def test_condition_incorrect_type_date():
    code = "C42"
    incorrect_condition_date = 2002
    mock.patch("patient.PatientResource")
    with pytest.raises(TypeError):
        ConditionResource("0", code, incorrect_condition_date,
                          PatientResource("0", "2441"))


def test_condition_incorrect_value_date_condition():
    code = "C42"
    incorrect_condition_date = date.today() + timedelta(days=10)
    mock.patch("patient.PatientResource")
    with pytest.raises(Exception):
        ConditionResource("0", code, incorrect_condition_date,
                          PatientResource("0", "2441"))


def test_condition_incorrect_type_patient():
    code = "C42"
    condition_date = date(2002, 4, 11)
    incorrect_patient = "this is not patient"
    with pytest.raises(TypeError):
        ConditionResource("0", code, condition_date,
                          incorrect_patient)


def test_condition_convert_to_fhir_gets_called_only_once():
    code = "C42"
    condition_date = date(2002, 4, 11)
    patient = PatientResource("0", "2441")

    with mock.patch.object(ConditionResource, "_convert_to_FHIR",
                           return_value="mock", ) as mock__convert_to_FHIR:
        condition = ConditionResource("0", code, condition_date, patient)
        _ = condition.FHIRInterpretation
        _ = condition.FHIRInterpretation
        mock__convert_to_FHIR.assert_called_once_with()


def test_condition_correct_conditionJson():
    code = "C42"
    condition_date = date(2002, 4, 11)
    patient = PatientResource("0", "2441")
    condition = ConditionResource("0", code, condition_date, patient)
    assert type(condition.conditionJSON()) == dict
