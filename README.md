**Automated Agent to Scrape Tender Webistes, APIs and Feeds**

Files:
- reasoning.py: 
  functions:
  loads_tenders_data(): Loads in tender data from a file.
  calculate_keyword_scores(): Calculates a score based on a wieghted keyword dictionary
  train_relevance_model(): Trains a small logistic regression model on tender data in relevance specifially for UL. Also saves the model to prevent having to retain.
  predict_relecance(): USes the trained model to predict the releanve of a ternder
- predictor.py
  functions:
  calculate_keyword_scores(): calculates a score based on weight keyword dictionary
  predict_relevance(): Uses the pretrained model to predict relevance for UL.
  fetch_new_tedners(): Fetches new data currently only from TenderInfo API. Future plan is to recieve information from TenderAus RSS as well.
  format_tender_data(): helper function to translate the API field names into what we are expecting (description/agency/category/URL)
  load_trained_model(): Loads the saved simple logistic regression model and vectorizers for use. This prevents the need to re train the model
  post_to_hubspot(): Post a single matched tender to hubspot. Currently posts to the 'deals' page as no access to specific tenders page.
  post_to_notion(): Post data to Notion, currently just rough implementation, need further workings of notion to improve.
- train_evaluate_models.py
  functions:
  load_tedners_data(): Loads data to train the model
  calculate_keyword_score(): calculates a score based on weight keyword dictionary
  prepare_data(): Prepares data for model input. Including train/val/test split.
  train_and_evaluate(): Trains the logisitic regression model and evaluates against the test data set
  

