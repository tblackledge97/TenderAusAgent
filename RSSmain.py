import requests
import json
import datetime
from filter_ops import filter_opportunities
from unspscCodes import unspsc_mapping

def main():
    """
    Fetches data from the AusTender OCDS API, filters it, and prints the results.
    """
    # Define the API endpoint URL for a specific date range.
    # The 'releases' endpoint is generally better for a broader search.
    # Or, to be precise, 'tenderLastModified' might be a better endpoint.
    #base_url = "https://api.tenders.gov.au/ocds/findByDates/contractLastModified"
    start_date = "2024-02-08T00:00:00Z"
    end_date = "2025-09-14T23:59:59Z"
    url = f"{base_url}/{start_date}/{end_date}"

    # Define your company's search filters.
    # Update these values to match the opportunities you're looking for.
    my_company_filters = {
        'unspsc_codes': ['4310', '4323', '8010', '8011', '8110', '8111', '8113', '8115', '8116', '8117'],
        'keywords':
            ['IT', 'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'predictive maintenance', 'computer vision', 'object detection', 'edge computing', 'real-time analytics', 'realtime analytics', 'digital twin', 'automation', 'computer vision platform', 'video analytics', 'live video', 'streaming', 'stream', 'real-time', 'realtime', 'video', 'image', 'photo', 'cctv', 'camera', 'gis', 'geographic information systems', 'remote sensing', 'lidar', 'orthomosaic', 'spatial analytics', 'hazard mapping', 'evacuation modelling', 'early warning systems', 'biodiversity monitoring', 'infrastructure', 'roads', 'streets', 'corridors', 'smart cities', 'utilities', 'powerline', 'stormwater', 'parking', 'asset management', 'asset lifecycle', 'condition assessment', 'inspection', 'resilience', 'retrofit', 'decarbonisation', 'climate adaptation', 'renewable energy', 'renewables', 'solar', 'wind', 'wind turbine', 'turbine', 'operational efficiency', 'manufacturing', 'supply chain visibility'
                'flow monitoring', 'counting', 'disaster', 'fire', 'flood', 'emergency response', 'emergency', 'public safety', 'vessel monitoring', 'remote operations', 'drone', 'drones', 'uav', 'unmanned aerial systems', 'uav inspection', 'drone video analytics', 'uav program manager', 'remote site inspection', 'sovereign industrial priorities', 'skilling stream', 'exports stream', 'security stream'], 
        'min_amount': 200000.00
    }

    try:
        print(f"Fetching data from the AusTender API...")
        response = requests.get(url)
        response.raise_for_status()

        api_data = response.json()
        
        opportunities = api_data.get('releases', [])
        
        if not opportunities:
            print("No opportunities found in the API response for the given date range.")
            return

        print(f"Filtering {len(opportunities)} opportunities...")
        filtered_opportunities = filter_opportunities(opportunities, my_company_filters)

        if filtered_opportunities:
            print(f"\nFound {len(filtered_opportunities)} opportunities matching your criteria:")
            for opp in filtered_opportunities:
                tender_info = opp.get('tender')
                if not tender_info:
                    continue
                
                # Corrected data extraction based on the schema
                tender_title = tender_info.get('title', 'N/A')
                buyer_name = opp.get('buyer', {}).get('name', 'N/A')
                tender_status = tender_info.get('status', 'N/A')
                
                # Correctly get the description from the tender object
                tender_description = tender_info.get('description', 'N/A')

                # Correctly get the ID to build the URL
                atm_id = opp.get('id', 'N/A')
                tender_url = f"https://www.tenders.gov.au/Atm/Show/{atm_id}" if atm_id != 'N/A' else 'N/A'
               
                print(f"\n- Tender Title: {tender_title}")
                print(f"  Procuring Agency: {buyer_name}")
                print(f"  Status: {tender_status}")
                print(f"  Description: {tender_description}")
                print(f"  Tender URL: {tender_url}")
                
                # Extract the contract value and award date from the awards section
                award_info = opp.get('awards', [{}])[0]
                award_value = award_info.get('value', {}).get('amount', 'N/A')
                award_date_str = award_info.get('date', 'N/A')
                print(f"  Awarded Value: ${award_value} AUD")
                print(f"  Award Date: {award_date_str}")
                
                # Print the UNSPSC codes and their categories if they exist
                matched_codes = opp.get("matched_unspsc", [])
                if matched_codes:
                    print("     Matched UNSPSC codes:")
                    for code in matched_codes:
                        prefix = str(code)[:4] # Ensure it's treated as a string for slicing
                        category = unspsc_mapping.get(prefix, "Unknown category")
                        print(f"        - {code} => {category}")
                print("-" * 20)
        else:
            print("\nNo opportunities found that match your criteria.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API response: {e}")

if __name__ == "__main__":
    main()