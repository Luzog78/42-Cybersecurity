const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

const DB_FILE = process.env.DB_FILE || './data/vulnerable.db';
const INIT_SQL = path.join(__dirname, './init.sql');

if (!fs.existsSync(path.dirname(DB_FILE))) {
	fs.mkdirSync(path.dirname(DB_FILE), { recursive: true });
}

const db = new sqlite3.Database(DB_FILE, (err) => {
	if (err) {
		console.error(err);
		return;
	}
	console.log('✅ Connected to SQLite database');

	const initSQL = fs.readFileSync(INIT_SQL, 'utf8');
	db.exec(initSQL);
});

app.get('/', (req, res) => res.render('index'));

app.get('/login', (req, res) => {
	res.render('login', { message: null, user: null });
});

app.post('/login', (req, res) => {
	const { username, password } = req.body;
	const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

	console.log('Executing query:', query);

	db.all(query, (err, rows) => {
		if (err) {
			return res.render('login', { message: err.message, user: null });
		}
		if (rows.length > 0) {
			res.render('login', { message: 'Login successful!', user: rows[0] });
		} else {
			res.render('login', { message: 'Invalid credentials', user: null });
		}
	});
});

app.get('/search', (req, res) => {
	res.render('search', { products: null, query: '', error: null });
});

app.post('/search', (req, res) => {
	const searchTerm = req.body.search;
	const query = `SELECT * FROM products WHERE name LIKE '%${searchTerm}%' OR description LIKE '%${searchTerm}%'`;

	console.log('Executing query:', query);

	db.all(query, (err, rows) => {
		if (err) {
			return res.render('search', {
				products: null,
				query: searchTerm,
				error: err.message
			});
		}
		res.render('search', {
			products: rows,
			query: searchTerm,
			error: null
		});
	});
});

app.get('/info', (req, res) => res.render('info'));

app.listen(PORT, '0.0.0.0', () => {
	console.log(`Vulnerable webapp running on http://localhost:${PORT}`);
});
