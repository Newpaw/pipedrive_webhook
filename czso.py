import requests
from bs4 import BeautifulSoup
import unicodedata
from typing import List

def czso_get_website_content(ico:str):
    url = f"https://apl.czso.cz/res/detail?ico={ico}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # If the response contains an HTTP error status code, raise an exception
    except requests.RequestException as e: 
        print(f"Error occurred: {e}")
        return None

    return response.content


def czso_parse_content(content):
    if content is None:
        print("No content to parse.")
        return None

    try:
        soup = BeautifulSoup(content, 'html.parser')
        data = soup.select('body > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(7) > div:nth-of-type(2)')
        
        # Normalize unicode characters in the extracted data
        normalized_data = [unicodedata.normalize("NFKD", item.get_text()) for item in data]

        return normalized_data
    except Exception as e:
        print(f"Error occurred while parsing: {e}")
        return None


def czso_get_base_cz_nace(input_string:str) -> str:
    # Slovník definující hlavní kategorie
    categories = {
        'A': 'A - Zemědělství, lesnictví, rybářství',
        'B': 'B - Těžba a dobývání',
        'C': 'C - Zpracovatelský průmysl',
        'D': 'D - Výroba a rozvod elektřiny, plynu, tepla a klimatizovaného vzduchu',
        'E': 'E - Zásobování vodou; činnosti související s odpadními vodami, odpady a sanacemi',
        'F': 'F - Stavebnictví',
        'G': 'G - Velkoobchod a maloobchod; opravy a údržba motorových vozidel',
        'H': 'H - Doprava a skladování',
        'I': 'I - Ubytování, stravování a pohostinství',
        'J': 'J - Informační a komunikační činnosti',
        'K': 'K - Peněžnictví a pojišťovnictví',
        'L': 'L - Činnosti v oblasti nemovitostí',
        'M': 'M - Profesní, vědecké a technické činnosti',
        'N': 'N - Administrativní a podpůrné činnosti',
        'O': 'O - Veřejná správa a obrana; povinné sociální zabezpečení',
        'P': 'P - Vzdělávání',
        'Q': 'Q - Zdravotní a sociální péče',
        'R': 'R - Kulturní, zábavní a rekreační činnosti',
        'S': 'S - Ostatní činnosti',
        'T': 'T - Činnosti domácností jako zaměstnavatelů; činnosti domácností produkujících blíže neurčené výrobky a služby pro vlastní potřebu',
        'U': 'U - Činnosti exteritoriálních organizací a orgánů',
    }

    categories_num = {
        '01': 'A - Zemědělství, lesnictví, rybářství',
        '02': 'A - Zemědělství, lesnictví, rybářství',
        '03': 'A - Zemědělství, lesnictví, rybářství',
        '05': 'B - Těžba a dobývání',
        '06': 'B - Těžba a dobývání',
        '07': 'B - Těžba a dobývání',
        '08': 'B - Těžba a dobývání',
        '09': 'B - Těžba a dobývání',
        '10': 'C - Zpracovatelský průmysl',
        '11': 'C - Zpracovatelský průmysl',
        '12': 'C - Zpracovatelský průmysl',
        '13': 'C - Zpracovatelský průmysl',
        '14': 'C - Zpracovatelský průmysl',
        '15': 'C - Zpracovatelský průmysl',
        '16': 'C - Zpracovatelský průmysl',
        '17': 'C - Zpracovatelský průmysl',
        '18': 'C - Zpracovatelský průmysl',
        '19': 'C - Zpracovatelský průmysl',
        '20': 'C - Zpracovatelský průmysl',
        '21': 'C - Zpracovatelský průmysl',
        '22': 'C - Zpracovatelský průmysl',
        '23': 'C - Zpracovatelský průmysl',
        '24': 'C - Zpracovatelský průmysl',
        '25': 'C - Zpracovatelský průmysl',
        '26': 'C - Zpracovatelský průmysl',
        '27': 'C - Zpracovatelský průmysl',
        '28': 'C - Zpracovatelský průmysl',
        '29': 'C - Zpracovatelský průmysl',
        '30': 'C - Zpracovatelský průmysl',
        '31': 'C - Zpracovatelský průmysl',
        '32': 'C - Zpracovatelský průmysl',
        '33': 'C - Zpracovatelský průmysl',
        '35': 'D - Výroba a rozvod elektřiny, plynu, tepla a klimatizovaného vzduchu',
        '36': 'E - Zásobování vodou; činnosti související s odpadními vodami, odpady a sanacemi',
        '37': 'E - Zásobování vodou; činnosti související s odpadními vodami, odpady a sanacemi',
        '38': 'E - Zásobování vodou; činnosti související s odpadními vodami, odpady a sanacemi',
        '39': 'E - Zásobování vodou; činnosti související s odpadními vodami, odpady a sanacemi',
        '41': 'F - Stavebnictví',
        '42': 'F - Stavebnictví',
        '43': 'F - Stavebnictví',
        '45': 'G - Velkoobchod a maloobchod; opravy a údržba motorových vozidel',
        '46': 'G - Velkoobchod a maloobchod; opravy a údržba motorových vozidel',
        '47': 'G - Velkoobchod a maloobchod; opravy a údržba motorových vozidel',
        '49': 'H - Doprava a skladování',
        '50': 'H - Doprava a skladování',
        '51': 'H - Doprava a skladování',
        '52': 'H - Doprava a skladování',
        '53': 'H - Doprava a skladování',
        '55': 'I - Ubytování, stravování a pohostinství',
        '56': 'I - Ubytování, stravování a pohostinství',
        '58':  'J - Informační a komunikační činnosti',
        '59':  'J - Informační a komunikační činnosti',
        '60':  'J - Informační a komunikační činnosti',
        '61':  'J - Informační a komunikační činnosti',
        '62':  'J - Informační a komunikační činnosti',
        '63':  'J - Informační a komunikační činnosti',
        '64':  'K - Peněžnictví a pojišťovnictví',
        '65':  'K - Peněžnictví a pojišťovnictví',
        '66':  'K - Peněžnictví a pojišťovnictví',
        '68':  'L - Činnosti v oblasti nemovitostí',
        '69':  'M - Profesní, vědecké a technické činnosti',
        '70':  'M - Profesní, vědecké a technické činnosti',
        '71':  'M - Profesní, vědecké a technické činnosti',
        '72':  'M - Profesní, vědecké a technické činnosti',
        '73':  'M - Profesní, vědecké a technické činnosti',
        '74':  'M - Profesní, vědecké a technické činnosti',
        '75':  'M - Profesní, vědecké a technické činnosti',
        '77':  'N - Administrativní a podpůrné činnosti',
        '78':  'N - Administrativní a podpůrné činnosti',
        '79':  'N - Administrativní a podpůrné činnosti',
        '80':  'N - Administrativní a podpůrné činnosti',
        '81':  'N - Administrativní a podpůrné činnosti',
        '82':  'N - Administrativní a podpůrné činnosti',
        '84':  'O - Veřejná správa a obrana; povinné sociální zabezpečení',
        '85':  'P - Vzdělávání', 
        '86':  'Q - Zdravotní a sociální péče',
        '87':  'Q - Zdravotní a sociální péče',
        '88':  'Q - Zdravotní a sociální péče',  
        '90':  'R - Kulturní, zábavní a rekreační činnosti',
        '91':  'R - Kulturní, zábavní a rekreační činnosti',
        '92':  'R - Kulturní, zábavní a rekreační činnosti',
        '93':  'R - Kulturní, zábavní a rekreační činnosti',     
        '94':  'S - Ostatní činnosti',
        '95':  'S - Ostatní činnosti',
        '96':  'S - Ostatní činnosti',     
        '97':  'T - Činnosti domácností jako zaměstnavatelů; činnosti domácností produkujících blíže neurčené výrobky a služby pro vlastní potřebu',
        '98':  'T - Činnosti domácností jako zaměstnavatelů; činnosti domácností produkujících blíže neurčené výrobky a služby pro vlastní potřebu',
        '99': 'U - Činnosti exteritoriálních organizací a orgánů',

    }

    first_character = input_string[0]
    first_two_characters = input_string[:2]


    if first_character.isalpha():
        return categories.get(first_character.upper(), 'Neznámá kategorie')
    elif first_character.isdigit():
        return categories_num.get(first_two_characters, 'Neznámá sub-kategorie' )



def main():
    #ico = "03739741"  # Replace this with any valid ICO
    #content = czso_get_website_content(ico)
    #cz_nace = czso_parse_content(content)[0]
    #print(cz_nace)
    #cz_nace_main = czso_get_base_cz_nace(str(cz_nace))
    #print(cz_nace_main)
    pass
    


if __name__ == "__main__":
    main()
