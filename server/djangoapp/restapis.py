import requests
import json
from .models import CarDealer, DealerReview, CarModel, CarMake
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
    
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, params=kwargs, json=json_payload)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs): 
# dealer_doc = dealer
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        print(json_result)
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer.get("address", ""),
                city=dealer.get("city", ""),
                id=dealer.get("id", ""),
                lat=dealer.get("lat", ""),
                long=dealer.get("long", ""),
                st=dealer.get("st", ""),
                zip=dealer.get("zip", ""),
                full_name=dealer.get("full_name", ""),
                short_name=dealer.get("short_name", ""),
            )
            results.append(dealer_obj)
        return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealer_id):
    json_result = get_request(url, id=dealer_id)

    if json_result:
        dealers = json_result
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(
            address=dealer_doc["address"],
            city=dealer_doc["city"],
            id=dealer_doc["id"],
            lat=dealer_doc["lat"],
            long=dealer_doc["long"],
            full_name=dealer_doc["full_name"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"],
            zip=dealer_doc["zip"]
        )
        return results[0]
         # Return None or handle the case when json_result is empty
    return None
        

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, id=dealer_id)
    print(json_result) 

    if isinstance(json_result, list):
        for review in json_result:
            if review['purchase']:
                review_obj = DealerReview(
                    dealership=review['dealership'], 
                    purchase=review['purchase'], 
                    purchase_date=review['purchase_date'], 
                    name=review['name'], 
                    review=review['review'], 
                    car_make=review['car_make'], 
                    car_model=review['car_model'], 
                    car_year=review['car_year'], 
                    id=review['id'], 
                    sentiment='sentiment'
                )
            else:
                review_obj = DealerReview(
                    dealership=review['dealership'], 
                    purchase=review['purchase'], 
                    purchase_date=None, 
                    name=review['name'], 
                    review=review['review'], 
                    car_make=review['car_make'], 
                    car_model=review['car_model'], 
                    car_year=review['car_year'], 
                    id=review['id'], 
                    sentiment='sentiment'
                )
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            print("Sentiments: ", review_obj.sentiment)
            print("Results: ", review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c989295b-406a-43e5-992f-0742bcd9d389"
    api_key = "W8RN3cMVOYg6ugb9VgY6ZbmaQnEcGtQowEC2VXEWNrVP"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    try:
        response = natural_language_understanding.analyze( text=dealerreview,features=Features(sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
        label=json.dumps(response, indent=2)
        label = response['sentiment']['document']['label']

        return(label)

    except:
        print("Can't analyze the sentiment")
        return 'none'


