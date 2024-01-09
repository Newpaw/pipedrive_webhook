
import requests
from typing import Optional, List
import logging
from dataclasses import dataclass

from pipedrive import get_pipedrive_companies, change_pipedrive_company_data

logging.basicConfig(
    format='[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


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
    url = f"https://ares.novopacky.com/company/{strip_ico}"
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
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
    except requests.RequestException as e:
        logging.error(f"Error fetching data from ARES for ICO {ico}: {e}")
        return None




def main():
    companies = get_pipedrive_companies()

    for company in companies:
        if company is not None and company.ico:
            ares_company = get_ares_companies(company.ico)
            if ares_company:
                change_pipedrive_company_data(company_id=company.id_company,
                                        new_ares_name=ares_company.name,
                                        new_size = ares_company.size,
                                        new_address = ares_company.address,
                                        new_business_field = '; '.join(ares_company.business_fields) if isinstance(ares_company.business_fields, list) else None,
                                        new_legal_form = ares_company.legal_form,
                                        ares_main_economic_activity_cz_nace = ares_company.main_cz_nace,
                                        ares_based_main_economic_activity_cz_nace = ares_company.based_main_cz_nace
                                        )
                logging.info(f"Done {company.ico}")
            else:
                logging.warning(f"ARES data not found for ICO {company.ico}")

if __name__ == "__main__":
    main()
