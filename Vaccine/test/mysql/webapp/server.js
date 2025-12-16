const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// VULNERABLE: Database connection with exposed credentials
const db = mysql.createPool({
	host: process.env.DB_HOST || 'mysql',
	user: process.env.DB_USER || 'webapp',
	password: process.env.DB_PASSWORD || 'webapp123',
	database: process.env.DB_NAME || 'vulnerable_db',
	waitForConnections: true,
	connectionLimit: 10,
	queueLimit: 0
});

// Connect with retry logic
let isConnected = false;
const connectDB = () => {
	db.getConnection((err, connection) => {
		if (err) {
			console.error(`[${new Date().toISOString()}] Database connection failed, retrying in 3 seconds...`);
			console.error('Error:', err.code, err);
			setTimeout(connectDB, 3000);
		} else {
			console.log('✅ Connected to MySQL database');
			isConnected = true;
			if (connection)
				connection.release();
		}
	});
};

// Handle connection errors after initial connection
db.on('error', (err) => {
	console.error('Database error:', err);
	if (err.code === 'PROTOCOL_CONNECTION_LOST') {
		isConnected = false;
		connectDB();
	}
});

connectDB();

// Home page
app.get('/', (req, res) => {
	res.render('index');
});

// Login page - VULNERABLE TO SQL INJECTION
app.get('/login', (req, res) => {
	res.render('login', { message: null, user: null });
});

// VULNERABLE: Direct SQL injection in login
app.post('/login', (req, res) => {
	const { username, password } = req.body;

	// INSECURE: String concatenation allows SQL injection
	const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;

	console.log('Executing query:', query); // For educational debugging

	db.query(query, (err, results) => {
		if (err) {
			return res.render('login', {
				message: `Database error: ${err.message}`,
				user: null
			});
		}

		if (results.length > 0) {
			res.render('login', {
				message: 'Login successful!',
				user: results[0]
			});
		} else {
			res.render('login', {
				message: 'Invalid credentials',
				user: null
			});
		}
	});
});

// Product search page - VULNERABLE TO SQL INJECTION
app.get('/search', (req, res) => {
	res.render('search', { products: null, query: '', error: null });
});

// VULNERABLE: SQL injection in search
app.post('/search', (req, res) => {
	const searchTerm = req.body.search;

	// INSECURE: String concatenation allows SQL injection
	const query = `SELECT * FROM products WHERE name LIKE '%${searchTerm}%' OR description LIKE '%${searchTerm}%'`;

	console.log('Executing query:', query); // For educational debugging

	db.query(query, (err, results) => {
		if (err) {
			return res.render('search', {
				products: null,
				query: searchTerm,
				error: `Database error: ${err.message}`
			});
		}

		res.render('search', {
			products: results,
			query: searchTerm,
			error: null
		});
	});
});

// Info page explaining vulnerabilities
app.get('/info', (req, res) => {
	res.render('info');
});

app.listen(PORT, '0.0.0.0', () => {
	console.log(`Vulnerable webapp running on http://localhost:${PORT}`);
	console.log(`PHPMyAdmin available at http://localhost:8081`);
});
