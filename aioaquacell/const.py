""" Constants for Aquacell API. """
from enum import StrEnum, unique

from aioaquacell.brand_credentials import BrandCredentials


@unique
class Brand(StrEnum):
    AQUACELL = "aquacell"
    HARVEY = "harvey"


BASE_API_URL = "https://y7xyrocicl.execute-api.eu-west-1.amazonaws.com"
ALL_SOFTENERS = f"{BASE_API_URL}/prod/v1/softeners/all"
REGION_NAME = "eu-west-1"

SUPPORTED_BRANDS: dict[str, BrandCredentials] = {
    Brand.AQUACELL: BrandCredentials(name="AquaCell",
                                      client_id="64kp67l1jo9toeesan7s1sdpae",
                                      pool_id=f"{REGION_NAME}_noZbcE2Av",
                                      identity_pool_id=f"{REGION_NAME}:f44120d5-bd20-4461-b282-1ed637861951"),
    Brand.HARVEY: BrandCredentials(name="Harvey",
                                    client_id="67c9dtgnbjid8l9dh5juih2iq4",
                                    pool_id=f"{REGION_NAME}_gtX9aUXzh",
                                    identity_pool_id=f"{REGION_NAME}:f8177510-75ef-4533-a317-9ac8d240fcef"),
}
