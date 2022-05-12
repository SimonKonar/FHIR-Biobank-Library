import pytest
from fhir_library.storageTemperature import StorageTemperature


def test_storage_temperature_correct_code():
    code = "temperature2to10"
    storage = StorageTemperature(code)
    assert storage.storageTemperatureCode == code


def test_storage_temperature_incorrect_type_code():
    code = 42
    with pytest.raises(TypeError):
        StorageTemperature(code)


def test_storage_temperature_incorrect_value_code():
    code = "incorrect code"
    with pytest.raises(Exception):
        StorageTemperature(code)
