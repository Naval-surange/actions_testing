def generateModel(filePath, schema_table, yml_name):
    import pandas as pd
    import numpy as np

    # Read the data
    df = pd.read_csv(filePath)

    columns = df.columns
    dtypes = df.dtypes

    primary_contains = ["id"]
    temporal_contains = ["date", "time", "year",
                         "month", "day", "hour", "minute", "second"]
    ordinal_dtypes_contains = ["int", "float", "double"]
    ordinal_ignore = ["code"]

    primary_col = []
    temporal_cols = []
    ordinal_cols = []
    category_cols = []

    for col in columns:
        if any(x in col.lower() for x in primary_contains):
            primary_col.append(col)
        elif any(x in col.lower() for x in temporal_contains):
            temporal_cols.append(col)
        elif any(x in str(dtypes[col]) for x in ordinal_dtypes_contains) and not any(x in col.lower() for x in ordinal_ignore):
            ordinal_cols.append(col)
        else:
            category_cols.append(col)

    yml_dict = {
        "cubes":
        [
            {
                "name": yml_name,
                "sql_table": "public.\\\""+schema_table+"\\\"",
                "joins": [],
                "dimesnions": [],
                "measures": [],
            }
        ]
    }

    for cols in ordinal_cols:
        yml_dict["cubes"][0]["measures"].append({
            "name": cols,
            "sql": "SUM("+cols+")",
            "type": "number"
        })

    yml_dict["cubes"][0]["dimesnions"].append({
        "name": primary_col[0],
        "sql": primary_col[0],
        "type": "string",
        "primaryKey": True
    })

    for cols in category_cols:
        yml_dict["cubes"][0]["dimesnions"].append({
            "name": cols,
            "sql": cols,
            "type": "string"
        })

    for cols in temporal_cols:
        yml_dict["cubes"][0]["dimesnions"].append({
            "name": cols,
            "sql": cols,
            "type": "time"
        })


    import yaml
    class MyDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(MyDumper, self).increase_indent(flow, False)

    with open(yml_name, 'w') as outfile:
        outfile.write(yaml.dump(yml_dict,Dumper=MyDumper))


import sys
if(len(sys.argv) != 4):
    print("Please provide the file path, schema.table name and yml name")
    print("Example: python generateModel.py /home/username/data.csv schema.table_name yml_name.yml")
    exit(0)
    
filePath = sys.argv[1]
schema_table = sys.argv[2]
yml_name = sys.argv[3]
generateModel(filePath, schema_table, yml_name)