# main
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
    # We will use a fixed, recent date range for demonstration.
    base_url = "https://api.tenders.gov.au/ocds/findByDates/contractPublished"
    start_date = "2024-02-08T00:00:00Z"
    end_date = "2025-09-14T23:59:59Z"
    url = f"{base_url}/{start_date}/{end_date}"

    # Define your company's search filters.
    # Update these values to match the opportunities you're looking for.
    my_company_filters = {
        'unspsc_codes': ['4310', '4323', '8010', '8011', '8110', '8111', '8113', '8115', '8116', '8117'], # UNSPSC for Computer services
        'keywords':
            ['IT', 'ai',
                'artificial intelligence',
                'machine learning',
                'ml',
                'deep learning',
                'predictive maintenance',
                'computer vision',
                'object detection',
                'edge computing',
                'real-time analytics',
                'realtime analytics',
                'digital twin',
                'automation',
                'computer vision platform',
                'video analytics',
                'live video',
                'streaming',
                'stream',
                'real-time',
                'realtime',
                'video',
                'image',
                'photo',
                'cctv',
                'camera',
                'gis',
                'geographic information systems',
                'remote sensing',
                'lidar',
                'orthomosaic',
                'spatial analytics',
                'hazard mapping',
                'evacuation modelling',
                'early warning systems',
                'biodiversity monitoring',
                'infrastructure',
                'roads',
                'streets',
                'corridors',
                'smart cities',
                'utilities',
                'powerline',
                'stormwater',
                'parking',
                'asset management',
                'asset lifecycle',
                'condition assessment',
                'inspection',
                'resilience',
                'retrofit',
                'decarbonisation',
                'climate adaptation',
                'renewable energy',
                'renewables',
                'solar',
                'wind',
                'wind turbine',
                'turbine',
                'operational efficiency',
                'manufacturing',
                'supply chain visibility'
                'flow monitoring',
                'counting',
                'disaster',
                'fire',
                'flood',
                'emergency response',
                'emergency',
                'public safety',
                'vessel monitoring',
                'remote operations',
                'drone',
                'drones',
                'uav',
                'unmanned aerial systems',
                'uav inspection',
                'drone video analytics',
                'uav program manager',
                'remote site inspection',
                'sovereign industrial priorities',
                'skilling stream',
                'exports stream',
                'security stream'], # Keywords to look for in the description
        'min_amount': 200000.00 # Minimum value in AUD
    }

    try:
        print(f"Fetching data from the AusTender API...")
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX

        # Parse the JSON response into a Python object.
        api_data = response.json()
        
        # Access the list of opportunities from the 'releases' key, if it exists.
        opportunities = api_data.get('releases', [])
        
        if not opportunities:
            print("No opportunities found in the API response for the given date range.")
            return

        # Use the filter_opportunities function to find matches.
        print(f"Filtering {len(opportunities)} opportunities...")
        filtered_opportunities = filter_opportunities(opportunities, my_company_filters)

        # Print the results.
        if filtered_opportunities:
            print(f"\nFound {len(filtered_opportunities)} opportunities matching your criteria:")
            for opp in filtered_opportunities:
                # Get the tender object and skip if it's not present.
                tender_info = opp.get('tender')
                if not tender_info:
                    continue
                
                # Extract and print relevant details from the filtered opportunity.
                # Use .get() to safely access nested keys, providing a default value if not found.
                tender_title = tender_info.get('title', 'N/A')
                buyer_name = opp.get('buyer', {}).get('name', 'N/A')
                ocid = opp.get('ocid', 'N/A')

                # Extract dates and status from the tender object
                tender_status = tender_info.get('status', 'N/A')
                tender_post_date = tender_info.get('datePublished', 'N/A')
                tender_closing_date = tender_info.get('tenderPeriod', {}).get('endDate', 'N/A')
                
                # We still want the first contract's info
                contract = opp.get('contracts', [{}])[0]
                description = contract.get('description', 'N/A')
                value = contract.get('value', {}).get('amount', 'N/A')
                award_date_str = contract.get('date', 'N/A')

                # Determine the user-friendly status
                if tender_status == 'active':
                    display_status = "Open"
                elif tender_status == 'complete':
                    display_status = "Awarded"
                else:
                    display_status = "N/A"
                print(f"\n- Tender Title: {tender_title}")
                print(f"  Procuring Agency: {buyer_name}")
                print(f"  OCID: {ocid}")
                print(f"  Status: {display_status}")
                print(f"  Tender Post Date: {tender_post_date}")
                print(f"  Tender Closing Date: {tender_closing_date}")
                print(f"  Description: {description}")
                print(f"  Value: ${value} AUD")
                print(f"  Award Date: {award_date_str}")

                # Print the UNSPSC codes and their categories if they exist
                matched_codes = opp.get("matched_unspsc", [])
                if matched_codes:
                    print("     Matched UNSPSC codes:")
                    for code in matched_codes:
                        prefix = code[:4]
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