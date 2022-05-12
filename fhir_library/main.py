from fhir_library import bundle as bnd, diagnosis as dng, patient as ptn, \
    specimen as spc
import fhirclient.models.patient as fhirclient_patient
import fhirclient.models.identifier as fhirclient_identifier
import fhirclient.models.meta as fhirclient_meta
import fhirclient.models.fhirdate as fhirclient_date
import fhirclient.models.quantity as fhirclient_quantity
import fhirclient.models.codeableconcept as fhirclient_codeable_concept
import fhirclient.models.coding as fhirclient_coding
import fhirclient.models.specimen as fhirclient_specimen
import fhirclient.models.extension as fhirclient_extension
import fhirclient.models.fhirreference as fhirclient_reference
import fhirclient.models.bundle as fhirclient_bundle
from datetime import date, datetime
import os
import xml.etree.ElementTree as ET

current_working_directory = os.getcwd()
par_dir = os.path.dirname(current_working_directory)
print(par_dir)
tree = ET.parse(par_dir + "/BBM211219230002-000079.XML")
root = tree.getroot()

"""
    MY LIBRARY IMPLEMETATION 
"""


def my_fhir_library_implementation():
    patient_id = root.attrib.get("id")
    patient_sex = root.attrib.get("sex")
    patient_birthdate = root.attrib.get("year")
    patient_birthdate = date(int(patient_birthdate), 1, 1)
    patient = ptn.PatientResource("patient-0", patient_id, patient_sex,
                                  patient_birthdate)

    samples = []
    counter = 0
    for sample in root.iter(
            r"{http://www.bbmri.cz/schemas/biobank/data}tissue"):
        sample_id = str(sample.attrib.get("sampleId"))
        sample_quantity = float((sample.find(
            r"{http://www.bbmri.cz/schemas/biobank/data}availableSamplesNo").text))
        sample_collection_time = (
            sample.find(
                r"{http://www.bbmri.cz/schemas/biobank/data}cutTime").text)
        sample_collection_time = datetime.strptime(sample_collection_time,
                                                   "%Y-%m-%dT%H:%M:%S").date()
        sample_material_type = "whole-blood"

        diagnosis_code = (sample.find(
            r"{http://www.bbmri.cz/schemas/biobank/data}diagnosis").text)

        diagnosis = dng.Diagnosis(diagnosis_code)

        my_sample = spc.SpecimenResource("specimen-" + str(counter), sample_id,
                                         sample_material_type,
                                         patient,
                                         sample_collection_time,
                                         sample_quantity,
                                         extensions=[diagnosis])
        samples.append(my_sample)
        counter += 1

    entries = [bnd.Entry(patient, "https://example.com/patient/" +
                         patient.patientId, "patient/" + patient.patientId)]

    for sample in samples:
        entry = bnd.Entry(sample,
                          "https://example.com/specimen/" + sample.specimenId,
                          "specimen/" + sample.specimenId)
        entries.append(entry)

    bundle = bnd.Bundle("45224775412", entries)
    return bundle.bundleJSON


"""
FHIR_CLIENT IMPLEMENTATION
"""


def fhir_client_implementation():
    xml_patient_id = root.attrib.get("id")
    xml_patient_sex = root.attrib.get("sex")
    xml_patient_birthdate = root.attrib.get("year")
    xml_patient_birthdate = date(int(xml_patient_birthdate), 1, 1)

    patient_meta = fhirclient_meta.Meta()
    patient_meta.profile = [
        "https://fhir.bbmri.de/StructureDefinition/Patient"]

    patient_birthdate = fhirclient_date.FHIRDate()
    patient_birthdate.date = xml_patient_birthdate

    patient_identifier = fhirclient_identifier.Identifier()
    patient_identifier.value = xml_patient_id
    patient_identifier.use = "usual"

    patient_identifier_code = fhirclient_coding.Coding()
    patient_identifier_code.code = "ACSN"
    patient_identifier_code.system = \
        "http://terminology.hl7.org/CodeSystem/v2-0203"
    patient_identifier_code.userSelected = True

    patient_identifier_codeable_concept = \
        fhirclient_codeable_concept.CodeableConcept()
    patient_identifier_codeable_concept.coding = [patient_identifier_code]
    patient_identifier.type = patient_identifier_codeable_concept

    fhir_patient = fhirclient_patient.Patient()
    fhir_patient.id = "0"
    fhir_patient.identifier = [patient_identifier]
    fhir_patient.meta = patient_meta
    fhir_patient.birthDate = patient_birthdate
    fhir_patient.gender = xml_patient_sex
    fhir_patient.multipleBirthBoolean = False
    fhir_patient.deceasedBoolean = False

    fhir_patient_reference = fhirclient_reference.FHIRReference()
    fhir_patient_reference.reference = "Patient/" + fhir_patient.id

    samples = []

    sample_ids = []
    counter = 0
    for sample in root.iter(
            r"{http://www.bbmri.cz/schemas/biobank/data}tissue"):
        fhir_sample_meta = fhirclient_meta.Meta()
        fhir_sample_meta.profile = [
            "https://fhir.bbmri.de/StructureDefinition/Specimen"]

        sample_id = str(sample.attrib.get("sampleId"))

        fhir_sample_identifier = fhirclient_identifier.Identifier()
        fhir_sample_identifier.use = "usual"
        fhir_sample_identifier_code = fhirclient_coding.Coding()
        fhir_sample_identifier_code.code = "ACSN"
        fhir_sample_identifier_code.system = "http://terminology.hl7.org/CodeSystem/v2-0203"
        fhir_sample_identifier_code.userSelected = True

        fhir_sample_identifier_codeable_concept = fhirclient_codeable_concept.CodeableConcept()
        fhir_sample_identifier_codeable_concept.coding = [
            patient_identifier_code]

        fhir_sample_identifier.type = fhir_sample_identifier_codeable_concept
        fhir_sample_identifier.value = sample_id

        sample_quantity_value = float((sample.find(
            r"{http://www.bbmri.cz/schemas/biobank/data}availableSamplesNo").text))

        fhir_sample_container = fhirclient_specimen.SpecimenContainer()
        fhir_sample_quantity = fhirclient_quantity.Quantity()
        fhir_sample_quantity.value = sample_quantity_value
        fhir_sample_quantity.system = "http://unitsofmeasure.org"
        fhir_sample_container.specimenQuantity = fhir_sample_quantity

        sample_collection_time = (
            sample.find(
                r"{http://www.bbmri.cz/schemas/biobank/data}cutTime").text)
        sample_collection_time = datetime.strptime(sample_collection_time,
                                                   "%Y-%m-%dT%H:%M:%S").date()

        fhir_sample_collection = fhirclient_specimen.SpecimenCollection()

        fhir_sample_collected_time = fhirclient_date.FHIRDate()
        fhir_sample_collected_time.date = sample_collection_time

        fhir_sample_collection.collectedDateTime = fhir_sample_collected_time

        sample_material_type = "whole-blood"

        fhir_sample_material_type_code = fhirclient_coding.Coding()
        fhir_sample_material_type_code.code = sample_material_type
        fhir_sample_material_type_code.system = "https://fhir.bbmri.de/CodeSystem/SampleMaterialType"
        fhir_sample_material_type_code.userSelected = False

        fhir_sample_material_type_codeable_concept = fhirclient_codeable_concept.CodeableConcept()
        fhir_sample_material_type_codeable_concept.coding = [
            fhir_sample_material_type_code]

        diagnosis_code = (sample.find(
            r"{http://www.bbmri.cz/schemas/biobank/data}diagnosis").text)

        fhir_diagnosis = fhirclient_extension.Extension()

        fhir_diagnosis_code = fhirclient_coding.Coding()
        fhir_diagnosis_code.code = diagnosis_code
        fhir_diagnosis_code.system = "http://hl7.org/fhir/sid/icd-10"
        fhir_diagnosis_code.userSelected = False

        fhir_diagnosis_codeable_concept = fhirclient_codeable_concept.CodeableConcept()
        fhir_diagnosis_codeable_concept.coding = [fhir_diagnosis_code]

        fhir_diagnosis.url = "https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis"
        fhir_diagnosis.valueCodeableConcept = fhir_diagnosis_codeable_concept
        # diagnosis = dng.Diagnosis(diagnosis_code)

        fhir_sample = fhirclient_specimen.Specimen()
        fhir_sample.id = "specimen-" + str(counter)
        fhir_sample.meta = fhir_sample_meta
        fhir_sample.identifier = [fhir_sample_identifier]
        fhir_sample.collection = fhir_sample_collection
        fhir_sample.container = [fhir_sample_container]
        fhir_sample.type = fhir_sample_material_type_codeable_concept
        fhir_sample.subject = fhir_patient_reference
        fhir_sample.extension = [fhir_diagnosis]
        sample_ids.append("specimen-" + str(counter))
        samples.append(fhir_sample)
        counter += 1

    entries = []

    fhir_entry_patient_request = fhirclient_bundle.BundleEntryRequest()
    fhir_entry_patient_request.url = "patient/" + xml_patient_id
    fhir_entry_patient_request.method = "PUT"

    fhir_entry_patient = fhirclient_bundle.BundleEntry()
    fhir_entry_patient.resource = fhir_patient
    fhir_entry_patient.fullUrl = "https://example.com/patient/" + xml_patient_id
    fhir_entry_patient.request = fhir_entry_patient_request

    entries.append(fhir_entry_patient)

    counter = 0
    for sample in samples:
        fhir_entry_sample_request = fhirclient_bundle.BundleEntryRequest()
        fhir_entry_sample_request.url = "specimen/" + sample_ids[counter]
        fhir_entry_sample_request.method = "PUT"

        fhir_entry_sample = fhirclient_bundle.BundleEntry()
        fhir_entry_sample.resource = sample
        fhir_entry_sample.fullUrl = "https://example.com/specimen/" + \
                                    sample_ids[counter]
        fhir_entry_sample.request = fhir_entry_sample_request

        entries.append(fhir_entry_sample)
        counter += 1

    fhir_bundle = fhirclient_bundle.Bundle()
    fhir_bundle.id = "45224775412"
    fhir_bundle.entry = entries
    fhir_bundle.type = "transaction"
    return fhir_bundle.as_json()


print(my_fhir_library_implementation())
fhir_json = str(fhir_client_implementation()).replace("True", "true")
fhir_json = fhir_json.replace("False", "false")
print(fhir_json)

