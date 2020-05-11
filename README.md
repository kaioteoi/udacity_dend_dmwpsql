`Udacity - Data Engineer nanodegree project`

# Sparkify ETL

## Requirements
- [Python 3+](https://www.python.org/downloads/)
- [Postgres 9.5](https://www.postgresql.org/download/)

*If you want to experiment with the provided notebooks:*

- [Jupyter notebook](https://jupyter.org/install)

## Running the ETL
Make sure to have `Python3` installed, as per *requirements* section.

At the project root dir, execute the following command on your terminal:
```bash
$ python etl/etl.py
```

## Project files

### etl/etl.py
Main script responsible for processing all the data

### etl/create_tables.py
Script file responsible for bootstrapping all the tables used on ETL process.

**Attention: this script DROP all the tables as part of its bootstrap process, be aware to avoid losing any data.**

### etl/sql_queries.py
Centralizes all SQL statements used on `create_tables.py` and `etl.py` scripts.

---

### data/log_data/
Contains all the log data from user interaction logs on the platform.

### data/song_data/
Contains the metadata about the song itself (band name, album, year of release).

---

### playbooks/etl.ipynb
Playbook containing step by step process applied on `etl.py` final script.

### playbooks/test.ipynb
Playbook containing SELECT statements for `etl.py` processing validation purposes.
