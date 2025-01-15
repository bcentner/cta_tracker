from enum import Enum


class CTAErrorException(Exception):
    def __init__(self, error, detail=None):
        self.error = error
        self.detail = detail

        message = f"Error {error.code}: {error.name} - {error.explanation}"
        if detail:
            message += f" Detail: {detail}"
        super().__init__(message)
        
        
class ArrivalErrors(Enum):  # FIXME: restructure
    MISSING_PARAMETER = (100, "The query string does not contain one of the required parameters, currently: 'mapid or stpid', 'key'.")
    INVALID_API_KEY = (101, "The value for the required parameter 'key' is not a valid API key.")
    MAX_DAILY_USAGE_EXCEEDED = (102, "The number of successful API Requests using the supplied 'key' have exceeded the maximum daily value.")
    INVALID_MAPID = (103, "At least one of the supplied values for the 'mapid' parameter is not valid. The first invalid id is returned.")
    MAPID_NOT_INTEGER = (104, "At least one of the supplied values for the 'mapid' parameter is not an integer value. The first invalid id is returned.")
    MAX_MAPID_EXCEEDED = (105, "A maximum of 4 values may be specified for the parameter 'mapid'. More than 4 were supplied.")
    INVALID_ROUTE_IDENTIFIER = (106, "At least one of the supplied values for the 'rt' parameter is invalid. Supported values are: 'Red', 'Blue', 'Brn', 'G', 'Org', 'P', 'Pink', 'Y'.")
    MAX_ROUTE_IDENTIFIER_EXCEEDED = (107, "A maximum of 4 values may be specified for the parameter 'rt'. More than 4 were supplied.")
    INVALID_STPID = (108, "At least one of the supplied values for the 'stpid' parameter is invalid. The first invalid value is returned.")
    MAX_STPID_EXCEEDED = (109, "A maximum of 4 values may be specified for the parameter 'stpid'. More than 4 were supplied.")
    INVALID_MAX = (110, "A non-integer value was specified for the 'max' parameter.")
    MAX_POSITIVE_INTEGER = (111, "A value less than 1 was specified for the 'max' parameter. The value must be an integer greater than zero.")
    STPID_NOT_INTEGER = (112, "At least one of the supplied values for the 'stpid' parameter is not an integer value. The first invalid id is returned.")
    INVALID_PARAMETER = (500, "The query string contains a parameter that is not supported by the train tracker API, currently supported parameters are: 'mapid', 'key', 'rt', 'stpid', 'max'.")
    SERVER_ERROR = (900, "A server error occurred.")

    def __init__(self, code, explanation):
        self.code = code
        self.explanation = explanation

    @classmethod
    def from_code(cls, code):
        for error in cls:
            if error.code == code:
                return error
        return None 
    
# TODO: add other error codes
