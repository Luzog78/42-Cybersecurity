<div align="center">

# 42 Cursus - Cybersecurity: Arachnida

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="30" alt="python" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" height="30" alt="vscode" />

<br><br>

</div>


## Overview

- **Summary:** *Introductory project to web scraping and metadata extraction and edition.*
- **Version:** *1.00*
- **Subject:** [en.subject.pdf](https://cdn.intra.42.fr/pdf/pdf/88967/en.subject.pdf)
- **Author(s):** *[ysabik](https://profile.intra.42.fr/users/ysabik)*
- **Public repo:** [GitHub](https://github.com/Luzog78/42-Cybersecurity)

<br>

- [[Arachnida]](#42-cursus---cybersecurity-arachnida)
	- [[Installation]](#installation)
	- [[Overview]](#overview)
	- [[Spider]](#spider)
	- [[Scorpion]](#scorpion)


<br><br>

## Installation

To install the project dependencies and build the required files, you can run:
```bash
make
```

To run a basic http server for testing, you can run:
```bash
make test
```

For more information on the available commands, you can run:
```bash
make help
```


<br><br>

## Spider

```
spider: Spider is a web crawler. It takes a URL and crawls it for links and files.
spider: Its goal is to find and download certain files (.jpg, .jpeg, .png, .gif and .bmp).
spider:
spider: Syntax:
spider: ./spider.py [flags...] <URL>
spider:
spider: Flags:
spider:   -r               recursively downloads the files
spider:   -l <limit>       recursion limit (default: 5)
spider:   -p <save_path>   path to save files (default: "./data/")
spider:   -c               clear files in "save_path" before crawling
spider:   -s <sleep_time>  time (in sec) to wait between requests (default: 0)
spider:   -h, --help       display this help message
```

```bash
# In a terminal
make test

# In another terminal
./spider http://localhost:8000 -r
```

```bash
./spider https://fr.wikipedia.org/wiki/Venezuela -s 1 -c
```


<br><br>

## Scorpion

```
scorpion: Scorpion is an EXIF metadata editor. It takes image files and
scorpion:  allows you to view and edit their EXIF metadata.
scorpion:
scorpion: Syntax:
scorpion: ./scorpion.py [flags...] <image> [<images>...]
scorpion:
scorpion: Flags:
scorpion:   -h, --help       display this help message
```

```bash
# First, fetch images using spider
./spider http://localhost:8000 -r

# Then, see/edit the images exifs using scorpion
./scorpion data/127.0.0.1\:8000/*
```


<br><br>

---

<sup><i>This is an educational project proposed by 42 School through the 42Cursus program.</i><sup>
