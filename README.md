# LinkedIn Connections

LinkedIn Connections is a small helpfull script for sending connections in LinkedIn.

## Usage

Just clone the project and run it with the following parameters:

```sh
--username <your login for LinkedIn>
--password <your password for LinkedIn>
--connections <count of needed connections per run>
--search_url <prepared search url in quotes (open LinkedIn and make some search with needed parameters)>
--webdriver_path <absolute path to the Chrome Webdriver>
```

Example for running:
```sh
 python3 linkedin_connect.py --login=johnsmith@gmail.com --password=qwerty --connections=30 --search_url="https://www.linkedin.com/search/results/people/?geoUrn=%5B%22105080838%22%5D&industry=%5B%2296%22%5D&keywords=human%20resources&origin=FACETED_SEARCH&serviceCategory=%5B%2249%22%5D&sid=RZV"
```

## License
MIT

**Free Software, Hell Yeah!**