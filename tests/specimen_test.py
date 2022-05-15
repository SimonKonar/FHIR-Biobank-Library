import pytest
from datetime import date, timedelta
from unittest import mock
from fhir_biobank.diagnosis import Diagnosis
from fhir_biobank.patient import PatientResource
from fhir_biobank.specimen import SpecimenResource
from fhir_biobank.storageTemperature import StorageTemperature


def test_specimen_correct_required_parameters_only():
    with mock.patch("fhir_biobank.patient.PatientResource"):
        identifier = "2441"
        specimen_material_code = "whole-blood"
        patient = PatientResource("0", "744")
        collected_date = date(2020, 9, 11)
        quantity = 3.5
        specimen = SpecimenResource("0", identifier, specimen_material_code,
                                    patient,
                                    collected_date, quantity)
        assert specimen.identifier == identifier \
               and specimen.specimenMaterialCode == specimen_material_code \
               and specimen.subject == patient \
               and specimen.collectedDateTime == collected_date \
               and specimen.quantity == quantity


def test_specimen_incorrect_type_identifier():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = 2441
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    with pytest.raises(TypeError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity)


def test_specimen_incorrect_type_material_code():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = []
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    with pytest.raises(TypeError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity)


def test_specimen_incorrect_value_identifier():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "incorrect code"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    with pytest.raises(ValueError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity)


def test_specimen_incorrect_type_collected_date():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = 2000
    quantity = 3.5
    with pytest.raises(TypeError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity)


def test_specimen_incorrect_value_collected_date():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date.today() + timedelta(days=10)
    quantity = 3.5
    with pytest.raises(ValueError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity)


def test_specimen_incorrect_type_quantity():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3
    with pytest.raises(TypeError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity)


def test_specimen_correct_body_site_collection_code():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    body_site_code = "C44"
    specimen = SpecimenResource("0", identifier, specimen_material_code,
                                patient,
                                collected_date, quantity, body_site_code)
    assert specimen.bodySiteCollectionCode == body_site_code


def test_specimen_incorrect_type_body_site_collection_code():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    body_site_code = 44
    with pytest.raises(TypeError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity, body_site_code)


def test_specimen_correct_quantity_unit():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    quantity_unit = "mililiter"
    specimen = SpecimenResource("0", identifier, specimen_material_code,
                                patient,
                                collected_date, quantity,
                                quantity_unit=quantity_unit)
    assert specimen.quantityUnit == quantity_unit


def test_specimen_incorrect_type_quantity_unit():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    quantity_unit = []
    with pytest.raises(TypeError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity, quantity_unit=quantity_unit)


def test_specimen_correct_quantity_code():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    quantity_code = "ml"
    specimen = SpecimenResource("0", identifier, specimen_material_code,
                                patient,
                                collected_date, quantity,
                                quantity_unit_code=quantity_code)
    assert specimen.quantityUnitCode == quantity_code


def test_specimen_incorrect_type_quantity_code():
    mock.patch("fhir_biobank.patient.PatientResource")
    identifier = "2441"
    specimen_material_code = "whole-blood"
    patient = PatientResource("0", "744")
    collected_date = date(2020, 9, 11)
    quantity = 3.5
    quantity_unit = 45
    with pytest.raises(TypeError):
        SpecimenResource("0", identifier, specimen_material_code, patient,
                         collected_date, quantity,
                         quantity_unit_code=quantity_unit)


def test_specimen_correct_extensions():
    with mock.patch("fhir_biobank.patient.PatientResource"), mock.patch(
            "fhir_biobank.diagnosis.Diagnosis"):
        identifier = "2441"
        specimen_material_code = "whole-blood"
        patient = PatientResource("0", "744")
        collected_date = date(2020, 9, 11)
        quantity = 3.5
        extensions = [Diagnosis("C42")]
        specimen = SpecimenResource("0", identifier, specimen_material_code,
                                    patient,
                                    collected_date, quantity,
                                    extensions=extensions)
        assert specimen.extensions[0] == extensions[0]


def test_specimen_incorrect_type_extensions():
    with mock.patch("fhir_biobank.patient.PatientResource"), mock.patch(
            "fhir_biobank.diagnosis.Diagnosis"):
        identifier = "2441"
        specimen_material_code = "whole-blood"
        patient = PatientResource("0", "744")
        collected_date = date(2020, 9, 11)
        quantity = 3.5
        extensions = []
        with pytest.raises(ValueError):
            SpecimenResource("0", identifier, specimen_material_code,
                             patient,
                             collected_date, quantity,
                             extensions=extensions)


def test_specimen_incorrect_value_in_extensions():
    with mock.patch("fhir_biobank.patient.PatientResource"), mock.patch(
            "fhir_biobank.diagnosis.Diagnosis"):
        identifier = "2441"
        specimen_material_code = "whole-blood"
        patient = PatientResource("0", "744")
        collected_date = date(2020, 9, 11)
        quantity = 3.5
        extensions = [StorageTemperature("temperature2to10"),
                      "unsupported extension"]
        with pytest.raises(TypeError):
            SpecimenResource("0", identifier, specimen_material_code,
                             patient,
                             collected_date, quantity,
                             extensions=extensions)


def test_specimen_convert_to_fhir_gets_called_only_once():
    with mock.patch("fhir_biobank.patient.PatientResource"), mock.patch(
            "fhir_biobank.diagnosis.Diagnosis"):
        identifier = "2441"
        specimen_material_code = "whole-blood"
        patient = PatientResource("0", "744")
        collected_date = date(2020, 9, 11)
        quantity = 3.5
        extensions = [Diagnosis("C42")]
        with mock.patch.object(SpecimenResource, "_convert_to_FHIR",
                               return_value="mock", ) as mock__convert_to_FHIR:
            specimen = SpecimenResource("0", identifier,
                                        specimen_material_code, patient,
                                        collected_date, quantity,
                                        extensions=extensions)
            _ = specimen.FHIRInterpretation
            _ = specimen.FHIRInterpretation
            mock__convert_to_FHIR.assert_called_once_with()


def test_specimen_correct_specimenJson():
    with mock.patch("fhir_biobank.patient.PatientResource"), mock.patch(
            "fhir_biobank.diagnosis.Diagnosis"):
        identifier = "2441"
        specimen_material_code = "whole-blood"
        patient = PatientResource("0", "744")
        collected_date = date(2020, 9, 11)
        quantity = 3.5
        extensions = [Diagnosis("C42")]
        specimen = SpecimenResource("0", identifier, specimen_material_code,
                                    patient,
                                    collected_date, quantity,
                                    extensions=extensions)
        assert type(specimen.specimenJSON()) == dict
