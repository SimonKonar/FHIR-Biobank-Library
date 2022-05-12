from datetime import date
from unittest import mock

import pytest

from fhir_library.bundle import Bundle, Entry
from fhir_library.condition import ConditionResource
from fhir_library.patient import PatientResource
from fhirclient.models.patient import Patient
from fhirclient.models.specimen import Specimen
from fhirclient.models.condition import Condition
import fhirclient.models.bundle as fhir_bundle

from fhir_library.specimen import SpecimenResource


def test_entry_correct_patient_resource():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry = Entry(patient, full_url, short_url)
        assert type(
            entry.resource) == Patient and entry.resourceFullUrl == full_url \
               and entry.resourceShortUrl == short_url \
               and entry.requestMethod == "PUT"


def test_entry_correct_specimen_resource():
    with mock.patch("fhir_library.patient.PatientResource"), mock.patch(
            "fhir_library.specimen.SpecimenResource"):
        patient = PatientResource("0", "2441")
        specimen = SpecimenResource("0", "442", "bone-marrow", patient,
                                    date(2012, 2, 28), 4.0)
        full_url = "https:/example.com/specimen/442"
        short_url = "specimen/442"
        entry = Entry(specimen, full_url, short_url)
        assert type(
            entry.resource) == Specimen and entry.resourceFullUrl == full_url \
               and entry.resourceShortUrl == short_url \
               and entry.requestMethod == "PUT"


def test_entry_correct_condition_resource():
    with mock.patch("fhir_library.patient.PatientResource"), mock.patch(
            "fhir_library.specimen.SpecimenResource"):
        patient = PatientResource("0", "2441")
        condition = ConditionResource("0", "1442", date(2012, 5, 8), patient)
        full_url = "https:/example.com/condition/1442"
        short_url = "condition/1442"
        entry = Entry(condition, full_url, short_url)
        assert type(
            entry.resource) == Condition and entry.resourceFullUrl == full_url \
               and entry.resourceShortUrl == short_url \
               and entry.requestMethod == "PUT"


def test_entry_incorrect_type_resource():
    incorrect_resource = 42
    full_url = "https:/example.com/patient/2441"
    short_url = "patient/2441"
    with pytest.raises(TypeError):
        Entry(incorrect_resource, full_url, short_url)


def test_entry_incorrect_type_full_url():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = 422
        short_url = "patient/2441"
        with pytest.raises(TypeError):
            entry = Entry(patient, full_url, short_url)


def test_entry_incorrect_type_short_url():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = 2441
        with pytest.raises(TypeError):
            entry = Entry(patient, full_url, short_url)


def test_entry_correct_request_method():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        request = "DELETE"
        entry = Entry(patient, full_url, short_url, request)
        assert entry.requestMethod == request


def test_entry_incorrect_type_request_method():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        request = []
        with pytest.raises(TypeError):
            entry = Entry(patient, full_url, short_url, request)


def test_entry_incorrect_value_request_method():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        incorrect_request = "incorrect method"
        with pytest.raises(TypeError):
            Entry(patient, full_url, short_url, incorrect_request)


def test_entry_convert_to_fhir_gets_called_only_once():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
    with mock.patch.object(Entry, "_convert_to_FHIR",
                           return_value="mock", ) as mock__convert_to_FHIR:
        entry = Entry(patient, full_url, short_url)
        _ = entry.FHIRInterpretation
        _ = entry.FHIRInterpretation
        mock__convert_to_FHIR.assert_called_once_with()


def test_entry_correct_entryJson():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry = Entry(patient, full_url, short_url)
        assert type(entry.entryJSON) == dict


def test_bundle_correct_values():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry = Entry(patient, full_url, short_url)
        bundle = Bundle("6441", [entry])
        assert type(bundle.entries[
                        0]) == fhir_bundle.BundleEntry and bundle.id == "6441"


def test_bundle_incorrect_id():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        bundle_id = 6441
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry = Entry(patient, full_url, short_url)
        with pytest.raises(TypeError):
            Bundle(bundle_id, [entry])


def test_bundle_multiple_correct_entries():
    with mock.patch("fhir_library.patient.PatientResource"), mock.patch(
            "fhir_library.specimen.SpecimenResource"), mock.patch(
        "fhir_library.condition.ConditionResource"):
        patient = PatientResource("0", "2441")
        specimen = SpecimenResource("0", "442", "bone-marrow", patient,
                                    date(2012, 2, 28), 4.0)
        condition = ConditionResource("0", "1442", date(2012, 5, 8), patient)
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry_patient = Entry(patient, full_url, short_url)
        entry_specimen = Entry(specimen, full_url, short_url)
        entry_condition = Entry(condition, full_url, short_url)
        bundle = Bundle("6441",
                        [entry_patient, entry_specimen, entry_condition])
        assert type(bundle.entries[0]) == fhir_bundle.BundleEntry \
               and type(bundle.entries[1]) == fhir_bundle.BundleEntry \
               and type(bundle.entries[2]) == fhir_bundle.BundleEntry \
               and bundle.id == "6441"


def test_bundle_incorrect_value_in_entries():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry_patient = Entry(patient, full_url, short_url)
        entry_incorrect_type = 47
        with pytest.raises(TypeError):
            bundle = Bundle("6441", [entry_patient, entry_incorrect_type])


def test_bundle_empty_entries():
    full_url = "https:/example.com/patient/2441"
    short_url = "patient/2441"
    with pytest.raises(ValueError):
        bundle = Bundle("6441", [])


def test_bundle_incorrect_type_bundle_type():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry_patient = Entry(patient, full_url, short_url)
        incorrect_bundle_type = 7541
        with pytest.raises(TypeError):
            bundle = Bundle("6441", [entry_patient], incorrect_bundle_type)


def test_bundle_incorrect_value_bundle_type():
    with mock.patch("fhir_library.patient.PatientResource"):
        patient = PatientResource("0", "2441")
        full_url = "https:/example.com/patient/2441"
        short_url = "patient/2441"
        entry_patient = Entry(patient, full_url, short_url)
        incorrect_bundle_type = "incorrect type of bundle"
        with pytest.raises(TypeError):
            bundle = Bundle("6441", [entry_patient], incorrect_bundle_type)

