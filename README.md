# quick-recon.py
Do some quick reconnaissance on a domain-based web-application.  
This is very useful if you test a single web-application or domain and don't have time (mood) to gather information manually.

**Features**

* Do a HTTP-OPTIONS request to lookup the allowed HTTP methods
* Print the HTTP-response headers set by the server
* Get the used technology (webserver, proxy, languages, scriptlanguage, frontend, frameworks) based on: w3techs.com
* Get the name of the CMS (if in use) based on: whatcms.org
* Read out: robots.txt
* Bruteforce some interesting files, wordlist from: github.com/hannob/snallygaster

**Installation**

`pip -r requirements.txt`

**Usage**

```
quick-recon.py [-h] domain

positional arguments:
  domain      domain (by URL;e.g. https://test.de)

optional arguments:
  -h, --help  show this help message and exit
```

**Example**

Executing `python quick-recon.py https://bund.de` will output:

```
[!] HTTP-OPTIONS failed
[-] HTTP-response header:
---
	Date: Sun, 17 Jun 2018 21:54:00 GMT
	Content-Length: 233
	Keep-Alive: timeout=5, max=100
	Connection: Keep-Alive
	Content-Type: text/html; charset=iso-8859-1
	Set-Cookie: {..}
---
[!] No "Server"-header
[-] W3-technologies:
--
	Content Management: Government Site Builder
	Server-side Language: Java
	Client-side Language: JavaScript
	JavaScript Library: jQuery
	Markup Language: HTML5
	Character Encoding: UTF-8
	Image File Formats: PNG, JPEG
	Site Elements: External CSS, Inline CSS, Session Cookies
	SSL Certificate Authority: Deutsche Telekom
	Server Location: Germany
	Content Language: German
--
[!] No CMS detected
[!] No robots.txt
[!] Checking interesting files
[-] Checked 50% of dictionary
[!] Finished quick-reconnaissance on: https://bund.de
```
