[![PyDDLOracle](https://circleci.com/gh/sbugera/PyDDLOracle.svg?style=svg)](https://circleci.com/gh/sbugera/PyDDLOracle)

# ExtOra
## Oracle Database DDL Extractor
### Version 1.0.0

This is a simple tool to extract objects DDL from Oracle Database and store them in files.

## Requirements
* Python 3.6+
* Database user with ```SELECT_CATALOG_ROLE``` and ```CREATE SESSION``` privileges

If ```SELECT_CATALOG_ROLE``` is not allowed, you can use the following privileges instead:
```sql
grant select on sys.dba_tables           to <your_db_username>;
grant select on sys.dba_tab_cols         to <your_db_username>;
grant select on sys.dba_all_tables       to <your_db_username>;
grant select on sys.dba_part_tables      to <your_db_username>;
grant select on sys.dba_part_key_columns to <your_db_username>;
grant select on sys.dba_tab_partitions   to <your_db_username>;
grant select on sys.dba_tab_comments     to <your_db_username>;
grant select on sys.dba_col_comments     to <your_db_username>;
grant select on sys.dba_indexes          to <your_db_username>;
grant select on sys.dba_object_usage     to <your_db_username>;
grant select on sys.dba_ind_columns      to <your_db_username>;
grant select on sys.dba_constraints      to <your_db_username>;
grant select on sys.dba_recyclebin       to <your_db_username>;
grant select on sys.dba_cons_columns     to <your_db_username>;
```

## Installation

```
pip install -r requirements.txt
```

##  Settings
Rename [config_con.template.yaml](config_con.template.yaml) to ```config_con.yaml``` and edit it with your database connection parameters.

File names, output directory and other settings can be changed in [config.yaml](config.yaml).

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
  * Partitions (only RANGE, LIST and HASH)
  * Storage parameters
  * Indexes
  * Comments