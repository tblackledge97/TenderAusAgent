# filter opportunities

import requests
import json
import datetime
from unspscCodes import unspsc_mapping


# This script fetches procurement data from the AusTender OCDS API,
# filters it based on specific criteria, and prints matching opportunities.
# You may need to install the 'requests' library: pip install requests


def filter_opportunities(opportunities, filters):
    """
    Filters a list of procurement opportunities based on a dictionary of filters.
    
    The filter logic is now an "OR" condition. An opportunity will be
    included in the results if it matches any of the following:
    - UNSPSC codes
    - Keywords in the contract description
    - Minimum contract value

    Args:
        opportunities (list): A list of dictionaries, where each dictionary
                             represents a single procurement opportunity.
        filters (dict): A dictionary containing filter criteria.
                        Possible keys:
                        - 'unspsc_codes': list of UNSPSC codes (e.g., ['81110000']).
                        - 'keywords': list of keywords to search in contract descriptions.
                        - 'min_amount': minimum contract value.

    Returns:
        list: A new list containing only the opportunities that match at least one filter.
    """
    
    # Check if the input is valid JSON and contains the 'contracts' key.
    if not isinstance(opportunities, list):
        print("Error: The input data is not a list of opportunities.")
        return []

    matched_opportunities = []

    for opportunity in opportunities:
        # Assume an opportunity is NOT a match until a filter passes.
        unspsc_match = False
        keyword_match = False
        amount_match = False
        
        # This list will store any UNSPSC codes that match
        matched_codes = []

        # Check for UNSPSC code match.
        if 'unspsc_codes' in filters and filters['unspsc_codes']:
            contract_items = opportunity.get('contracts', [])
            for contract in contract_items:
                for item in contract.get('items', []):
                    if item.get('classification', {}).get('scheme') == 'UNSPSC':
                        unspsc_id = item['classification']['id']
                        prefix = unspsc_id[:4]
                        if prefix in filters['unspsc_codes']:
                            unspsc_match = True
                            matched_codes.append(unspsc_id)

        # Check for keyword match in contract description.
        if 'keywords' in filters and filters['keywords']:
            contract_descriptions = [c.get('description', '').lower() for c in opportunity.get('contracts', [])]
            keyword_match = any(any(keyword.lower() in desc for desc in contract_descriptions) for keyword in filters['keywords'])

        # Check for minimum amount.
        if 'min_amount' in filters:
            contract_values = [c.get('value', {}).get('amount') for c in opportunity.get('contracts', [])]
            amount_match = any(float(v) >= filters['min_amount'] for v in contract_values if v is not None)
                
        # Now, check if ANY of the conditions are true using "OR"
        if unspsc_match or keyword_match or amount_match:
            # If there was a UNSPSC match, add the codes to the opportunity for printing
            if unspsc_match:
                opportunity["matched_unspsc"] = matched_codes
            matched_opportunities.append(opportunity)

    return matched_opportunities