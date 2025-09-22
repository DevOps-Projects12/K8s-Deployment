var express = require('express');
var app = express();

app.get('/', function (req, res) {
    res.send('{ "response": "Welcome to the world of programming" }');
});

app.get('/will', function (req, res) {
    res.send('{ "response": "You are at right path" }');
});
app.get('/ready', function (req, res) {
    res.send('{ "response": " Great!, It works!" }');
});
app.listen(process.env.PORT || 3000);
module.exports = app;
