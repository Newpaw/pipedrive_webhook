import os
import logging
from flask import Flask, request
from threading import Thread


from pipedrive import get_pipedrive_companies, change_pipedrive_company_data
from helper import different_and_correct_ico
from api_my_ares import get_ares_companies

logging.basicConfig(
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")




def process_data(data):
    if different_and_correct_ico(data):
        pipedrive_companies = get_pipedrive_companies()
        new_ico = data["current"].get("7d2ccc518c77ec9a5cefc1d88ef617bf8b005586")
        for pipedrive_company in pipedrive_companies:
            if pipedrive_company.ico == str(new_ico):
                logging.debug(pipedrive_company)
                ares_company = get_ares_companies(new_ico)
                change_pipedrive_company_data(
                    company_id=pipedrive_company.id_company,
                    new_ares_name=ares_company.name,
                    new_address=ares_company.address,
                    new_size=ares_company.size,
                    new_business_field='; '.join(ares_company.business_fields) if isinstance(ares_company.business_fields, list) else None,
                    new_legal_form=ares_company.legal_form,
                    ares_main_economic_activity_cz_nace=ares_company.main_cz_nace,
                    ares_based_main_economic_activity_cz_nace=ares_company.based_main_cz_nace

                )


@app.route("/", methods=["GET"])
def index():
    logging.info("Someone hit the site https://pipedriveares.mluvii.com/.")
    return "ok", 200


@app.route(f"/{WEBHOOK_URL}", methods=["POST"])
def webhook():
    data = request.get_json()
    if data is None:
        return "Bad Request", 400

    thread = Thread(target=process_data, args=(data,))
    thread.start()

    return "", 200


if __name__ == "__main__":
    app.run(port=5000)
