import json
import os
import requests
import logging

from dataclasses import dataclass
from typing import List

from czso import czso_get_website_content, czso_parse_content, czso_get_base_cz_nace
from ares import get_company_data_ares
from verification import verify_ico

logging.basicConfig(
    format='[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


@dataclass
class Pipedrive_Company:
    id_pipedrive: int
    name: str
    address: str
    size: str
    ico: str


def get_companies() -> List[Pipedrive_Company]:
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

                instance_company = Pipedrive_Company(id_, name, address, size, ico)
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
            print("API request failed, reason: ", data["error"])
            break
    return companies_list


def change_company_data(
    company_id: int,
    new_ares_name: str,
    new_size: str,
    new_address: str,
    new_business_field: str,
    new_legal_form: str
):
    api_token = os.environ.get('API_TOKEN')

    url = (
        f"https://api.pipedrive.com/v1/organizations/{company_id}?api_token={api_token}"
    )
    # Sestavte data pro aktualizaci názvu společnosti
    data = {
        "3dbfb80ada1c97f7f448c152a235be8caac790ba": new_ares_name,
        "8ef4ed6f463f487c5602a4be1f6ebe7206770ed9": new_size,
        "b75689d548fb12a231391c7c6cab088d2ce82fe7": new_address,
        "87be25f87f72beb20a053be3eb0d2eac6022889a": new_business_field,
        "d81ddd0705469fa140c83ec11f11f69458255107": new_legal_form,
    }

    # Poslat PUT požadavek na API
    response = requests.put(url, json=data)

    # Zkontrolovat odpověď a zpracovat výsledek
    if response.status_code == 200:
        pass
    else:
        print("Chyba při aktualizaci názvu společnosti.")
        print(response.json())

def change_main_economic_activity_cz_nace(
    company_id: int,
    ares_main_economic_activity_cz_nace: str,
    ares_based_main_economic_activity_cz_nace:str,
):
    api_token = os.environ.get('API_TOKEN')

    url = (
        f"https://api.pipedrive.com/v1/organizations/{company_id}?api_token={api_token}"
    )
    # Sestavte data pro aktualizaci názvu společnosti
    data = {
        "e0220d408af2bc5442d14a19eb366597272d57ae": ares_main_economic_activity_cz_nace,
        "09b652932939205881a0618b334b87136ecef2d7": ares_based_main_economic_activity_cz_nace,
    }

    # Poslat PUT požadavek na API
    response = requests.put(url, json=data)

    # Zkontrolovat odpověď a zpracovat výsledek
    if response.status_code == 200:
        pass
    else:
        print("Chyba při aktualizaci názvu společnosti.")
        print(response.json())


def different_and_correct_ico(data:json) -> bool:
    current_layer = data['current'].get('7d2ccc518c77ec9a5cefc1d88ef617bf8b005586')
    previous_layer = data['previous'].get('7d2ccc518c77ec9a5cefc1d88ef617bf8b005586')
    exist_the_ico = verify_ico(current_layer)

    logging.info(f"The verification  for IČ {current_layer} is {exist_the_ico}")

    if current_layer == previous_layer or not exist_the_ico:
        return False
    else:
        return True






def main():
    companies = get_companies()
    for company in companies:
        if company.ico:
            ico = str(company.ico.strip())
            company_ares = get_company_data_ares(ico)
            content = czso_get_website_content(ico)
            if czso_parse_content(content):
                ares_main_economic_activity_cz_nace = czso_parse_content(content)[0]
                change_company_data(
                    company_id=company.id_pipedrive,
                    new_address=f"{company_ares.address}, {company_ares.psc}",
                    new_ares_name=company_ares.name,
                    new_business_field=company_ares.business_fields,
                    new_legal_form=company_ares.legal_form,
                    new_size=company_ares.size,
                )
                change_main_economic_activity_cz_nace(
                    company_id=company.id_pipedrive,
                    ares_main_economic_activity_cz_nace = ares_main_economic_activity_cz_nace,
                    ares_based_main_economic_activity_cz_nace=czso_get_base_cz_nace(str(ares_main_economic_activity_cz_nace)),
                )
                print(czso_get_base_cz_nace(str(ares_main_economic_activity_cz_nace)))
            else:
                change_company_data(
                    company_id=company.id_pipedrive,
                    new_address=f"{company_ares.address}, {company_ares.psc}",
                    new_ares_name=company_ares.name,
                    new_business_field=company_ares.business_fields,
                    new_legal_form=company_ares.legal_form,
                    new_size=company_ares.size,
                )
                print(ico)

if __name__ == "__main__":
    main()
