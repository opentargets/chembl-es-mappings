# chembl-es-mappings

Helper scripts to ensure that indexes queried by PIS have not changed.

## ElasticSearch index mapper

Program to query ChEMBL ElasticSearch and create simplified representation of
indexes which begin with the name `chembl`.

This was created to help quickly get an overview of the fields present in
ElasticSearch, as not all objects queried have all fields present, so it isn't
sufficient to use an 'example' object and assume that it is a proper
representation of the index where it came from.

When run the script will create a _simplified_ json representation of each index
in the directory from which the script is executed. The simplification
is of the form of datatype which will be either "keyword", "boolean", or
"short".

An additional file, `indices_combined` is created which concatenates all of the
other indices. This is useful for finding a field when you don't known which
index contains it.

This script is a diagnostic tool, and results should be properly verified!

## Requirements

- Python 3.8
- dependencies as specified in the `requirements.txt` file.

It is easiest to create a virtual environment to run the script in. See
[here](https://docs.python.org/2/library/venv.html#module-venv) for details.

## Running

1. Set up environment variables pointing to ChEMBL ES:

```
export ES_CH_URL=<some value>
export ES_CH_PORT=<some value>
```

2. Execute `python3 <path to file>` from within the directory in
   which you want to generate the json files.

3. Run the script `compare-chembl.sh` to see a basic overview of differences between selected indexes. The
   script only checks for differences in the indexes that are used in Platform Input Support
   as inputs. The fields that are used are subject to change as the ChEMBL resource is
   further exploited. To get a current list consult the `config.yml` file of the PIS.
