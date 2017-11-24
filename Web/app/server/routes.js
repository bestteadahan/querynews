var PythonShell = require('python-shell');

var translate = require('@google-cloud/translate')({
	projectId: 'firm-harbor-161515',
	keyFilename: 'test-3a097062634b.json'
});
var params = {
	from: 'en',
	to: 'zh-TW'
};

module.exports = function (app) {
	app.get('/', function (req, res) {
		res.redirect('/query');
	});

	app.get('/query', function (req, res) {
		res.render('query');
	});

	// 利用python-shell取MongoDB資料
	app.post('/query', function (req, res) {
		var word = req.body['word'].trim().toLowerCase();
		if (req.body['level'] != null) {
			var level = req.body['level'];
		} else {
			level = 1;
		}
		var options = {
			mode: 'text',
			pythonOptions: ['-u'],
			scriptPath: './',
			encoding: 'utf-8',
			args: [word, level]
		};

		PythonShell.run('findword.py', options, function (err, results) {
			if (err) throw err;
			res.charset = 'value';
			var rec = JSON.parse(results);
			translate.translate(word, params, function (err, translation) {
				if (!err) {
					res.render('query', {
						records: rec,
						notice: word,
						trans: translation
					});
				}
			});
		});
	});
}