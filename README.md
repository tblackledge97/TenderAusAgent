# TenderAusAgent
Beginnings of an agent to pull data from the AusTenders API and filter it for opportunities that suit Unleash.

# main.py
Primary entry point for procurement data. Define the search criteria and make the API request. Displays the data in a readable format.

# filter_ops.py
Filters the procurement data. It takes two arguments, opportunities and filters. Opportunities is a list of ditionaries where each dictionary represents a single procurement opportunity returned by the API. Filters is the dictionary of criteria defined in the main script. Work so that if any of the my_company_filters are satisfied, the tedner is returned.

# unspscCodes.py
A list of the codes that might be useful to unleash live (Only the first 4 digits, the 'segment' and 'family').
