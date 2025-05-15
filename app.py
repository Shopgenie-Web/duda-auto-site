import json, time
from slugify import slugify
from sheets_helper import get_row_dict, set_processed
from duda_helper import create_site, set_site_data
from email_helper import send_email
from flask import jsonify

@app.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json(force=True)
    row_num = int(payload["row"])
    record = get_row_dict(row_num)

    # 1. Clone site
    site_slug = slugify(record["Shop Name (as you want it displayed throughout your site)"])[:30]
    site_slug = f"{site_slug}-{int(time.time())}"      # uniqueness
    site_name = create_site(os.environ["TEMPLATE_ID"], site_slug)

    # 2. Push Site Data (keys must exist in template)
    site_data = {
        "shop_name": record["Shop Name (as you want it displayed throughout your site)"],
        "phone": record["Phone number"],
        "primary_color": record["Primary Color for Color Scheme (Use color codes eg. #ffffff)"],
        "secondary_color": record["Secondary Color for Color Scheme (Use color codes eg. #ffffff)"],
        # add other mappings here…
    }
    set_site_data(site_name, site_data)

    # 3. Email customer
    draft_url = f"https://{site_name}.multiscreensite.com/"
    html = f"""
        <p>Hi,</p>
        <p>Your draft website is ready: <a href="{draft_url}">{draft_url}</a></p>
        <p>We'll be in touch with next steps!</p>
    """
    send_email(record["Please provide an email address that you'd like to use to receive a link to your website draft after completing this form & to receive job applications from your website"],
               os.environ["EMAIL_SUBJECT"], html)

    # 4. Mark processed
    set_processed(row_num)

    return jsonify({"site": site_name, "row": row_num})
