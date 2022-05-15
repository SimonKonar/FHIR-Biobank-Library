# tests for PatientResource class
from unittest import mock

import pytest
from datetime import date, timedelta

from fhir_biobank.patient import PatientResource


def test_patient_correct_identifier():
    assert type(PatientResource("0", "2441")) == PatientResource


def test_patient_incorrect_type_identifier():
    with pytest.raises(TypeError):
        PatientResource("0", 23212)


def test_patient_with_correct_gender():
    patient = PatientResource("0", "2441", "male")
    assert patient.gender == "male"


def test_patient_with_incorrect_type_gender():
    with pytest.raises(TypeError):
        PatientResource("0", "2441", 2415)


def test_patient_with_incorrect_gender():
    with pytest.raises(ValueError):
        PatientResource("0", "2441", "apache")


def test_patient_with_correct_birth_date():
    patient = PatientResource("0", "2441", birth_date=date(2000, 2, 18))
    assert patient.birthDate == date(2000, 2, 18)


def test_patient_with_incorrect_type_birth_date():
    with pytest.raises(TypeError):
        PatientResource("0", "2441", birth_date=10)


def test_patient_with_incorrect_value_birth_date():
    with pytest.raises(ValueError):
        PatientResource("0", "2441",
                        birth_date=date.today() + timedelta(days=10))


def test_patient_with_correct_deceased_boolean():
    patient = PatientResource("0", "2441", deceased_boolean=True)
    assert patient.deceasedBoolean


def test_patient_with_incorrect_type_deceased_boolean():
    with pytest.raises(TypeError):
        PatientResource("0", "2441", deceased_boolean=112)


def test_patient_with_deceased_boolean_false_and_correct_deceased_datetime():
    with pytest.raises(ValueError):
        PatientResource("0", "2441", deceased_boolean=False,
                        deceased_datetime=date.today())


def test_patient_with_deceased_boolean_none_and_correct_deceased_datetime():
    with pytest.raises(ValueError):
        PatientResource("0", "2441", deceased_datetime=date.today())


def test_patient_with_deceased_boolean_true_and_correct_deceased_datetime():
    deceased_date = date(2005, 4, 7)
    patient = PatientResource("0", "2441", deceased_boolean=True,
                              deceased_datetime=deceased_date)
    assert patient.deceasedDatetime == deceased_date


def test_patient_with_correct_multiple_birth_boolean():
    patient = PatientResource("0", "2441", multiple_birth_boolean=True)
    assert patient.multipleBirthBoolean


def test_patient_with_incorrect_type_multiple_birth_boolean():
    with pytest.raises(TypeError):
        PatientResource("0", "2441", multiple_birth_boolean="True")


def test_patient_with_correct_multiple_int_and_multiple_birth_boolean():
    patient = PatientResource("0", "2441", multiple_birth_boolean=True,
                              multiple_birth_int=1)

    assert patient.multipleBirthBoolean and patient.multipleBirthInteger == 1


def test_patient_with_incorrect_type_multiple_birth_int_and_correct_multiple_birt_boolean():
    with pytest.raises(TypeError):
        PatientResource("0", "2441", multiple_birth_boolean=True,
                        multiple_birth_int="ase")


def test_patient_with_correct_multiple_int_and_no_multiple_birth_boolean():
    with pytest.raises(ValueError):
        PatientResource("0", "2441", multiple_birth_int=2)


def test_patient_with_multiple_birth_boolean_false_and_correct_multiple_birth_int():
    with pytest.raises(ValueError):
        PatientResource("0", "2441", multiple_birth_boolean=False,
                        multiple_birth_int=2)


def test_patient_with_correct_patient_links():
    patient_for_link = PatientResource("0", "2441")
    patient = PatientResource("0", "4477", patient_links=[patient_for_link])
    assert patient.link[0] == patient_for_link


def test_patient_with_incorrect_type_patient_links():
    with pytest.raises(TypeError):
        PatientResource("0", "2441", patient_links=2441)


def test_patient_with_incorrect_value_inside_patient_links():
    with pytest.raises(TypeError):
        PatientResource("0", "2441", patient_links=["24"])


def test_patient_with_correct_and_incorrect_values_inside_patient_links():
    patient_link = PatientResource("0", "2441")
    incorrect_value = 42
    list_patient_links = [patient_link, incorrect_value]
    with pytest.raises(TypeError):
        PatientResource("0", "2441", patient_links=list_patient_links)


def test_patient_convert_to_fhir_gets_called_only_once():
    gender = "male"
    birth_date = date(2000,2,18)
    with mock.patch.object(PatientResource, "_convert_to_FHIR",
                           return_value="mock", ) as mock__convert_to_FHIR:
        patient = PatientResource("0","2441",gender,birth_date)
        _ = patient.FHIRInterpretation
        _ = patient.FHIRInterpretation
        mock__convert_to_FHIR.assert_called_once_with()


def test_patient_correct_patientJson():
    gender = "male"
    birth_date = date(2000, 2, 18)
    patient = PatientResource("0", "2441", gender, birth_date)
    assert type(patient.patientJSON()) == dict


"""
    with unittest.mock.patch("patient.PatientResource.link", new_callable=unittest.mock.PropertyMock) as mock_link:
        mock_link.return_value = "2441"
        mock_patient = PatientResource("awe")
        patient = PatientResource("ewa4",patient_links=[mock_patient])
        print(patient.link)
"""
