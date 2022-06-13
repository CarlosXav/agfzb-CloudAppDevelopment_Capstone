/**
 * Get reviews of a given dealership by id
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    //if state is specified
    if(params.dealerId!=null){
        let reListPromise = getReviews(cloudant, {dealership:params.dealerId});
        return reListPromise;
    } else {
        return {};
    }


}


 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records.
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
function getReviews(cloudant, selector) {

    return new Promise((resolve, reject) => {
        cloudant.postFind({db:'reviews',selector:selector})
                .then((result)=>{
                    resolve({result:result.result.docs});
                })
                .catch(err => {
                    console.log(err);
                    reject({ err: err });
                });
    })


}
