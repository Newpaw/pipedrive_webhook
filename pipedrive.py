from ares import get_company_data_ares
import requests
from dataclasses import dataclass
from typing import List
import json
import os

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
    new_legal_form: str,
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



def different_ico(data:json) -> bool:
    current_layer = data['current'].get('7d2ccc518c77ec9a5cefc1d88ef617bf8b005586')
    previous_layer = data['previous'].get('7d2ccc518c77ec9a5cefc1d88ef617bf8b005586')
    if current_layer == previous_layer:
        return False
    else:
        return True






def main():
    #companies = get_companies()
    #for company in companies:
    #    if company.ico:
    #        company_ares = get_company_data_ares(str(company.ico.strip()))
    #        print(company_ares.name)
    #        change_company_data(
    #            company_id=company.id_pipedrive,
    #            new_address=f"{company_ares.address}, {company_ares.psc}",
    #            new_ares_name=company_ares.name,
    #            new_business_field=company_ares.business_fields,
    #            new_legal_form=company_ares.legal_form,
    #            new_size=company_ares.size,
    #        )
    pass
if __name__ == "__main__":
    main()
