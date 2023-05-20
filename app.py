import os
import logging
from flask import Flask, request
from threading import Thread
from ares import get_company_data_ares
from pipedrive import get_companies, change_company_data, different_ico, change_main_economic_activity_cz_nace
from czso import czso_get_website_content, czso_parse_content, czso_get_base_cz_nace


logging.basicConfig(
    format='[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

def process_common_data(company, company_ares):
    change_company_data(
        company_id=company.id_pipedrive,
        new_address=f"{company_ares.address}, {company_ares.psc}",
        new_ares_name=company_ares.name,
        new_business_field=company_ares.business_fields,
        new_legal_form=company_ares.legal_form,
        new_size=company_ares.size,
    )

def process_data(data):
    if different_ico(data):
        companies = get_companies()
        new_ico = data['current'].get('7d2ccc518c77ec9a5cefc1d88ef617bf8b005586')
        for company in companies:
            if company.ico == str(new_ico):
                ico = str(company.ico.strip())
                company_ares = get_company_data_ares(ico)
                content = czso_get_website_content(ico)
                parsed_content = czso_parse_content(content)
                logging.info(company.name)
                process_common_data(company, company_ares)
                if parsed_content:
                    ares_main_economic_activity_cz_nace = parsed_content[0]
                    change_main_economic_activity_cz_nace(
                        company_id=company.id_pipedrive,
                        ares_main_economic_activity_cz_nace = ares_main_economic_activity_cz_nace,
                        ares_based_main_economic_activity_cz_nace = czso_get_base_cz_nace(str(ares_main_economic_activity_cz_nace)),
                    )

@app.route('/', methods=['GET'])
def index():
    logging.info("Someone hit the site https://pipedriveares.mluvii.com/.")
    return 'ok', 200

@app.route(f'/{WEBHOOK_URL}', methods=['POST'])
def webhook():
    data = request.get_json()
    if data is None:
        return 'Bad Request', 400

    thread = Thread(target=process_data, args=(data,))
    thread.start()

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)