<div align="center">

# 42 Cursus - Cybersecurity: ft_otp

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="30" alt="python" />
<img width="12" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" height="30" alt="vscode" />

<br><br>

</div>


## Overview

- **Summary:** *Nothing ever lasts forever... Tool for OTP generation and validation.*
- **Version:** *1.00*
- **Subject:** [en.subject.pdf](https://cdn.intra.42.fr/pdf/pdf/88968/en.subject.pdf)
- **Author(s):** *[ysabik](https://profile.intra.42.fr/users/ysabik)*
- **Public repo:** [GitHub](https://github.com/Luzog78/42-Cybersecurity)

<br>

- [[ft_otp]](#42-cursus---cybersecurity-ft_otp)
	- [[Installation]](#installation)
	- [[Overview]](#overview)


<br><br>

## Installation

To install the project dependencies and build the required files, you can run:
```bash
make
```

For more information on the available commands, you can run:
```bash
make help
```


<br><br>

## Overview

```
42-Cybersecurity - ft_otp | TOTP generator
 > [RFC 6238](https://tools.ietf.org/html/rfc6238)
 > [RFC 4226](https://tools.ietf.org/html/rfc4226)

Usage: ./ft_otp [FLAGS]

Flags:
  -g <file.key>, --generate <file.key>     Generate a new key, and save it in <file.key>
  -G <file.key>, --generate-qr <file.key>  Generate a new key, save it in <file.key>, and show it in the console
  -k <file.key>, --key <file.key>          Takes the key in <file.key> (minimum 64 hexa chars) and give the TOTP
  -s <seconds>,  --time-step <seconds>     Set the time step to <seconds> (default 30)
                 --qr <file.key>           Show the qrcode of the secret file
                 --gui                     Use GUI instead of terminal
  -v,            --verbose                 Print always in terminal (with GUI)
  -h,            --help                    Print this help message

Credits: ysabik (https://github.com/Luzog78)
```

Create a new key:
```bash
./ft_otp -G key.key -s 10
```

Verify the TOTP:
```bash
./ft_otp -k key.key

# Same as
oathtool --totp $(cat key.key)
```

Use the GUI:
```bash
./ft_otp --gui
```

Examples:
```
 ➜  ./ft_otp -Gv key.key
Key generated and saved in key.key
6059066c497062cb39e9eca4e2acf3c2d47c1a5d2e17ce4da977f91645d08f2beac3f9dfbdac435ef8c42ce98910a5d3f71863deaeceb9e59f72d85adb1f0ef505429cf798712fb3447de21242f76c86c504b758563f3637e6119b39e2c6a4f0c485a834d5dff938f34db1119bcdede3279da24d9071c854c370c861dbba0d8a04f8df3243552e178ce4b66cb2456d27127bf7e7f54a1abb4715d803132df54425ad7a7478569cabcad02f67b69c8c0fec1661e26eb7dc83ad8192b743921953f28c1e7f46fa34de34d4f378849c85daeb21f3633fd279b22a79bfa9b2925bff744e11852293f8963722bb7d0d79ef121c4c141b0e26347c05b07079ccf8e2c1
                                                                         
                                                                         
    █▀▀▀▀▀█ ▀ ▀▀█▄█▄ ██▀█▄▄▀ █ ▀▄█▄ ▀  ▀▄  ▀▄▀▀ ▄█ ██ ▀▀█▄ ▀▄ █▀▀▀▀▀█    
    █ ███ █ █ ████  ▄▄█  ▄█▀ █▀██▀▀▄ ▄  ▄▄ ▄ ▀▄█ █▀▀▀▄ █  █▄▀ █ ███ █    
    █ ▀▀▀ █ ▀█  ▀▀ █   ▄ ▀  ██▀ ▀▄█▀▀▀█▀ ▀▄ ▀█▄█▄█   ▀███ ▄ ▀ █ ▀▀▀ █    
    ▀▀▀▀▀▀▀ ▀▄█ █ █▄▀▄▀ █▄█▄▀▄▀ █ █ ▀ █▄█ ▀ ▀ ▀ █ ▀ █ ▀▄█ ▀ █ ▀▀▀▀▀▀▀    
    █▀█▀▄▄▀▄▀▀▄▀██▀██▀██ █ ▄▀▄▀▄█▄▀█▀█▀ ▄▀▄██ ██▀██▄ ▀▀█  ▄▀██ ▄█▀▀ █    
    ▄ ███ ▀  █▀▀▀█ ▀   █▀██▀ ▀▀▀▄ ▀▀ ▄█▀▄▄█ █▄▄▀▄  ██▄ ▀▀ ▀▀▀▀ ▄█ ▄ █    
    ▀█▄ ▀ ▀ ▀██▄ ▀  ▀ ▄█ ▄▀▀▀▄█▄▄██▄▄█ ▀█▄ ▄ ▀▀█▄ ▄▀▀   ▄ ▀▄▀▀▀▀▀████    
    ▀ ▀█▄ ▀▀▄▄▄▀█  ▄▀█▄ ▄▀▀█ ▀█▄▀█▄█ ▄▄▀█▀▀ █ ▀ ▄ ▀▄█▄▄▄▀▄█   ▄▄▀██▀█    
    ▀▄ ▄▄▄▀█ ▄▄▄ ▀▄▄▀█ ██ ▀▄ ▀▄▀   ▄█▄ ▄▄█▀▄▄█ ▀ ▄▀▀▀ ▄▀▄▀▀█  ▀ ▀ ▀██    
    ▄█▀▄▀▄▀▄▄  █▀▀▄  ▀  ▄▀██▀ █▀ ▄█ ████  ▄▀▄ █▀▄ ▄█▄▀▄ ▄▀▄▄ ▄▀ ▄▄▄██    
     ▄ ▀ ▄▀█▄ ▄█▀▄▀█▀▄▄▄▀▀▀  █▀▄▀ █▄▀▀ ██  ▄ ▀▄▄ █▀█ █▀▄▄▀█▄▀▄▀ ▄ ▀██    
    ▄█████▀  ▀▄▄▄█▄▀▄▀  ▀███▀▄▀█▀▄▀▀  ▄▄▄▄█▀▄▀▀█ █▀ ▄█▄▀ ▄█ ▀▀▀▀█▄▀      
    ▄█▀▄▄ ▀█ ▄▄▀█ ███▀▀▄█▀▀█ █▀▄▄▄ ▀█▀█▄▄█▄  ██▄▄▀▀▄█▄ █▄▄▀▄▀ ▀▀▀ █▄█    
      ▀▄██▀▀ ▄ █▄ █  ▀▄▀▄▀ █▄▀▄▄█ ▀▄█▀▄█▀▄ ██▄  ▄▄▄  █ ██▄▀▄▄▀▄ █ ▄██    
     ▄ █▄▄▀▀█▀█▀█▄█▄ ▀▀▀▀▄█▄▄█▀█▄█▄▄█▀▄▀ ▄▀█▀▀▀██▄  ▄▀ █▄▄▄▀█▀█▀▀▄▄      
    ▄ █ █▀▀▀█▀   ▄▀██▄▀ ▀ ▀▄█   █▄█▀▀▀█▄▀▀▄▀▄██▄ ▀▄▄█ ▄██▄█ █▀▀▀█▄▀▄▄    
    ▄██ █ ▀ █▄███▀   ██▄  ▄▀███▄▄▀█ ▀ ██ ▀ ▀▀▀█▀ █  ▄▀▀▀ █▄▄█ ▀ █▀ ██    
    ▄▄▀▀██▀█▀ ▀█▄█▄▀  ▀  ██ ▄  ▀▄█▀▀▀██▄▀ ██▀  ▄▀█▀ ▀▄▀▀██▀ ▀▀▀▀█ ▀▄█    
     ▀▀▄▄▄▀ ▀   ▄▀▄▄ █   █ ▀ █▄▄▄ █▀▄█▄█▄▄█▄▄█   ▄▀▀███ █▄▀▄█▀▄ █▄▀██    
       █▀▀▀ █  ▀▄█▄██  ▄ ▀ ▄  ▀▀█▀██ ▄▀▄▀▀█▄ █▀▄██▄▄▀█▀███████ ▀█▀ ▄█    
    █ ▄▀██▀▀▀▄▀█▀▄▀███ ▄█  ▀███ ▀▀██ ▄█▀█▀  ▄█  ▄   ▄▀ ▀ ▄▀ ▄▀ █▀█▄▀     
    █▄▄▀▄ ▀███▀█▄▄▄ ▄▀█▄▄▄▀▄█ ▀▄▄ ▀  █▀ █▄  ▀██▄ ▄▀ ▄█▄▄▄▄ █▄ █ ▀▄▀▀▀    
      ▀▄▄▀▀▄█ ██ ▄█▄▀█   ▄▄█▄  ▄█▄ ▄▄▄ ▀██ ▀▄ █▄▄█ █▄▄█▀█▄▀ ▄▀▀▄▀▀▀▄▄    
    ██▄  ▀▀▀█ ▀█▀   ▄▄▄██▄▀ ▄▄▀▄ ▄▄ █▀ ▀▀██▀▀▀▀▄█ ▀  ▀▄▄▄ ▄ ███     ▄    
    ▀   █▀▀███▀▄ █ █ ▀▀█ ▄ ▄▄▄ ▀▀█▄▄█▄▄▀██ ▀▄ █▀ ██▀ █▄▄▀ ▄▄▀▄█ ▄▀▄█     
    █▄▀▀ ▀▀▄▄ ▄▀▄ ▄ ▀█▀▀██▄▀▄ ▀▀▀ ██  ███▀▄▀▀▄▄▀█▄▀ ▄▄▀▄▀ ▄ ▄▀██ ▄ ▀▀    
    ██▀▄▄█▀  ██▀ █▀██  ▀ ▀▄▄▄  ▄▄▄ ▀▀▄ ▄█ ▄ ▀█▄  ████▀▀▀▄▀▀ ▀▄ ███▄▄▄    
    ▄ ▀█ ▀▀█▀ ▄▄ ▀█▄▄ ▀▄▄██  █  ▀██▄   ▀▀▀  ▀█▄▀▄████▄█▀█▄ ▄ ▄ ▀█▄ █     
     ▀▀ ▀ ▀▀▄  ▄ █▀▄ ▀▄ ▀█ ▀ ██▀▀▀█▀▀▀███▄█ ▄▄▄  █▀ ██▄█ █▀▀█▀▀▀█▄███    
    █▀▀▀▀▀█  ▀▄   ▀▄█▄▄▄ ▀ ▄█▄▀▀▄▀█ ▀ █  ▄▀█▄█ ██▄▄██ █ █ ▀ █ ▀ █▀       
    █ ███ █ ▄▄▄▀██ ▀▄▀█▀ ▄ ▀█ ▀▀ ████▀█ ▄▀  ▄  █▄▀▄▀█▄▄▄ ▀█▄█▀█▀█ █ ▀    
    █ ▀▀▀ █ █▄ ▄ ▄█▀█▀█ ▄█ ▄ █▀▀█▀ ▄▄   ██▄▄ █▄  ▄ ▄▄▀▄▀ ██▀   █▄ ▀▄▀    
    ▀▀▀▀▀▀▀ ▀▀ ▀▀ ▀ ▀    ▀▀   ▀     ▀▀   ▀ ▀▀  ▀▀ ▀ ▀ ▀▀ ▀▀▀▀▀     ▀     
                                                                         
                                                                         

 ➜  ./ft_otp -k key.key
358398

 ➜  sleep 30

 ➜  ./ft_otp -k key.key
521334
```


<br><br>

---

<sup><i>This is an educational project proposed by 42 School through the 42Cursus program.</i><sup>
