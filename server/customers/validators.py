
from cerberus.validator import Validator

from utils.validators import protobuf_validator

CUSTOMER_SCHEMA = {
    "name": {
        "required": True,
        "minlength": 3,
        "maxlength": 42,
    }
}


@protobuf_validator
def validate_customer(customer):
    """Validate a customer"""
    validator = Validator(CUSTOMER_SCHEMA)
    result = validator.validate(customer)
    errors = validator.errors

    return result, errors

