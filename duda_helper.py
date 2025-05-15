import os, requests, base64

BASE = "https://api.duda.co/api"
AUTH = (os.environ["DUDA_API_USERNAME"], os.environ["DUDA_API_PASSWORD"])

def create_site(template_id: str, site_name: str):
    res = requests.post(
        f"{BASE}/sites/multiscreen/{site_name}",
        auth=AUTH,
        json={"template_id": template_id}
    )
    res.raise_for_status()
    return res.json()["site_name"]    # should echo back

def set_site_data(site_name: str, data: dict):
    res = requests.put(
        f"{BASE}/sites/multiscreen/{site_name}/siteData",
        auth=AUTH,
        json={"data": data}
    )
    res.raise_for_status()
