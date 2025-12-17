const express = require('express');
const { Pool } = require('pg');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

const db = new Pool({
	host: process.env.DB_HOST || 'postgres',
	user: process.env.DB_USER || 'webapp',
	password: process.env.DB_PASSWORD || 'rootpassword',
	database: process.env.DB_NAME || 'vulnerable_db',
	port: 5432
});

const connectDB = async () => {
	try {
		await db.query('SELECT 1');
		console.log('✅ Connected to PostgreSQL database');
	} catch (err) {
		console.error(`[${new Date().toISOString()}] Database connection failed, retrying in 3 seconds...`);
		console.error(err);
		setTimeout(connectDB, 3000);
	}
};

connectDB();

app.get('/', (req, res) => res.render('index'));

app.get('/login', (req, res) => {
	res.render('login', { message: null, user: null });
});

app.post('/login', async (req, res) => {
	const { username, password } = req.body;
	const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
	console.log('Executing query:', query);

	try {
		const result = await db.query(query);
		if (result.rows.length > 0) {
			res.render('login', { message: 'Login successful!', user: result.rows[0] });
		} else {
			res.render('login', { message: 'Invalid credentials', user: null });
		}
	} catch (err) {
		res.render('login', { message: `Database error: ${err.message}`, user: null });
	}
});

app.get('/search', (req, res) => {
	res.render('search', { products: null, query: '', error: null });
});

app.post('/search', async (req, res) => {
	const searchTerm = req.body.search;
	const query = `SELECT * FROM products WHERE name ILIKE '%${searchTerm}%' OR description ILIKE '%${searchTerm}%'`;
	console.log('Executing query:', query);

	try {
		const result = await db.query(query);
		res.render('search', {
			products: result.rows,
			query: searchTerm,
			error: null
		});
	} catch (err) {
		res.render('search', {
			products: null,
			query: searchTerm,
			error: `Database error: ${err.message}`
		});
	}
});

app.get('/info', (req, res) => res.render('info'));

app.listen(PORT, '0.0.0.0', () => {
	console.log(`Vulnerable webapp running on http://localhost:${PORT}`);
	console.log(`pgAdmin available at http://localhost:8081`);
});
