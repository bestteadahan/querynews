var http = require('http');
var express = require('express');
var bodyParser = require('body-parser');

var app = express();

app.locals.pretty = true;
app.set('ip','localhost');
app.set('port', process.env.PORT || 8000);
app.set('views', __dirname + '/app/server/views');
app.set('view engine', 'jade');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(__dirname + '/app/public'));

require('./app/server/routes')(app);

http.createServer(app).listen(app.get('port'),app.get('ip'), function(){
	console.log('Express server listening on port ' + app.get('port'));
});
