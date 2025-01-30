import xmltodict
from models.eta import CTATT

def parse_xml_to_pydantic(xml_data: str):
    # Convert XML to dict
    parsed_dict = xmltodict.parse(xml_data)
    
    # Extract the top-level 'ctatt' element
    ctatt_dict = parsed_dict.get("ctatt", {})
    
    # Validate and parse using Pydantic
    return CTATT.model_validate(ctatt_dict)