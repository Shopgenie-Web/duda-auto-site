import os
import requests
import base64
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("duda_helper")

BASE = "https://api.duda.co/api"

# Manually encode basic auth credentials
def _auth_header():
    user = os.environ["DUDA_API_USERNAME"]
    pw = os.environ["DUDA_API_PASSWORD"]
    credentials = f"{user}:{pw}"
    token = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {token}"}

def create_site(template_id: str, site_name: str):
    url = f"{BASE}/sites/multiscreen/create"
    payload = {
        "template_id": template_id,
        "site_name": site_name,
        "site_domain": site_name,  # optional, but can help for uniqueness
        "editor_type": "responsive"  # optional, but keeps things explicit
    }

    headers = {
        **_auth_header(),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    logger.info(f"🌐 Sending request to create site: {site_name} using template: {template_id}")
    logger.debug(f"Payload: {payload}")

    res = requests.post(url, headers=headers, json=payload)

    try:
        res.raise_for_status()
        logger.info(f"✅ Site created successfully: {res.json()}")
        return res.json()["site_name"]
    except requests.exceptions.HTTPError as err:
        logger.error(f"❌ HTTP error occurred: {err}")
        logger.error(f"Response body: {res.text}")
        raise

def set_site_data(site_name: str, data: dict):
    url = f"{BASE}/sites/multiscreen/{site_name}/siteData"
    headers = {
        **_auth_header(),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    logger.info(f"📦 Setting site data for: {site_name}")
    res = requests.put(url, headers=headers, json={"data": data})

    try:
        res.raise_for_status()
        logger.info(f"✅ Site data injected successfully.")
    except requests.exceptions.HTTPError as err:
        logger.error(f"❌ Error setting site data: {err}")
        logger.error(f"Response body: {res.text}")
        raise
