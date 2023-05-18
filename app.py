import os
from flask import Flask, request
from threading import Thread
from ares import get_company_data_ares
from pipedrive import get_companies, change_company_data, different_ico, change_main_economic_activity_cz_nace
from czso import czso_get_website_content, czso_parse_content

app = Flask(__name__)

webhook_url = os.environ.get('WEBHOOK_URL') 

def process_data(data):
    if different_ico(data):
        companies = get_companies()
        new_ico = data['current'].get('7d2ccc518c77ec9a5cefc1d88ef617bf8b005586')
        for company in companies:
            if company.ico == str(new_ico):
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
                    )
                else:
                    change_company_data(
                        company_id=company.id_pipedrive,
                        new_address=f"{company_ares.address}, {company_ares.psc}",
                        new_ares_name=company_ares.name,
                        new_business_field=company_ares.business_fields,
                        new_legal_form=company_ares.legal_form,
                        new_size=company_ares.size,
                    )


@app.route('/', methods=['GET'])
def index():
    return 'ok', 200


@app.route(f'/{webhook_url}', methods=['POST'])
def webhook():
    data = request.get_json()
    if data is None:
        # If no data is sent or it's not in JSON format, send a "bad request" status.
        return 'Bad Request', 400

    # Spawn a new thread to process the data.
    thread = Thread(target=process_data, args=(data,))
    thread.start()

    # Immediately return a 200 response.
    return '', 200

if __name__ == '__main__':
    app.run(port=5000)