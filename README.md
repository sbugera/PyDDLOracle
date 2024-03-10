[![PyDDLOracle](https://circleci.com/gh/sbugera/PyDDLOracle.svg?style=svg)](https://circleci.com/gh/sbugera/PyDDLOracle)

# PyDDLOracle
## Oracle Database DDL Extractor
### Version 1.0.0

This is a simple tool to extract objects DDL from Oracle Database and store them in files.

## Requirements
* Python 3.6+
* Database user with ```SELECT_CATALOG_ROLE``` and ```CREATE SESSION``` privileges

If ```SELECT_CATALOG_ROLE``` is not allowed, you can grant privileges listed in [privileges.sql](privileges.sql) to the user.

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
  * Constraints
  * Partitions (sub-partitions and reference partitions are not implemented yet)
  * Storage parameters (LOB storage parameters are not implemented yet)
  * Indexes
  * Comments
  * Grants