def generateModel(id):
    import pandas as pd
    import numpy as np

    # Read the data

    Datasotre_API = f"https://ckan.indiadataportal.com/api/3/action/datastore_info?id={id}&include_unique=false"
    Resource_API = f"https://ckan.indiadataportal.com/api/3/action/resource_show?id={id}"

    
    try:
        df = pd.read_json(Datasotre_API)
    except:
        print("datastore not found")
        exit(0)
    # print(df)
    # return
    data = df['result']['fields']

    resourceData = pd.read_json(Resource_API)


    primary_contains = ["id"]
    temporal_contains = ["date","time","year","month","day","hour","minute","second"]
    ordinal_dtypes_contains = ["int","float","double","numeric"]
    ordinal_ignore = ["code"]

    primary_col = []
    temporal_cols = []
    ordinal_cols = []
    category_cols = []

    for col in data:
        if col["schema"]["is_index"]:
            primary_col.append(col["id"])
        elif any(x in col["id"].lower() for x in temporal_contains):
            temporal_cols.append(col["id"])
        elif any(x in col["type"].lower() for x in ordinal_dtypes_contains) and not any(x in col["id"].lower() for x in ordinal_ignore):
            ordinal_cols.append(col["id"])
        else:
            category_cols.append(col["id"])

    name = resourceData["result"]["name"].split(".")[0]
    to_replace = ["-"," ","/","(",")",".","%","&","'","\"","/","\\","|","@","!","#","$","^","*","~","`","=","+","{","}","[","]",";",":","<",">","?"]
    for i in to_replace:
        name = name.replace(i,"_")

    if(len(name.split("_")) > 3):
        name = name.split("_")[:3]
        name = "_".join(name)
    else:
        name = name.split("_")
        name = "_".join(name)

    yml_dict = {
        "cubes":
        [
            {
                "name" : name,
                "joins": [],
                "dimensions": [],
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

    # add to inculude primary key in datamodeling

    # yml_dict["cubes"][0]["dimensions"].append({
    #     "name": primary_col[0],
    #     "sql": primary_col[0],
    #     "type": "string",
    #     "primaryKey": True
    # })


    for cols in category_cols:
        yml_dict["cubes"][0]["dimensions"].append({
            "name": cols,
            "sql": cols,
            "type": "string"
        })

    for cols in temporal_cols:
        yml_dict["cubes"][0]["dimensions"].append({
            "name": cols,
            "sql": cols,
            "type": "time"
        })


    import yaml
    class MyDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(MyDumper, self).increase_indent(flow, False)

    with open("./model/cubes/"+name+".yml", 'w') as outfile:
        outfile.write(yaml.dump(yml_dict,Dumper=MyDumper,sort_keys=False))
        outfile.write("    sql_table: \"public.\\\""+id+"\\\"\"")
        outfile.write("\n")
    
    orignal_name = resourceData["result"]["name"]
    cube_name = name
    res_id = id

    with open("cube_store_mapping.yml", 'r+') as file:
        documents = yaml.full_load(file)
        if not documents:
            documents = {}
        documents[cube_name] =  [{"res_id":res_id},{"orignal_name":orignal_name}]
        file.seek(0)
        yaml.dump(documents, file,sort_keys=False)




import sys
if(len(sys.argv) != 2):
    print("Please provide the RES_ID ")
    print("Example: python3 generateModel_RES_ID.py RES_ID ")
    exit(0)
    
RES_ID = sys.argv[1]
generateModel(RES_ID)