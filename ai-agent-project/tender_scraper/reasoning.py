import json

def load_tenders_data(file_path):
    """
    loads sample tenders, fake data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    tenders = load_tenders_data('tenders_data.json')
    print("successfully loaded", len(tenders), "tenders")
    print("First tender:", tenders[0]['title'])