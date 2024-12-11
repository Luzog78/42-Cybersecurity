```
42-Cybersecurity - Inquisitor | ARP Spoofer
ARP Spoofing attack to sniff FTP traffic between a Router and a Victim.

Example:
  Router: 192.168.0.1 [00:00:00:00:00:01]
  Victim: 192.168.0.2 [00:00:00:00:00:02]
  Attacker:           [00:00:00:00:00:03]

Before the attack:
  192.168.0.2 (Victim) wants to send a packet to 192.168.0.1 (Router)
  Victim's ARP Table:
    - 192.168.0.1 --> [00:00:00:00:00:01]
  The packet to 192.168.0.1 (Router) will go to [00:00:00:00:00:01] (Router)

After the attack:
  Attacker send an ARP-Update packet to Victim.
  Updated Victim's ARP Table:
    - 192.168.0.1 --> [00:00:00:00:00:03]
  The packet to 192.168.0.1 (Router) will go to [00:00:00:00:00:03] (Attacker)


Usage: ./inquisitor <IP-src> <MAC-src> <IP-target> <MAC-target>

Flags:
  -v, --verbose  Show all FTP traffic
  -h, --help     Print this help message


Example:
  ./inquisitor 192.168.0.2 00:00:00:00:00:02 192.168.0.1 00:00:00:00:00:01
  ./inquisitor  172.27.0.4 02:42:ac:1b:00:04  172.27.0.2 02:42:ac:1b:00:02 -v

Credits: ysabik (https://github.com/Luzog78)
```