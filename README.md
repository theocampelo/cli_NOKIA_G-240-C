Remote CLI NOKIA G-240-C Project

I've tried accessing it via terminal-based web-browsers but none really worked out because of JS interactions
(of course I could've used a proxy, VPN or DMZ I guess, that would probably have made things
quite a bit easier, but not quite as fun, though)

Notes:
* Router web access is default HTTPS (but insecure); running python requests library with param "verify=False" for invalid SSL GET/POST requests)
* All router's scripts are cgis.
* Encryption algorithms are readable on the cgi router pages' source code
* CSFR token and "nonce" tokens are used
* CSFR token is not reset after each operation, it's set by each valid logged session (by unique encrypted params/hashes)

Researching my home GPON router for remote management; port 80 forwarding is blocked and apparently you can't enable it, hence this thing.
Currently working on:

* Logging in with default credentials (via an SSH machine on the same network as the router)
* Port forwarding rules (TCP, UDP, TCP/UDP) / POST request with payload
* Deleting port forwarding rules (simple GET request with url ID parameters) / Parse HTML to get the id

TODO:
* Rewrite encryption algorithms to generate valid CSFR token and nonce/unique strings/hashes in PYTHON (currently run in JS)
* Reorganise code structure in separate files (main.py is merely a test file, a sketch of sorts if you will)
* Consider using a proxy to operate remotely without having to SSH into local machines
* Consider using BURP to intercept traffic and analyze requests (maybe before rewriting the enc. algo.; there might be a workaround this thing)
