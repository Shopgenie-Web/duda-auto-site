import logging
import os

# Log Duda credentials coming from the environment
logging.info(f"DUDA_API_USERNAME from env: {os.getenv('DUDA_API_USERNAME')}")
logging.info(f"DUDA_API_PASSWORD from env: {os.getenv('DUDA_API_PASSWORD')}")

import json
import time

from flask import Flask, request, jsonify
from sheets_helper import get_row_dict, set_processed
from duda_helper import create_site, set_site_data
from email_helper import send_email

app = Flask(__name__)

@app.route("/test-auth", methods=["GET"])
def test_auth():
    """
    Returns the Basic auth header that duda_helper will use,
    so you can verify your credentials are being encoded correctly.
    """
    import duda_helper
    return duda_helper._auth_header()

@app.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json(force=True)
    row_num = int(payload["row"])
    app.logger.info(f"🔄 Processing row {row_num}")

    # Pull the form record from Google Sheets
    record = get_row_dict(row_num)

    # 1. Clone site (auto-generated slug by Duda)
    app.logger.info("🌐 Creating site (auto-slug)")
    site_name = create_site(os.environ["TEMPLATE_ID"], None)
    app.logger.info(f"✅ Created site: {site_name}")

    # 2. Push siteData
    site_data = {
        "email": record["Please provide an email address that you'd like to use to receive a link to your website draft after completing this form & to receive job applications from your website"],
        "shop_name": record["Shop Name (as you want it displayed throughout your site)"],
        "shop_address": record["Shop Address"],
        "shop_city_state": record["Shop City & State Only (eg. Seattle, WA)"],
        "phone": record["Phone number"],
        "hours": record["Shop Hours (as you want it displayed throughout your site)"],
        "review_count": record["Current Number of Reviews (eg. 250)"],
        "logo_url": record["Shop Logo (please provide a link to the file)"],
        "primary_color": record["Primary Color for Color Scheme (Use color codes eg. #ffffff)"],
        "secondary_color": record["Secondary Color for Color Scheme (Use color codes eg. #ffffff)"],
        "motto": record["Your Motto/Slogan for The Shop"],
        "hero_image": record["Hero Section Background Image (please provide a link to the file showcasing your shop)"],
        "why_choose_us": record["Why Choose Us Content (explain why customers should choose your shop for their auto repair needs)"],
        # Coupons
        "coupon_1_amount": record["Coupon 1 (discount that is offered)"],
        "coupon_1_for": record["Coupon 1 (what is this discount for)"],
        "coupon_1_disclaimer": record["Coupon 1 (disclaimers/exceptions)"],
        "coupon_2_amount": record["Coupon 2 (discount that is offered)"],
        "coupon_2_for": record["Coupon 2 (what is this discount for)"],
        "coupon_2_disclaimer": record["Coupon 2 (disclaimers/exceptions)"],
        "coupon_3_amount": record["Coupon 3 (discount that is offered)"],
        "coupon_3_for": record["Coupon 3 (what is this discount for)"],
        "coupon_3_disclaimer": record["Coupon 3 (disclaimers/exceptions)"],
        # Services
        "service_1_name": record["Primary service offered 1 (name of service)"],
        "service_1_desc": record["Primary service offered 1 (short description of service)"],
        "service_2_name": record["Primary service offered 2 (name of service)"],
        "service_2_desc": record["Primary service offered 2 (short description of service)"],
        "service_3_name": record["Primary service offered 3 (name of service)"],
        "service_3_desc": record["Primary service offered 3 (short description of service)"],
        "additional_services_1": record["Additional services offered list 1 (include 3 or more, each on a separate line)"],
        "additional_services_2": record["Additional services offered list 2 (include 3 or more, each on a separate line)"],
        "additional_services_3": record["Additional services offered list 3 (include 3 or more, each on a separate line)"],
        # Reviews
        "review_1_content": record["Review content 1 (add a customer review)"],
        "review_1_name": record["Review 1 customer name (use proper capitalization)"],
        "review_2_content": record["Review content 2 (add a customer review)"],
        "review_2_name": record["Review 2 customer name (use proper capitalization)"],
        "review_3_content": record["Review content 3 (add a customer review)"],
        "review_3_name": record["Review 3 customer name (use proper capitalization)"],
        # Values
        "value_1_title": record["Company values 1"],
        "value_1_desc": record["Company values 1 explanation of said value"],
        "value_2_title": record["Company values 2"],
        "value_2_desc": record["Company values 2 explanation of said value"],
        "value_3_title": record["Company values 3"],
        "value_3_desc": record["Company values 3 explanation of said value"],
        # Vehicles
        "vehicle_regions": record["Manufacturer regions you support (Domestic, European, Asian, etc.)"],
        "vehicles_image": record["Vehicles Section Image (please provide a link to the file showcasing some vehicles you service)"],
        "vehicles_text": record["Vehicles section content (explain the various types of vehicles you service in a paragraph or two)"],
        "vehicle_makes_1": record["List of vehicle makes you service 1 (include 3 or more, each on a separate line)"],
        "vehicle_makes_2": record["List of vehicle makes you service 2 (include 3 or more, each on a separate line)"],
        "vehicle_makes_3": record["List of vehicle makes you service 3 (include 3 or more, each on a separate line)"],
        "vehicle_makes_4": record["List of vehicle makes you service 4 (include 3 or more, each on a separate line)"],
        # Financing
        "financing_1": record["Financing option 1"],
        "financing_1_desc": record["Financing option 1 details (explain the financing details)"],
        "financing_2": record["Financing option 2"],
        "financing_2_desc": record["Financing option 2 details (explain the financing details)"],
        "financing_3": record["Financing option 3"],
        "financing_3_desc": record["Financing option 3 details (explain the financing details)"],
        # FAQs
        "faq_1_title": record["FAQ 1 (title only)"],
        "faq_1_text": record["FAQ 1 details"],
        "faq_2_title": record["FAQ 2 (title only)"],
        "faq_2_text": record["FAQ 2 details"],
        "faq_3_title": record["FAQ 3 (title only)"],
        "faq_3_text": record["FAQ 3 details"],
        "faq_4_title": record["FAQ 4 (title only)"],
        "faq_4_text": record["FAQ 4 details"],
        "faq_5_title": record["FAQ 5 (title only)"],
        "faq_5_text": record["FAQ 5 details"],
        "faq_6_title": record["FAQ 6 (title only)"],
        "faq_6_text": record["FAQ 6 details"],
        # Location content
        "location_description": record["Location details (in a paragraph or two, talk a bit about the area that you serve)"],
        "surrounding_cities_1": record["Surrounding cities list 1 (include 3 or more, each on a separate line)"],
        "surrounding_cities_2": record["Surrounding cities list 2 (include 3 or more, each on a separate line)"],
        "surrounding_cities_3": record["Surrounding cities list 3 (include 3 or more, each on a separate line)"],
        "surrounding_cities_4": record["Surrounding cities list 4 (include 3 or more, each on a separate line)"],
        "today": record["Todays Date (mm/dd/yy)"]
    }
    app.logger.info(f"📦 Injecting siteData for site: {site_name}")
    set_site_data(site_name, site_data)

    # 3. Email customer
    draft_url = f"https://{site_name}.multiscreensite.com/"
    html = f"""
        <p>Hi,</p>
        <p>Your draft website is ready: <a href="{draft_url}">{draft_url}</a></p>
        <p>We'll be in touch with next steps!</p>
    """
    email_addr = record["Please provide an email address that you'd like to use to receive a link to your website draft after completing this form & to receive job applications from your website"]
    app.logger.info(f"✉️  Sending email to {email_addr}")
    send_email(email_addr, os.environ["EMAIL_SUBJECT"], html)

    # 4. Mark processed
    set_processed(row_num)
    app.logger.info(f"✅ Done processing row {row_num} (site: {site_name})")

    return jsonify({"site": site_name, "row": row_num})

if __name__ == "__main__":
    app.run(debug=True)
