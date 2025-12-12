import random
import string
from datetime import datetime

def generate_ai_reference(vaccine_type):
    # Map vaccine types to short codes
    type_codes = {
        "Measles": "MSL",
        "Polio": "POL",
        "BCG": "BCG",
        "Immunization": "IMM",
        "Chickenpox": "CHK",
        "General Health Check": "GHC"
    }

    code = type_codes.get(vaccine_type, "GEN")

    date_part = datetime.now().strftime("%Y%m%d")

    random_part = ''.join(random.choices(string.hexdigits.upper(), k=5))

    reference = f"KGH-{code}-{date_part}-{random_part}"
    return reference


def generate_ai_checkup_reference(check_type):
    type_codes = {
        "Eye Check-up": "EYE",
        "Dental Check-up": "DEN",
        "Both Eye & Dental": "BOTH"
    }
    code = type_codes.get(check_type, "GEN")
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"KGH-{code}-{date_part}-{random_part}"
