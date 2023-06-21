## Script to generate datamodel for a given resource with resurce ID

### Usage: 

```bash
python3 generateModel_RES_ID.py RES_ID
```
### Example: 

```bash
python3 generateModel_RES_ID.py 011d2088-3ed5-488f-9863-42c2ba2fa3ea
```

### Output: 
```
<Resource Name>.yml
```

### Methodology:
The code contains 4 lists which are used to generate the yml file.

```python
    primary_contains = ["id"]
    temporal_contains = ["date", "time", "year",
                         "month", "day", "hour", "minute", "second"]
    ordinal_dtypes_contains = ["int", "float", "double"]
    ordinal_ignore = ["code"]
```

the details of each list is as follows:

1. **primary_contains**: This list contains the column names which are primary keys in the table. The script will automatically detect the primary keys and add them to the list. 
2. **temporal_contains**: This list contains the column names which are temporal in nature. The script will automatically detect the temporal columns and add them to the list.
3. **ordinal_dtypes_contains**: This list contains the column names which are of ordinal data type. The script will automatically detect the ordinal columns and add them to the list.
4. **ordinal_ignore**: This list contains the column names which are of ordinal data type but are not to be considered as ordinal. The script will automatically detect the ordinal columns and add them to the list.

## Action - Create Model

### Usage: 

```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/bippisb/store2cube/actions/workflows/createModel.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "res_id": <RES_ID>
    }
  }'

```