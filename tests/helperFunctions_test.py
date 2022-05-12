from fhir_biobank.helperFunctions import Helper
import pytest
from fhirclient.models.coding import Coding


def test_create_coding_correct_code():
    coding = Helper.create_coding("C42")
    assert coding.code == "C42"


def test_create_coding_incorrect_type_code():
    with pytest.raises(TypeError):
        Helper.create_coding(455)


def test_create_coding_no_parameter_fail():
    with pytest.raises(TypeError):
        Helper.create_coding()


def test_create_coding_system_correct():
    system = "test/system"
    coding = Helper.create_coding("C42", system)
    assert coding.system == system


def test_create_coding_incorrect_type_system():
    with pytest.raises(TypeError):
        Helper.create_coding("C42", 4445)


def test_create_coding_correct_version():
    version = "v2"
    coding = Helper.create_coding("C42", version=version)
    assert coding.version == version


def test_create_coding_correct_display():
    display = "display string"
    coding = Helper.create_coding("C42", display="display string")
    assert coding.display == display


def test_create_coding_incorrect_type_display():
    with pytest.raises(TypeError):
        Helper.create_coding("C42", display=42)


def test_create_coding_correct_user_selected():
    coding = Helper.create_coding("C42", user_selected=True)
    assert coding.userSelected


def test_create_coding_correct_all_parameters():
    code = "C42"
    system = "example/system"
    version = "v2"
    display = "display string"

    coding = Helper.create_coding(code, system, version, display, True)
    assert coding.code == code and coding.system == system and \
           coding.version == version and coding.display == display \
           and coding.userSelected


def test_create_codeable_concept_correct_one_value_list_of_codings():
    coding = [Coding()]
    codeable_concept = Helper.create_codeable_concept(coding)
    assert codeable_concept.coding == coding


def test_create_codeable_concept_correct_multiple_values_list_of_coding():
    coding1 = Coding()
    coding2 = Coding()
    coding3 = Coding()
    codes = [coding1, coding2, coding3]
    codeable_concept = Helper.create_codeable_concept(codes)
    assert codeable_concept.coding == codes


def test_create_codeable_concept_incorrect_type_list_of_coding():
    with pytest.raises(TypeError):
        Helper.create_codeable_concept(42)


def test_create_codeable_concept_incorrect_value_inside_list_of_coding():
    coding1 = Coding()
    incorrect_value = 4
    codes = [coding1, incorrect_value]
    with pytest.raises(TypeError):
        Helper.create_codeable_concept(codes)


def test_create_identifier_correct_value():
    value = "2441"
    identifier = Helper.create_identifier("2441")

    assert identifier.value == value


def test_create_identifier_incorrect_type_value():
    incorrect_value = 2441
    with pytest.raises(TypeError):
        Helper.create_identifier(incorrect_value)


def test_create_identifier_correct_use():
    use = "official"
    identifier = Helper.create_identifier("2441", use)
    assert identifier.use == use


def test_create_identifier_incorrect_type_use():
    use = 4
    with pytest.raises(TypeError):
        Helper.create_identifier("2441", use)


def test_create_identifier_incorrect_value_use():
    use = "unsupported use"
    with pytest.raises(Exception):
        Helper.create_identifier("2441", use)


def test_create_identifier_correct_identifier_type():
    identifier_type = "PPN"
    identifier = Helper.create_identifier("2441",
                                          identifier_type=identifier_type)
    assert identifier.type.coding[0].code == identifier_type


def test_create_identifier_incorrect_type_identifier_type():
    identifier_type = 424
    with pytest.raises(TypeError):
        Helper.create_identifier("2441",identifier_type=identifier_type)


def test_create_identifier_incorrect_value_identifier_type():
    identifier_type = "incorrect type"
    with pytest.raises(Exception):
        Helper.create_identifier("2441",identifier_type=identifier_type)


def test_create_fhir_reference_correct_reference():
    reference="example/reference"
    fhir_reference = Helper.create_fhir_reference(reference)
    assert fhir_reference.reference == reference


def test_create_fhir_reference_incorrect_type_reference():
    reference  = 42
    with pytest.raises(TypeError):
        Helper.create_fhir_reference(reference)