import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List

@dataclass
class Company:
    """
    Třída Company je datový model, který reprezentuje informace o společnosti. Každá instance této třídy uchovává jednu sadu informací o konkrétní společnosti.

    Třída má následující atributy:

    ico: IČO (identifikační číslo osoby), jedinečný identifikátor společnosti.
    name: Jméno společnosti.
    adresa: Adresa společnosti.
    psc: Poštovní směrovací číslo (PSČ) společnosti.
    pravni_subjekt: Právní forma společnosti (např. akciová společnost, společnost s ručením omezeným atd.).
    obor_cinnosti: Obor činnosti, ve kterém společnost působí.
    velikost: Velikost společnosti podle počtu zaměstnanců."""

    ico: str
    name: str
    address: str
    psc: str
    legal_form: str
    business_fields: List[str]
    size: str

# Mapování názvů atributů na odpovídající značky XML
ATTRIBUTE_TAGS = {
    "name": "D:OF",
    "address": "D:UC",
    "psc": "D:PB",
    "legal_form": "D:NPF",
    "size": "D:KPP",
}

def get_soup(ico: str, ares_url: str) -> BeautifulSoup:
    response = requests.get(ares_url + str(ico))
    return BeautifulSoup(response.content, "lxml-xml")


def extract_data(soup: BeautifulSoup, tag: str) -> str:
    found = soup.find(tag)
    return found.text if found else None


def extract_business_fields(soup: BeautifulSoup) -> List[str]:
    business_fields = soup.find_all("D:Obor_cinnosti")
    if not business_fields:
        return []
    
    fields = [field.find("D:T").text for field in business_fields if field.find("D:T")]
    return "; ".join(fields) if fields else None


def get_company_data_ares(ico: str, ares_url: str = "http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_bas.cgi?ico=") -> Company:
    soup = get_soup(ico, ares_url)

    attributes = {attr: extract_data(soup, tag) for attr, tag in ATTRIBUTE_TAGS.items()}
    attributes["ico"] = ico
    attributes["business_fields"] = extract_business_fields(soup)

    return Company(**attributes)



def main():
    pass


if __name__ == "__main__":
    pass
