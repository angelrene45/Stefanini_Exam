# Async SQLite

Script that mapping csv file into sqlite database and do some basic operations

The script read csv sales_data_samples.csv 
- Create full query from CREATE TABLE with columns names
- Store list of dictionary with values }
- Insert Data 
- Get records

## Installation

You need to create .env file inside env folder and set the enviroment variables MAPBOX_TOKEN and SECRET_KEY:

```env
pip install databases
pip install databases[sqlite]
```
