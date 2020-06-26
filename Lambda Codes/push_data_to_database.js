console.log('Loading event');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
var tableName = "voiceform_registration";
AWS.config.update({region: "us-east-1"});
var translate = new AWS.Translate();
var lambda = new AWS.Lambda();

// Close dialog with the customer, reporting fulfillmentState of Failed or Fulfilled
function close(sessionAttributes, fulfillmentState, message) {
    return {
        sessionAttributes,
        dialogAction: {
            type: 'Close',
            fulfillmentState,
            message,
        },
    };
}

var getHindi = async (msg) => {
    var params = {
        Text: msg,
        SourceLanguageCode: "auto",
        TargetLanguageCode: "hi"
    };
    
    

    var tranlatedMsg = await translate.translateText(params, (err, data) => {
        return data;
    }).promise()

    return tranlatedMsg.TranslatedText
}

//var translatedMsg = await getHindi("mohankrishna")


function callVal(message){
    exports.handler = async (event) => {
    // TODO implement
    
    
    var translatedMsg = await getHindi(message)
    console.log(translatedMsg);
    return translatedMsg;
    };

}


  


let userInfo = {};

function storeRegistration(intent, callback) {

    
    let translateinfo={};

    // store every slot we received as part of registration
    Object.keys(intent.currentIntent.slots).forEach((item) => {
        console.log(item)
        userInfo[item] = {"S": intent.currentIntent.slots[item]};
        let trans
        if(Number.isInteger(intent.currentIntent.slots[item]))
        {
            trans=intent.currentIntent.slots[item].toString()

        }
        else
        {
            trans=intent.currentIntent.slots[item]
        }
        
        let secondTran=callVal(trans)
        translateinfo[item]= {"S": secondTran};
        //console.log(translateinfo[item])
        
        
    });

    // store a registration date
    userInfo.registration_date = {"S": new Date().getTime().toString() };
    userInfo.registration_userid = {"S": intent.userId};
    
    
    
    translateinfo.registration_date = {"S": new Date().getTime().toString() };
    translateinfo.registration_userid = {"S": intent.userId};
    
    
    dynamodb.putItem({
        "TableName": tableName,
        "Item" : userInfo,
    }, function(err, data) {
        if (err) {
            console.log('Failure storing user info');
            console.log(err);
            callback(close(intent.sessionAttributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': "I am sorry, but something went wrong saving your Registration Info. Please try again."}));
        } else {
            console.log("Successfully Stored UserInfo");
            callback(close(intent.sessionAttributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': "Thank you for registering for our service."}));
        }
    });
    
    
/*    dynamodb.putItem({
        "TableName": tableName,
        "Item" : translateinfo
    }, function(err, data) {
        if (err) {
            console.log('Failure storing user info');
            console.log(err);
            callback(close(intent.sessionAttributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': "I am sorry, but something went wrong saving your Registration Info. Please try again."}));
        } else {
            console.log("Successfully Stored UserInfo");
            callback(close(intent.sessionAttributes, 'Fulfilled',
            {'contentType': 'PlainText', 'content': "Thank you for registering for our service."}));
        }
    });*/
}

// --------------- Main handler -----------------------
 
// Route the incoming request based on intent.
// The JSON body of the request is provided in the event slot.
exports.handler = (event, context, callback) => {
    console.log(event);
    try {
        storeRegistration(event,
            (response) => {
                callback(null, response);
            });
    } catch (err) {
        callback(err);
    }
    
};

