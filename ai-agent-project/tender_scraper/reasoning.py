import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from scipy.sparse import hstack
import numpy as np

RELEVANCE_KEYWORDS = [
    "software development",
    "web application",
    "IT services",
    "cyber security",
    "cloud computing"
]


def load_tenders_data(file_path):
    """
    loads sample tenders, fake data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


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

    # vectorise the data
    desc_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_desc = desc_vectorizer.fit_transform(descriptions)

    other_vectorizer = TfidfVectorizer()
    X_other = other_vectorizer.fit_transform(categories_agencies)

    # combine the data
    X_combined = hstack([X_desc, X_other])

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


def predict_relevance(tender_descriptions, model, desc_vectorizer, other_vectorizer):
    """
    Uses the trained model to predict relevance.
    """
    # Vectoriser has already been fitted so to our vocab
    # so use .transform() not .fit_transform()
    new_descriptions = [tender.get('descriptions', '') + " " for tender in tenders]
    new_categories_agencies = [tender.get('category', '') + " " + tender.get('agency', '') for tender in tenders]

    new_X_desc = desc_vectorizer.transform(new_descriptions)
    new_X_other = other_vectorizer.transform(new_categories_agencies)

    # combine the data
    new_X_combined = hstack([new_X_desc, new_X_other])

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
            {"description": "Seeking a vendor to provide IT support and network maintenance for a government office.", "category": "IT Support", "agency": "Department of Finance"},
            {"description": "Request for proposals for the supply and installation of new office furniture.", "category": "Office Furniture", "agency": "Department of Health"},
            {"description": "The Department of Defence requires a new software solution for data analysis and reporting.", "category": "Software Development", "agency": "Department of Defence"},
            {"description": "Call for tenders for landscaping and gardening services at a public park.", "category": "Landscaping", "agency": "Department of the Environment"}
        ]

        # now predict
        predictions = predict_relevance(NEW_TENDERS, model, desc_vectorizer, other_vectorizer)

        print("-- Tender Predictions Report ---")
        for tender_data, prediction in zip(NEW_TENDERS, predictions):
            relevance_status = "RELEVANT" if prediction else "Not relevant"
            print(f"Title: '{tender_data['description']}'")
            print(f"Prediction: '{relevance_status}")
            print("-" * 30)
