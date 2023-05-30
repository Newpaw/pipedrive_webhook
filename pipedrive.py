import json
import os
import requests
import logging

from typing import List, Optional

from dataclasses import dataclass
from helper import verify_ico




logging.basicConfig(
    format='[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')



@dataclass
class Pipedrive_Company:
    id_company: str
    ico: str = None
    name: Optional[str] = None
    address: Optional[str] = None
    psc: Optional[str] = None
    legal_form: Optional[str] = None
    business_fields: Optional[List[str]] = None
    size: Optional[str] = None
    main_cz_nace: Optional[str] = None
    based_main_cz_nace: Optional[str] = None


def get_pipedrive_companies() -> List[Pipedrive_Company]:
    api_token = os.environ.get('API_TOKEN') 
    url = "https://api.pipedrive.com/v1/organizations?api_token=" + api_token

    start = 0
    limit = 100  # This can be any number up to 500, the maximum allowed by Pipedrive
    more_items = True

    companies_list = []

    while more_items:
        response = requests.get(url + "&start=" + str(start) + "&limit=" + str(limit))
        data = response.json()
        if data["success"]:
            companies = data["data"]
            for company in companies:
                id_ = company["id"]
                name = company["name"]
                address = company["address"]
                size = company["8ef4ed6f463f487c5602a4be1f6ebe7206770ed9"]
                ico = company["7d2ccc518c77ec9a5cefc1d88ef617bf8b005586"]

                instance_company = Pipedrive_Company(id_company=id_,ico=ico,name=name,address=address,size=size)
                companies_list.append(instance_company)

            # Check if there are more companies to fetch
            more_items = data["additional_data"]["pagination"][
                "more_items_in_collection"
            ]
            if more_items:
                start += (
                    limit  # If so, increment the start parameter for the next request
                )

        else:
            logging.error("API request failed, reason: ", data["error"])
            break
    return companies_list


def change_pipedrive_company_data(
    company_id: int,
    new_ares_name: str = None,
    new_size: str = None,
    new_address: str = None,
    new_business_field: str = None,
    new_legal_form: str = None,
    ares_main_economic_activity_cz_nace: str = None,
    ares_based_main_economic_activity_cz_nace:str = None,
):
    api_token = os.getenv('API_TOKEN')
    url = f"https://api.pipedrive.com/v1/organizations/{company_id}?api_token={api_token}"

    # Mapování klíčů na hodnoty
    data_keys = {
        "3dbfb80ada1c97f7f448c152a235be8caac790ba": new_ares_name,
        "8ef4ed6f463f487c5602a4be1f6ebe7206770ed9": new_size,
        "b75689d548fb12a231391c7c6cab088d2ce82fe7": new_address,
        "87be25f87f72beb20a053be3eb0d2eac6022889a": new_business_field,
        "d81ddd0705469fa140c83ec11f11f69458255107": new_legal_form,
        "e0220d408af2bc5442d14a19eb366597272d57ae": ares_main_economic_activity_cz_nace,
        "09b652932939205881a0618b334b87136ecef2d7": ares_based_main_economic_activity_cz_nace,
    }

    # Filtrujeme hodnoty, které nejsou None
    data = {key: value for key, value in data_keys.items() if value is not None}

    logging.info(data)
    
    # Poslat PUT požadavek na API
    response = requests.put(url, json=data)

    # Zkontrolovat odpověď a zpracovat výsledek
    if response.status_code == 200:
        logging.info(f"Company {new_ares_name if new_ares_name else 'unknown'} with company id {company_id} processed!")
    else:
        logging.error("Chyba při aktualizaci názvu společnosti!")






def main():
    pass
if __name__ == "__main__":
    main()
