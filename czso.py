import requests
from bs4 import BeautifulSoup
import unicodedata

def czso_get_website_content(ico):
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


def main():
    ico = "25110161"  # Replace this with any valid ICO
    content = czso_get_website_content(ico)
    parsed_data = czso_parse_content(content)[0]
    print(parsed_data)
    


if __name__ == "__main__":
    main()
