import os
import requests
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE = "https://api.duda.co/api"
AUTH = (os.environ["DUDA_API_USERNAME"], os.environ["DUDA_API_PASSWORD"])

def create_site(template_id: str, site_name: str):
    url = f"{BASE}/sites/multiscreen/create"  # Correct endpoint for creating a site
    logger.info(f"🌐 Sending request to create site: {site_name} using template: {template_id}")
    
    payload = {
        "template_id": template_id,
        "site_slug": site_name,  # You can add more fields if necessary
    }
    
    logger.debug(f"Request payload: {payload}")
    
    try:
        res = requests.post(url, auth=AUTH, json=payload)
        res.raise_for_status()  # Will raise an exception for HTTP errors
        
        logger.info(f"🎉 Site created successfully: {res.json()}")
        return res.json()["site_name"]  # Assuming this is the correct response key
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred: {err}")
        logger.error(f"Response: {res.text}")
        raise  # Re-raise the exception for further handling
    except Exception as err:
        logger.error(f"Unexpected error occurred: {err}")
        raise  # Re-raise the exception for further handling

def set_site_data(site_name: str, data: dict):
    url = f"{BASE}/sites/multiscreen/{site_name}/siteData"
    logger.info(f"📦 Sending request to set data for site: {site_name}")
    
    payload = {
        "data": data
    }
    
    logger.debug(f"Request payload: {payload}")
    
    try:
        res = requests.put(url, auth=AUTH, json=payload)
        res.raise_for_status()  # Will raise an exception for HTTP errors
        
        logger.info(f"✅ Data set successfully for site: {site_name}")
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP error occurred while setting site data: {err}")
        logger.error(f"Response: {res.text}")
        raise  # Re-raise the exception for further handling
    except Exception as err:
        logger.error(f"Unexpected error occurred while setting site data: {err}")
        raise  # Re-raise the exception for further handling
