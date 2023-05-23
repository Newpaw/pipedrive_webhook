import os
import requests
import logging
import redis
import pickle

from typing import List, Optional
from dataclasses import dataclass


logging.basicConfig(
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# získání instance Redis
try:
    redis_instance = redis.Redis(host="redis_next_new", port=6379, db=0)
except redis.RedisError as e:
    logging.error(f"Nepodařilo se připojit k Redisu: {e}")
    redis_instance = None

@dataclass
class Pipedrive_Company:
    id_company: str
    ico: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    psc: Optional[str] = None
    legal_form: Optional[str] = None
    business_fields: Optional[List[str]] = None
    size: Optional[str] = None
    main_cz_nace: Optional[str] = None
    based_main_cz_nace: Optional[str] = None


def get_pipedrive_companies() -> List[Pipedrive_Company]:
    # Zkuste načíst seznam firem z cache
    companies_list = get_pipedrive_companies_from_cache()
    if companies_list is not None and len(companies_list) > 0:
        return companies_list

    # Pokud data nejsou v cache nebo jsou prázdná, načtěte je ze serveru
    api_token = os.environ.get("API_TOKEN")
    url = "https://api.pipedrive.com/v1/organizations?api_token=" + api_token

    start = 0
    limit = 100
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

                instance_company = Pipedrive_Company(
                    id_company=id_, ico=ico, name=name, address=address, size=size
                )
                companies_list.append(instance_company)

            more_items = data["additional_data"]["pagination"]["more_items_in_collection"]
            if more_items:
                start += limit

        else:
            logging.error("API request failed, reason: ", data["error"])
            break


    cache_pipedrive_companies(companies_list)
    return companies_list


def cache_pipedrive_companies(companies_list):
    pickled_companies_list = pickle.dumps(companies_list)
    try:
        redis_instance.setex('pipedrive_companies', 24 * 60 * 60, pickled_companies_list)
    except redis.RedisError as e:
        logging.error(f"Chyba při ukládání do Redisu: {e}")
        return None


def get_pipedrive_companies_from_cache():
    try:
        pickled_companies_list = redis_instance.get('pipedrive_companies')
        logging.info("Získání listu z cache!")
    except redis.RedisError as e:
        logging.error(f"Chyba při získávání dat z Redisu: {e}")
        return None

    if pickled_companies_list is not None:
        companies_list = pickle.loads(pickled_companies_list)
        if len(companies_list) > 0:
            logging.info(companies_list[0])
        return companies_list

    return []


def change_pipedrive_company_data(
    company_id: int,
    new_ares_name: str,
    new_size: str,
    new_address: str,
    new_business_field: str,
    new_legal_form: str,
    ares_main_economic_activity_cz_nace: str,
    ares_based_main_economic_activity_cz_nace: str,
):
    api_token = os.environ.get("API_TOKEN")

    url = (
        f"https://api.pipedrive.com/v1/organizations/{company_id}?api_token={api_token}"
    )
    data = {
        "3dbfb80ada1c97f7f448c152a235be8caac790ba": new_ares_name,
        "8ef4ed6f463f487c5602a4be1f6ebe7206770ed9": new_size,
        "b75689d548fb12a231391c7c6cab088d2ce82fe7": new_address,
        "87be25f87f72beb20a053be3eb0d2eac6022889a": new_business_field,
        "d81ddd0705469fa140c83ec11f11f69458255107": new_legal_form,
        "e0220d408af2bc5442d14a19eb366597272d57ae": ares_main_economic_activity_cz_nace,
        "09b652932939205881a0618b334b87136ecef2d7": ares_based_main_economic_activity_cz_nace,
    }

    response = requests.put(url, json=data)

    if response.status_code == 200:
        logging.info(f"Company {new_ares_name} with company id {company_id} processed!")
    else:
        logging.error("Chyba při aktualizaci názvu společnosti!")


def main():
    companies = get_pipedrive_companies()
    print(companies[0])


if __name__ == "__main__":
    main()
