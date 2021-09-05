# Rekyl portal

---

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

rekyl-portal is a tool that allows users to download all errands from a web portal into a MySQL database.

## Installation and usage
### Installation
Make sure that `config.ini` is available at the base of the project directory, structured as:
```yaml
[rekyl_portal]
username = abc
password = 123
url = https://abc.com

[linode_db]
url = mysql+pymysql://username:password@ip/db_name

[local_dev]
chrome_executable_path = local_path_to_chrome_executable
```
Make sure that `.env` is available at the base of the project directory, structured as:
```bash
REKYL_PORTAL_MYSQL_DB=abc
REKYL_PORTAL_MYSQL_USER=def
REKYL_PORTAL_MYSQL_PW=ghi
REKYL_PORTAL_MYSQL_ROOT_PW=jkl
```


Make sure that Docker is installed.


### Usage

```bash
docker-compose up --build scraper
```

Use `--build scraper` to rebuild scraper with the latest changes.

### Run locally
- Execute `docker-compose up --build scraper` in order to start the MySQL and Selenium containers
- Create and activate a virtual environment
- Install packages from requirements.txt
- Run `python browser_tools.py`
