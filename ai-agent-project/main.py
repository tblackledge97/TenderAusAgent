import requests
import xml.etree.ElementTree as ET
from email_sender import build_email_body, send_email

keywords = {
    "IT": 4,
    "ai": 5,
    "artificial intelligence": 5,
    "machine learning": 4,
    "ml": 4,
    "deep learning": 3,
    "predictive maintenance": 5,
    "computer vision": 5,
    "object detection": 4,
    "edge computing": 4,
    "real-time analytics": 5,
    "realtime analytics": 5,
    "digital twin": 4,
    "automation": 4,
    "computer vision platform": 5,
    "video analytics": 5,
    "live video": 5,
    "streaming": 5,
    "stream": 5,
    "real-time": 5,
    "realtime": 5,
    "video": 4,
    "image": 4,
    "photo": 3,
    "cctv": 4,
    "camera": 3,
    "gis": 4,
    "geographic information systems": 4,
    "remote sensing": 4,
    "lidar": 5,
    "orthomosaic": 3,
    "spatial analytics": 4,
    "hazard mapping": 3,
    "evacuation modelling": 2,
    "early warning systems": 3,
    "biodiversity monitoring": 2,
    "infrastructure": 5,
    "roads": 4,
    "streets": 3,
    "corridors": 5,
    "smart cities": 4,
    "utilities": 5,
    "powerline": 5,
    "stormwater": 3,
    "parking": 3,
    "asset management": 5,
    "asset lifecycle": 4,
    "condition assessment": 5,
    "inspection": 5,
    "resilience": 3,
    "retrofit": 2,
    "decarbonisation": 2,
    "climate adaptation": 3,
    "renewable energy": 5,
    "renewables": 5,
    "solar": 5,
    "wind": 5,
    "wind turbine": 5,
    "turbine": 4,
    "operational efficiency": 4,
    "manufacturing": 3,
    "supply chain visibility": 3,
    "flow monitoring": 3,
    "counting": 3,
    "disaster": 4,
    "fire": 4,
    "flood": 4,
    "emergency response": 4,
    "emergency": 4,
    "public safety": 4,
    "vessel monitoring": 3,
    "remote operations": 4,
    "drone": 5,
    "drones": 5,
    "uav": 5,
    "unmanned aerial systems": 5,
    "uav inspection": 5,
    "drone video analytics": 5,
    "uav program manager": 4,
    "remote site inspection": 5,
    "sovereign industrial priorities": 3,
    "skilling stream": 3,
    "exports stream": 3,
    "security stream": 3
}

# The RSS feed URL
# rss_urls = ["https://www.tenders.gov.au/public_data/rss/rss.xml",
#             "https://www.vendorpanel.com.au/PublicTendersRssV2.aspx?mode=all"]

# A dictionary to hold the request headers
#headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
#    '537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#}

found_matches = {}
# load the memory file
log_file = "processed_links.txt"

try:
    processed_links = set()
    try:
        with open(log_file, "r") as file:
            processed_links = {line.strip() for line in file}
    except FileNotFoundError:
        print(f"Log file, '{log_file}' not found. Starting with no history.")
        pass

    for rss_url in rss_urls:
        print(f"Checking for tenders at: {rss_url}")
        try:
            response = requests.get(rss_url, headers=headers)
            response.raise_for_status()

            root = ET.fromstring(response.text)
            items = root.findall('.//item')

            if not items:
                print("No tender items in RSS feed.")
            else:
                for item in items:
                    link = item.find('link').text
                    if link in processed_links:
                        continue

                    title = item.find('title').text
                    description = item.find('description').text
                    content_to_search = (title + " " + description).lower()

                    matched_keywords = []
                    total_score = 0

                    for keyword, weight in keywords.items():
                        if keyword.lower() in content_to_search:
                            matched_keywords.append(f"{keyword} (x{weight})")
                            total_score += weight

                    if matched_keywords:
                        found_matches[link] = {
                            'title': title,
                            'link': link,
                            'description': description,
                            'matched_keywords': matched_keywords,
                            'total_score': total_score
                        }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching RSS feed from {rss_url}: {e}")

    # This is the correct placement for the sorting and printing logic.
    # It executes only once, after the loop finishes.
    sorted_matches = sorted(found_matches.values(),
                            key=lambda x: x['total_score'],
                            reverse=True)

    new_links_found = [match['link'] for match in sorted_matches]

    if new_links_found:
        print(f"Adding {len(new_links_found)} new links to the log file.")
        try:
            with open(log_file, "a") as file:
                for link in new_links_found:
                    file.write(link + "\n")
        except Exception as e:
            print(f"Error writing file: {e}")

    if sorted_matches:
        # build the email
        email_subject = f"New Tender Opportunities ({len(sorted_matches)})"
        email_body = build_email_body(sorted_matches)

        # send the email
        send_email(email_subject, email_body, "t.blackledge97@gmail.com")

        print(f"Found {len(sorted_matches)} opportunities:")
        for match in sorted_matches:
            print("=" * 20)
            print(f"Title: {match['title']}")
            print(f"Link: {match['link']}")
            print(f"Description: {match['description']}")
            print(f"Matched Keywords: {', '.join(match['matched_keywords'])}")
            print(f"Total weighted score: {match['total_score']}")
    else:
        print("No matches found.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching the RSS feed: {e}")
except ET.ParseError as e:
    print(f"Error parsing XML: {e}")
