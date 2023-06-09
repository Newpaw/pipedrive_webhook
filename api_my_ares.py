import logging
import requests

from dataclasses import dataclass
from typing import Optional, List


logging.basicConfig(
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


BASE_URL = "https://ares.novopacky.com/"


@dataclass
class AresCompany:
    """Dataclass for storing ARES company data."""

    ico: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    legal_form: Optional[str] = None
    business_fields: Optional[List[str]] = None
    size: Optional[str] = None
    main_cz_nace: Optional[str] = None
    based_main_cz_nace: Optional[str] = None


def get_ares_companies(ico: str) -> Optional[AresCompany]:
    """
    Fetch company information from the ARES service.
    :param ico: ICO of the company.
    :return: AresCompany object if successful, None otherwise.
    """
    strip_ico = str(ico).strip()
    url = f"{BASE_URL}company/{strip_ico}"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred for ICO {strip_ico}: {http_err}")
        return None
    except requests.RequestException as err:  # More specific exception
        logging.error(f"An error occurred for ICO {strip_ico}: {err}")
        return None

    logging.info(f"Response 200 for ICO {strip_ico}.")
    data = response.json()

    # Check if address and psc are not None before concatenating
    address = data.get("address")
    psc = data.get("psc")
    full_address = f"{address}, {psc}" if address and psc else address or psc

    return AresCompany(
        ico=strip_ico,
        name=data.get("name"),
        address=full_address,
        legal_form=data.get("legal_form"),
        business_fields=data.get("business_fields"),
        size=data.get("size"),
        main_cz_nace=data.get("main_cz_nace"),
        based_main_cz_nace=data.get("based_main_cz_nace"),
    )


def get_companies_by_vat(vat_number: str) -> Optional[AresCompany]:
    stripet_vat_number = str(vat_number).strip()
    url = f"{BASE_URL}companyVAT/{stripet_vat_number}"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred for VAT {stripet_vat_number}: {http_err}")
        return None
    except requests.RequestException as err:  # More specific exception
        logging.error(f"An error occurred for VAT {stripet_vat_number}: {err}")
        return None

    logging.info(f"Response 200 for VAT {stripet_vat_number}.")
    data = response.json()

    return AresCompany(name=data.get("name"), address=data.get("address"))
    

def main():
    pass


if __name__ == "__main__":
    main()
