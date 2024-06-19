import re
def parse_filter_query(filter_query):
    conditions = re.split(' && ', filter_query, flags=re.IGNORECASE)
    parsed_conditions = []

    operator_mapping = {
        'scontains': 'LIKE',
        'sgt': '>',
        'slt': '<',
        'seq': '=',
        'sneq': '!='
    }

    for condition in conditions:
        column, operator, value = condition.split(' ')
        column = column[1:-1]  # remove the curly braces

        sql_operator = operator_mapping[operator]

        if operator == 'scontains':
            value = f"'%{value}%'"
        else:
            # Check if the value is numeric
            if value.isdigit():
                # If it's numeric, don't wrap it in quotes
                value = f"{value}"
            else:
                # If it's not numeric, wrap it in quotes
                value = f"'{value}'"

        parsed_conditions.append(f"{column} {sql_operator} {value}")

    return ' AND '.join(parsed_conditions)


filter_query="{name} scontains John && {id} sgt 5"
parsed_filter_query=parse_filter_query(filter_query)
print(f"filter_query: {filter_query}")
print(f"parsed_filter_query: {parsed_filter_query}")