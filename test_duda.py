import requests
from requests.auth import HTTPBasicAuth

resp = requests.post(
    "https://api.duda.co/api/sites/multiscreen/create",
    auth=HTTPBasicAuth("2669cb120e", "qItYKj02wXD8"),
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
    json={"template_id": "e08fda61"}
)
print(resp.status_code)
print(resp.text)
