<div align="center">

# 42 Cursus - Cybersecurity: ft_onion

<img src="https://upload.wikimedia.org/wikipedia/commons/c/c9/Tor_Browser_icon.svg" height="30" alt="Tor" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg" height="30" alt="nginx" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ssh/ssh-original.svg" height="30" alt="ssh" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg" height="30" alt="docker" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg" height="30" alt="HTML5" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" height="30" alt="vscode" />

<br><br>

</div>


## Overview

- **Summary:** *Unleash the power of anonymity on the Internet. First use of Tor network by creating a hidden service.*
- **Version:** *1.00*
- **Subject:** [en.subject.pdf](https://cdn.intra.42.fr/pdf/pdf/88969/en.subject.pdf)
- **Author(s):** *[ysabik](https://profile.intra.42.fr/users/ysabik)*
- **Public repo:** [GitHub](https://github.com/Luzog78/42-Cybersecurity)

<br>

- [[ft_onion]](#42-cursus---cybersecurity-ft_onion)
	- [[Installation]](#installation)
	- [[Overview]](#overview)
		- [[Web server]](#web-server)
		- [[SSH access]](#ssh-access)
		- [[Tor hidden service]](#tor-hidden-service)


<br><br>

## Installation

To install the project dependencies and build the required files, you can run:
```bash
make all
```

For more information on the available commands, you can run:
```bash
make help
```


<br><br>

## Overview

The created container will run 3 main services:

#### Web server

A web server containing a fun ascii camera page is running via nginx on port 80.

Here is a [link](http://localhost:8080) to access it. But you can also run:
```bash
open http://localhost:8080
```

#### SSH access

An SSH server is running on port 4242. It is secured with a private key.
No password is accepted and other security measures are in place.

You can connect using the following command:
```bash
ssh -i ssh.key root@\:\:1 -p 4242
```

#### Tor hidden service

Lastly, the web server is also configured as a Tor hidden service.

When the container builds, it will generate a hidden service URL in the format:
`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.onion`, where all
the `x` are the unique identifier for your hidden service.

Once found, open the Tor browser. You can do it by running:
```bash
torbrowser-launcher
```

Next, connect to the Tor network and then navigate to the hidden service URL.


<br><br>

---

<sup><i>This is an educational project proposed by 42 School through the 42Cursus program.</i><sup>
