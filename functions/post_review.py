#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
# '''
#     Get the reviews by a given dealerId
# '''
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator(dict['IAM_API_KEY'])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict['COUCH_URL'])
    #my_database = service["reviews"]
    #verify that all entries exist
    # try:
    #     if (
    #         dict["review"]['id'] != None and
    #         dict["review"]['name'] != None and
    #         dict["review"]['dealership'] != None and
    #         dict["review"]['review'] != None and
    #         dict["review"]['purchase'] != None and
    #         dict["review"]['another'] != None and
    #         dict["review"]['purchase_date'] != None and
    #         dict["review"]['car_make'] != None and
    #         dict["review"]['car_model'] != None and
    #         dict["review"]['car_year'] != None
    #     ):
    #         my_document = my_database.create_document({"review":dict["review"]})
    #     elif:
    #         return {
    #             'statusCode': 500,
    #             'message': 'Something went wrong on the server'
    #         } 
    # except:
    #     return {
    #         'statusCode': 500,
    #         'message': 'Something went wrong on the server'
    #     }
    #my_document = my_database.create_document({"review":dict["review"]})
    try:
        response = service.post_document(db='reviews', document=dict["review"]).get_result()
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
            'statusCode': 500,
            'message': 'Something went wrong on the server'
        } 
