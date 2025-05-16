import os
import logging
import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger("duda_helper")
logger.setLevel(logging.INFO)

BASE = "https://api.duda.co/api"
AUTH = HTTPBasicAuth(
    os.environ["DUDA_API_USERNAME"],
    os.environ["DUDA_API_PASSWORD"],
)

def create_site(template_id: str, site_slug: str = None) -> str:
    """
    Creates a new multiscreen site from a template.
    - If site_slug is provided: clones into that exact slug via
      POST /sites/multiscreen/{site_slug}.
    - Otherwise: auto-generates slug via POST /sites/multiscreen/create.
    Returns the new site_name (slug) as returned by Duda.
    """
    if site_slug:
        url = f"{BASE}/sites/multiscreen/{site_slug}"
        payload = {"template_id": template_id}
    else:
        url = f"{BASE}/sites/multiscreen/create"
        payload = {"template_id": template_id}

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    logger.info(f"🌐 Creating site (template={template_id}) → {url}")
    logger.debug(f"Payload: {payload}")

    resp = requests.post(url, auth=AUTH, headers=headers, json=payload)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        logger.error(f"❌ create_site failed [{resp.status_code}]: {resp.text}")
        raise

    body = resp.json()
    site_name = body.get("site_name")
    logger.info(f"✅ Created site: {site_name}")
    return site_name

def set_site_data(site_name: str, data: dict):
    """
    Pushes the `data` dict into the given site's siteData endpoint.
    """
    url = f"{BASE}/sites/multiscreen/{site_name}/siteData"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    logger.info(f"📦 Setting siteData for: {site_name}")
    resp = requests.put(url, auth=AUTH, headers=headers, json={"data": data})
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        logger.error(f"❌ set_site_data failed [{resp.status_code}]: {resp.text}")
        raise

    logger.info("✅ siteData updated successfully")