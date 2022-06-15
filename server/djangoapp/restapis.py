from sys import implementation
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url}")
    #Attempt to get api_key param
    #api_key = kwargs.get("api_key")
    try:
        # Call get from requests lib with URL and params
        # if api_key:
        #     #GET with auth
        #     params = dict()
        #     params["text"] = kwargs["text"]
        #     params["version"] = kwargs["version"]
        #     params["features"] = kwargs["features"]
        #     params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        #     response = requests.get(url, headers={"Content-Type": "application/json"},
        #                             params=params, auth=HTTPBasicAuth('apikey', api_key))
        # else:
            #GET w/o auth
            response = requests.get(url, headers={"Content-Type": "application/json"},
                                    params=kwargs)
    except:
        #If any network error occurs
        print("Network exception occured")
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, json=json_payload, params=kwargs)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    #Call get_request with the url param
    json_result = get_request(url)
    if json_result:
        #Get the result list in JSON as dealers
        dealers = json_result["result"]
        for dealer in dealers:
            #Create each CarDealer obj with the json results
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"],
                                   full_name=dealer["full_name"], id=dealer["id"],
                                   lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], st=dealer["st"],
                                   zip=dealer["zip"])
            results.append(dealer_obj)
    
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    #call get request with url and dealer_id arg
    json_result=get_request(url=url, dealerId=dealer_id)
    if json_result:
        #Get the result list in JSON as reviews
        reviews = json_result["body"]["data"]["docs"]
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"],
                                    purchase=review["purchase"], review=review["review"],
                                    purchase_date=review["purchase_date"],
                                    car_make=review["car_make"], car_model=review["car_model"],
                                    car_year=review["car_year"], sentiment=analyze_review_sentiments(review["review"]),
                                    id=review["id"])
            results.append(review_obj)

    return results

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    #Call get_request with url
    json_result = get_request(url=url)
    if json_result:
        #Get the result list in JSON as dealers
        dealers = json_result["result"]
        for dealer in dealers:
            #Check if the id matches the requested dealerId
            if dealer["id"] == dealerId:
                #Create each CarDealer obj with the json results
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"],
                                    full_name=dealer["full_name"], id=dealer["id"],
                                    lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"], st=dealer["st"],
                                    zip=dealer["zip"])
            results.append(dealer_obj)
    return results

#Create get dealer by state function
def get_dealer_by_st_from_cf(url, st):
    results = []
    #Call get_request with formatted Url
    json_result = get_request(url=url, state=st)
    if json_result:
        #get the json result list as dealers
        dealers = json_result["result"]
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"],
                                    full_name=dealer["full_name"], id=dealer["id"],
                                    lat=dealer["lat"], long=dealer["long"],
                                    short_name=dealer["short_name"], st=dealer["st"],
                                    zip=dealer["zip"])
            results.append(dealer_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    api_key = "_0H8Dw-Z29hjwxeGeD6Vni8wmPUiGJb3U_UhLg0TNRR4"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f6b70ecb-4d10-4ec9-8288-3a0f270f512b"
    # -------
    # Please forgive this ugly workaround.
    # It was made to compensate for the poor implementation of the watson api,
    # which doesn't account for text that is too short to evaluate.
    # It should now still evaluate both short and long strings correctly.
    if len(dealer_review) >= 30:
        text = dealer_review
    else:
        text = dealer_review+" neutral text. neutral text. neutral text."
    # -------
    version = "2021-08-01"
    try:
        authenticator = IAMAuthenticator(api_key)
        NLU = NaturalLanguageUnderstandingV1(version=version, authenticator=authenticator)
        NLU.set_service_url(url)
        features = Features(sentiment=SentimentOptions(targets=[text]))
        response = NLU.analyze(text=text, features=features).get_result()
        label = json.dumps(response, indent=2)
        label = response['sentiment']['document']['label']
        return (label)
    except:
        print("An error occured with the NLU usage attempt")
        return "No analysis made"

    

