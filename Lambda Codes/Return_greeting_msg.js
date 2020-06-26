console.log('Loading event');
var AWS = require('aws-sdk');

// Close dialog with the customer
function close(sessionAttributes, fulfillmentState, message) {
    return {
        sessionAttributes,
        dialogAction: {
            type: 'ElicitIntent',
            message,
        },
    };
}

function buildResponse(intent, callback) {
    console.log("buildResponse");

    let responseText = "Welcome to our  service. Are you interested in registering?";

    callback(close(intent.sessionAttributes, 'Fulfilled', {
        'contentType': 'PlainText',
        'content': responseText
    }));

};

// --------------- Main handler -----------------------
 
// Route the incoming request based on intent.
// The JSON body of the request is provided in the event slot.
exports.handler = (event, context, callback) => {
    try {
        console.log(event);
        console.log(`request received for userId=${event.userId}, intentName=${event.currentIntent.name}`);

        buildResponse(event,
            (response) => {
                callback(null, response);
            });
    } catch (err) {
        callback(err);
    }
};