```
42-Cybersecurity - Stockholm | First ransomware
Infects all the files contained in a folder, encrypting with AES-256-CTR.

See https://cloud.google.com/blog/topics/threat-intelligence/wannacry-malware-profile/?hl=en


Usage: ./stockholm [FLAGS]

Flags:
  -k <key>,  --key <key>      Encrypt files with <key>. It should be at least 16 chars.
  -r <key>,  --reverse <key>  Reverse the infection.
  -R                          Reverse the infection (with the default key).
  -d <path>, --dir <path>     Infect the folder <path>. By default: ~/infection/
  -s,        --silent         Do not print anything (even errors).
  -v,        --version        Get the current version.
  -h,        --help           Print this help message


Examples:
  ./stockholm
  ./stockholm -R

  ./stockholm -k this_is_a_keyphrase
  ./stockholm -r this_is_a_keyphrase

  ./stockholm -s -k this_is_a_keyphrase -d /tmp/infection
  ./stockholm -s -r this_is_a_keyphrase -d /tmp/infection

  ./stockholm -v
  ./stockholm -h


Credits: ysabik (https://github.com/Luzog78)
```
