'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const BBCMicrobit = require('bbc-microbit');
const restService = express();

const pin = 0; // ms
var doorstatus = 0;


restService.use(bodyParser.urlencoded({
    extended: true
}));

restService.use(bodyParser.json());

restService.post('/echo', function(req, res) {
    var speech = req.body.result && req.body.result.parameters && req.body.result.parameters.TempText ? req.body.result.parameters.TempText : "Something not right"

    if (doorstatus == 1)
    	speech = 'Door is closed';
    else 
    	speech = 'Door is opened';

    console.log(speech);

    return res.json({
        speech: speech,
        displayText: speech,
        source: 'webhook-microbit'
    });
});



restService.listen((process.env.PORT || 8000), function() {
    console.log("Server up and listening");

    console.log('Scanning for microbit');
	BBCMicrobit.discover(function(microbit) {
		console.log('\tdiscovered microbit: id = %s, address = %s', microbit.id, microbit.address);

	  	microbit.on('disconnect', function() {
	    	console.log('\tmicrobit disconnected!');
	    	process.exit(0);
	  	});

	  	microbit.on('pinDataChange', function(pin, value) {
			console.log('\ton -> pin data change: pin = %d, value = %d', pin, value);
			if (value == 3) 
				doorstatus = 1;
			else 
				doorstatus = 0;
		});

	  	console.log('connecting to microbit');
	  	microbit.connectAndSetUp(function() {
		    console.log('\tconnected to microbit');

		    console.log('setting pin %d as input', pin);
		    microbit.pinInput(pin, function() {
		    	console.log('\tpin set as input');

		      	console.log('setting pin %d as analog', pin);
		      	microbit.pinAnalog(pin, function() {
		        	console.log('\tpin set as analog');

		        	console.log('subscribing to pin data');
		        
		        	microbit.subscribePinData(function() {
		          		console.log('\tsubscribed to pin data');
		        	});
		      	});
		    });
		});

	});
});
