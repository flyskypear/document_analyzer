# AI Document Analyzer

Clone this repository, set the path for the folder where all the files are stored and the arguments for the analyzer in `docker-compose.yml`. 

Then the following commands can be ran:

To run the analyzer interactively:

```bash
[user@localhost document_analyzer]$ docker compose run --rm analyzer
```

To run the jupyter lab with the analyzer notebook and code:

```bash
[user@localhost document_analyzer]$ docker compose run --rm --service-port notebook
```