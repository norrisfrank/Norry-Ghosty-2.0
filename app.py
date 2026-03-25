import os
import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# SOCIAL MEDIA URLS FOR USERNAME OSINT
social_media = [
    {"url": "https://www.facebook.com/{}", "name": "Facebook"},
    {"url": "https://www.twitter.com/{}", "name": "Twitter"},
    {"url": "https://www.instagram.com/{}", "name": "Instagram"},
    {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
    {"url": "https://www.github.com/{}", "name": "GitHub"},
    {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
    {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
    {"url": "https://www.youtube.com/{}", "name": "Youtube"},
    {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
    {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
    {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
    {"url": "https://www.behance.net/{}", "name": "Behance"},
    {"url": "https://www.medium.com/@{}", "name": "Medium"},
    {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
    {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
    {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
    {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
    {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
    {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
    {"url": "https://www.ello.co/{}", "name": "Ello"},
    {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
    {"url": "https://www.telegram.me/{}", "name": "Telegram"},
    {"url": "https://www.weheartit.com/{}", "name": "We Heart It"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ip", methods=["POST"])
def track_ip():
    data = request.json
    ip = data.get("ip")
    if not ip:
        return jsonify({"error": "No IP provided"}), 400
    
    try:
        req_api = requests.get(f"http://ipwho.is/{ip}")
        ip_data = req_api.json()
        return jsonify(ip_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/myip", methods=["POST"])
def my_ip():
    try:
        response = requests.get('https://api.ipify.org/?format=json')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/phone", methods=["POST"])
def track_phone():
    data = request.json
    phone = data.get("phone")
    if not phone:
        return jsonify({"error": "No phone number provided"}), 400
    
    try:
        default_region = "ID"
        parsed_number = phonenumbers.parse(phone, default_region)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        jenis_provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "id")
        is_valid_number = phonenumbers.is_valid_number(parsed_number)
        is_possible_number = phonenumbers.is_possible_number(parsed_number)
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        number_type_id = phonenumbers.number_type(parsed_number)
        
        number_type = "Unknown"
        if number_type_id == phonenumbers.PhoneNumberType.MOBILE:
            number_type = "Mobile"
        elif number_type_id == phonenumbers.PhoneNumberType.FIXED_LINE:
            number_type = "Fixed-line"
            
        timezone1 = timezone.time_zones_for_number(parsed_number)
        timezoneF = ', '.join(timezone1)
        
        return jsonify({
            "Location": location,
            "Region Code": region_code,
            "Timezone": timezoneF,
            "Operator": jenis_provider,
            "Valid number": is_valid_number,
            "Possible number": is_possible_number,
            "International format": formatted_number,
            "Original number": parsed_number.national_number,
            "Type": number_type
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/username", methods=["POST"])
def track_username():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "No username provided"}), 400
    
    results = {}
    try:
        for site in social_media:
            url = site['url'].format(username)
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    results[site['name']] = url
                else:
                    results[site['name']] = "Not Found"
            except requests.RequestException:
                results[site['name']] = "Not Found"
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
