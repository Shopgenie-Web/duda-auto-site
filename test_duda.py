import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("2669cb120e", "qItYKj02wXD8")
url = "https://api.duda.co/api/sites/multiscreen/create"
payload = {"template_id": "e08fda61"}

resp = requests.post(
    url,
    auth=auth,
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
    json=payload
)

print(resp.status_code)
print(resp.text)
