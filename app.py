import os
import logging
from flask import Flask, request
from threading import Thread
from typing import Optional


from pipedrive import change_pipedrive_company_data
from helper import different_and_correct_ico, different_vat
from api_my_ares import get_ares_companies, get_companies_by_vat

logging.basicConfig(
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")


def process_company(data):
    company_id = data["meta"].get("id")
    new_ico = data["current"].get("7d2ccc518c77ec9a5cefc1d88ef617bf8b005586")
    new_vat = data["current"].get("29d4a8de55841cc13da1337ea8fd4b3278868c68")
    ares_company = get_ares_companies(new_ico)
    if ares_company:
        change_pipedrive_company_data(
            company_id=company_id,
            new_ares_name=ares_company.name,
            new_address=ares_company.address,
            new_size=ares_company.size,
            new_business_field='; '.join(ares_company.business_fields) if isinstance(ares_company.business_fields, list) else None,
            new_legal_form=ares_company.legal_form,
            ares_main_economic_activity_cz_nace=ares_company.main_cz_nace,
            ares_based_main_economic_activity_cz_nace=ares_company.based_main_cz_nace
        )
    vat_company = get_companies_by_vat(new_vat)

    if vat_company:
        change_pipedrive_company_data(
            company_id=company_id,
            new_ares_name=vat_company.name,
            new_address=vat_company.address
        )



def process_data(data):
    try:
        if different_and_correct_ico(data) or different_vat(data):
            process_company(data)
    except Exception as e:
        logging.error(f"Error processing data: {e}")
        

@app.route("/", methods=["GET"])
def index():
    if "X-Forwarded-For" in request.headers:
        client_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
        
    else:
        client_ip = request.remote_addr

    logging.info(f"Someone from IP {client_ip} hit the site https://pipedriveares.mluvii.com/.")
    return "ok", 200


@app.route('/<path:subpath>', methods=["POST"])
def webhook(subpath):
    if subpath != WEBHOOK_URL:
        logging.warning(f"{subpath} not allowed!")
        return "Not Found", 404
    
    data = request.get_json()
    if data is None:
        logging.error("Bad request received in webhook")
        return "Bad Request", 400

    thread = Thread(target=process_data, args=(data,))
    thread.start()

    return "", 200


if __name__ == "__main__":
    app.run(port=5000)
