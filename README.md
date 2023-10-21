# ExtOra
## Oracle Database DDL Extractor
### Version 1.0.0

This is a simple tool to extract objects DDL from Oracle Database and store them in files.

## Requirements
* Python 3.6+
* Database user with ```SELECT_CATALOG_ROLE``` and ```CREATE SESSION``` privileges

If ```SELECT_CATALOG_ROLE``` is not granted, you can use the following privileges instead:
```sql
grant select on sys.dba_tables           to <your_db_username>;
grant select on sys.dba_tab_cols         to <your_db_username>;
grant select on sys.dba_all_tables       to <your_db_username>;
grant select on sys.dba_part_tables      to <your_db_username>;
grant select on sys.dba_part_key_columns to <your_db_username>;
grant select on sys.dba_tab_partitions   to <your_db_username>;
```

## Installation

```
pip install -r requirements.txt
```

##  Settings
Rename [config_con.ini.template](./config_con.ini.template) to ```config_con.ini``` and edit it with your database connection parameters.

File names, output directory and other settings can be changed in [config.ini](./config.ini).

## Usage

```
python main.py [-s <schema name>]
```
Where ```schema_name``` is the name of the schema to extract. If not specified, connection user will be used.

For example:
```
python main.py -s HR
```
or:
```
python main.py
```

## Currently supported objects
* Tables
  * Columns
  * Constraints (only NOT NULL)
  * Partitions (only RANGE and LIST)
  * Storage parameters