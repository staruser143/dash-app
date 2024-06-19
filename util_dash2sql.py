import re
# Function to parse filter query
def parse_filter_query(filter_query):
    print(f"Start: parse_filter_query")
    print(f"filter_query: {filter_query}")

    if not filter_query:
        return {"filters": [], "logic": "AND"}
    
    filter_query = filter_query.strip().lstrip('{').rstrip('}')
    conditions = re.split(r' (&| \|) ', filter_query)
    
    parsed_filters = []
    for condition in conditions:
        match = re.match(r'({[^}]+}) (==|!=|>|>=|<|<=|in|not in|contains|not contains|sgt|sge|slt|sle) (.+)', condition)
        if match:
            column = match.group(1).strip('{}')
            operator = match.group(2)
            value = match.group(3).strip('"')
            parsed_filters.append({"column_id": column, "operator": operator, "value": value})
    
    logic = 'AND' if ' & ' in filter_query else 'OR'
    
    print(f"parsed_filters: {parsed_filters}")  
    print(f"logic: {logic}")
    print(f"End: parse_filter_query")
    return {"filters": parsed_filters, "logic": logic}

# Function to convert parsed filters to SQL
def convert_dash_filter_to_sql(dash_filter):
    print(f"Start: convert_dash_filter_to_sql")
    print(f"dash_filter: {dash_filter}")

    operators_map = {
        "==": "=",
        "!=": "!=",
        ">": ">",
        ">=": ">=",
        "<": "<",
        "<=": "<=",
        "in": "IN",
        "not in": "NOT IN",
        "contains": "LIKE",
        "not contains": "NOT LIKE",
        "sgt": ">",
        "sge": ">=",
        "slt": "<",
        "sle": "<="
    }

    conditions = []
    for filter in dash_filter["filters"]:
        column = filter["column_id"]
        operator = operators_map[filter["operator"]]
        value = filter["value"]

        if operator in ["LIKE", "NOT LIKE"]:
            value = f"'%{value}%'"
        elif operator in ["IN", "NOT IN"]:
            value = f"({value})"
        else:
            value = f"'{value}'" if isinstance(value, str) else value

        condition = f"{column} {operator} {value}"
        conditions.append(condition)

    logic = dash_filter["logic"]
    where_clause = f" {logic} ".join(conditions) if conditions else "1=1"
  
    print(f"where_clause: {where_clause}")
    print(f"End: convert_dash_filter_to_sql")
    return where_clause


print(parse_filter_query("{name} scontains White"))