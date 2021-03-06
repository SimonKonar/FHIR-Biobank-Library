# FHIR Library

This Python library is simplifying work with FHIR library focused on BBMRI-ERIC biobanks.
This library works with Patient, Specimen, and Condition resources, along with
extensions needed for these resources as defined by [simplifier.net/bbrmi.de](https://simplifier.net/bbmri.de).

Documentation of this library is available at [fhir-biobank.readthedocs.io](https://fhir-biobank.readthedocs.io)


## Installation
pip install fhir-biobank

## Usage
This library allows you to easily create FHIR resources along with all the data in a single constructor.
Use case of creating a simple Patient resource:
```python
from fhir_biobank import PatientResource

internal_id = "0"
patient_identifier = "4816522"
patient_gender = "female"
patient_birthdate = date(2000, 12, 11)
patient = PatientResource(internal_id, patient_identifier, patient_gender, patient_birthdate)
```

Standard action is to convert FHIR resource to a JSON representation.
Use case of converting Patient resource to a JSON representation:

```python
json_representation = patient.patientJSON()
```

JSON representation of the Patient resource initialized above looks like this:
```json
{
  "id": "0",
  "meta": { "profile": [ "https://fhir.bbmri.de/StructureDefinition/Patient" ] },
  "birthDate": "2000-12-11",
  "deceasedBoolean": "False",
  "gender": "female",
  "identifier": [
    {
      "type": {
        "coding": [
          {
            "code": "ACSN",
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "userSelected": "True"
          }
        ]
      },
      "use": "usual",
      "value": "4816522"
    }
  ],
  "multipleBirthBoolean": "False",
  "resourceType": "Patient"
}
```
In order to upload resource to a server, creating Bundle resource containing all of the resources that you want to upload is necessary.
Bundle contains list of Entry resources, where each Entry resource represents specific resource(for example Patient resource).
Here is a example how to create Bundle resource containing the Patient resource made earlier:

```python
from fhir_biobank.bundle import Bundle, Entry

fullURL_patient_resource = "https://example.com/patient/0"
shortURL_patient_resource = "patient/0"
entry = Entry(patient, fullURL_patient_resource, shortURL_patient_resource)
entries = [entry]
bundle_id = "424242"
bundle = Bundle(bundle_id, entries)
```

