import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from scipy.sparse import hstack, csr_matrix
import numpy as np

RELEVANCE_KEYWORDS = [
    "software development",
    "web application",
    "IT services",
    "cyber security",
    "cloud computing"
]

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
    "security stream": 3,
    # my added words for testing
    "software development": 4,
    "web application": 4,
    "IT services": 4,
    "cyber security": 5,
    "cloud computing": 4,
    "data analysis": 5,
    "software": 4,
    "data": 3
}


def load_tenders_data(file_path):
    """
    loads sample tenders, fake data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def calculate_keyword_scores(tender):
    """
    Calculates a score based on the predefined, weighted keyword dictionary.
    """
    score = 0
    # combine the text and dictionary
    text = (tender.get('title', '') + " " + tender.get('description', '')).lower()

    for keyword, weight in keywords.items():
        if keyword in text:
            score += weight

    return score


def train_relevance_model(tenders):
    """
    Trains an ML model to predict tender relevance.
    """
    # prep the data seperately for:
    # desciption
    # category
    # agency
    descriptions = [tender.get('description', '') for tender in tenders]
    categories_agencies = [tender.get('category', '') + " " +
                           tender.get('agency', '') for tender in tenders]

    labels = np.array([tender['is_relevant'] for tender in tenders])

    # keywords scores
    keyword_scores = [calculate_keyword_scores(tender) for tender in tenders]
    X_keyword = csr_matrix(np.array(keyword_scores)).T

    # vectorise the data
    desc_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_desc = desc_vectorizer.fit_transform(descriptions)

    other_vectorizer = TfidfVectorizer()
    X_other = other_vectorizer.fit_transform(categories_agencies)

    # combine the data
    X_combined = hstack([X_desc, X_other, X_keyword])

    # train the classification model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_combined, labels)

    # Save the trained model and vectorizers to files
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('desc_vectorizer.pkl', 'wb') as f:
        pickle.dump(desc_vectorizer, f)
    with open('other_vectorizer.pkl', 'wb') as f:
        pickle.dump(other_vectorizer, f)

    return model, desc_vectorizer, other_vectorizer


def score_tender_relevance(tender, keywords):
    """
    Scores a tender's relevant based on list of keywords.
    Returns True is a match is found, otherwise false.
    """
    tender_text = (tender['title'] + " " + tender['description']).lower()

    for keyword in keywords:
        if keyword in tender_text:
            return True
    return False


def predict_relevance(new_tenders, model, desc_vectorizer, other_vectorizer):
    """
    Uses the trained model to predict relevance.
    """
    # Vectoriser has already been fitted so to our vocab
    # so use .transform() not .fit_transform()
    new_descriptions = [tender.get('description', '') for tender in new_tenders]
    new_categories_agencies = [tender.get('category', '') + " " + tender.get('agency', '') for tender in new_tenders]

    new_keyword_scores = [calculate_keyword_scores(tender) for tender in new_tenders]
    new_X_keyword = csr_matrix(np.array(new_keyword_scores)).T

    new_X_desc = desc_vectorizer.transform(new_descriptions)
    new_X_other = other_vectorizer.transform(new_categories_agencies)

    # combine the data
    new_X_combined = hstack([new_X_desc, new_X_other, new_X_keyword])

    predictions = model.predict(new_X_combined)

    return predictions


if __name__ == '__main__':
    tenders = load_tenders_data('tenders_data.json')

    # Check their is enough data
    if len(tenders) < 2:
        print("Error, not enough data.")
    else:
        model, desc_vectorizer, other_vectorizer = train_relevance_model(tenders)
        print("Model training complete. Ready for predictions")
        print("-" * 20)

        # new tenders
        NEW_TENDERS = [
            {"title": "IT Support RFP", "description": "Seeking a vendor to provide IT support and network maintenance for a government office.", "category": "IT Support", "agency": "Department of Finance"},
            {"title": "Office Furniture Supply", "description": "Request for proposals for the supply and installation of new office furniture.", "category": "Office Furniture", "agency": "Department of Health"},
            {"title": "Data Analytics Solution", "description": "The Department of Defence requires a new software solution for data analysis and reporting.", "category": "Software Development", "agency": "Department of Defence"},
            {"title": "Landscaping Services", "description": "Call for tenders for landscaping and gardening services at a public park.", "category": "Landscaping", "agency": "Department of the Environment"}
        ]

        # now predict
        predictions = predict_relevance(NEW_TENDERS, model, desc_vectorizer, other_vectorizer)

        print("-- Tender Predictions Report ---")

        for tender_data, prediction in zip(NEW_TENDERS, predictions):

            keyword_score = calculate_keyword_scores(tender_data)

            is_final_match = prediction or (keyword_score >= 5)

            relevance_status = "RELEVANT" if prediction else "Not relevant"

            if is_final_match:
                print("**Match Found!**")
                print(f"  Title: {tender_data.get('title', 'N/A')}")
                print(f"  Description: {tender_data.get('description', 'N/A')[:70]}...")
                print(f"  AI Prediction: {'Relevant' if prediction else 'Not relevant'}")
                print(f"  Keyword score: {keyword_score} (Threshold: 5)")
                print("-" * 50)
