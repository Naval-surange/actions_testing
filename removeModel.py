def removeModel(Name):
    import yaml
    with open("cube_store_mapping.yml", 'r+') as file:
        documents = yaml.full_load(file)
        if not documents:
            documents = {}
        if Name in documents:
            del documents[Name]
        
        file.seek(0)
        file.truncate()
        yaml.dump(documents, file,sort_keys=False)

    # remove model file
    import os
    try:
        os.remove("./model/cubes/"+Name+".yml")
    except:
        print("Model not found")

import sys
if(len(sys.argv) != 2):
    print("Please provide the name ")
    print("Example: python3 generateModel_RES_ID.py name ")
    exit(0)
    
Name = sys.argv[1]
removeModel(Name)

# Bankwise_ATM_POS:
# - res_id: ff48df57-58c2-4eb4-9c12-e604c9651790
# - orignal_name: Bankwise ATM POS Card Statistics