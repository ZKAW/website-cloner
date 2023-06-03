# Basic website cloner

**Description:**

* This script is a basic website cloner that downloads all the files from a website and saves them in a folder.
* It works by scraping all the links on the page, save them locally, and replace them with the local path.

## Installation

## From [pypi](pypi.org).

```sh
pip3 install wclone
```

## From source

```sh
git clone https://github.com/Simatwa/website-clone.git
cd website-cloner
bash install.sh
```

## Usage

```sh
$ wclone <url>
```

**More info:**

* In order to use the tor network, you need to download the [tor package](https://www.torproject.org/dist/torbrowser/11.0.9/tor-win32-0.4.6.10.zip) and start the tor service.

<details>

<summary>

> For further info run `$ wclone --help`

</summary>

<details>

```
 usage: wclone [-h] [-v]
              [-tp PROXY]
              [-o FOLDER]
              [-w PATH]
              [--use-tor]
              host

Basic website cloner written in Python

positional arguments:
  host       URL pointing to a
             website

options:
  -h, --help
             show this help
             message and exit
  -v, ---version
             show program's
             version number and
             exit
  -tp PROXY, --tor-proxy PROXY
             Proxy server url
             without schema -
             localhost:9050
  -o FOLDER, --output FOLDER
             Folder for saving
             contents - host
  -w PATH, --workspace PATH
             Directory for saving
             contents - /storage/
             emulated/0/git/Smart
             wa/website-cloner
  --use-tor  Use tor proxy -
             False
```
</details>





