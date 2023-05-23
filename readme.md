# Pipedrive Ares Application

## Overview
This application helps to process company data by fetching information from ares and then using this information to update corresponding company information on pipedrive. 

The application is built using Flask and uses pipedrive API to interact with pipedrive data.

## Key Features

- Fetches and processes company data.
- Updates the corresponding company information on Pipedrive based on the newly fetched data.
- Utilizes webhooks to trigger the process asynchronously upon receiving the post request.
- The application logs all requests received along with their IP addresses for tracing and troubleshooting.

## Prerequisites

- Python 3.8 or later
- Flask
- API_TOKEN for pipedrive API access

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Change into the directory:
    ```bash
    cd <repository-folder>
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    ```bash
    source venv/bin/activate  # for linux
    venv\Scripts\activate  # for windows
    ```

5. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set the necessary environment variables:
    ```bash
    export WEBHOOK_URL=<your_webhook_url>
    export API_TOKEN=<your_api_token>
    ```

## Directory Structure

├── Dockerfile
├── api_my_ares.py
├── app.py
├── helper.py
├── pipedrive.py
└── requirements.txt


## Usage

- To start the server, run:
    ```bash
    python app.py
    ```

## API Endpoints

- GET `/`: Returns 'ok' and logs the IP address of the requester.
- POST `/<webhook_url>`: Triggers the processing of the company data. The webhook URL is read from the environment variable `WEBHOOK_URL`.

## Disclaimer

Please ensure to handle the security aspects carefully when deploying this application. Also, ensure to use secure and unique values for `WEBHOOK_URL` and `API_TOKEN` environment variables to prevent unauthorized access.

## Contact

For any queries or issues, please contact jan.novopacky@gmail.com.

## License

This project is licensed under MIT License.
