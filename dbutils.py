import re
import logging

logger = logging.getLogger(__name__)
def parse_filter_query(filter_query):
    logging.info("START: parse_filter_query")
    conditions = re.split(' && ', filter_query, flags=re.IGNORECASE)
    parsed_conditions = []

    operator_mapping = {
        'scontains': 'LIKE',
        'sgt': '>',
        'slt': '<',
        'seq': '=',
        'sneq': '!=',
        '>': '>',
        '<': '<',
        '=': '=',
        '!=': '!=',
        'icontains':'ILIKE'
    }

    for condition in conditions:
        column, operator, value = condition.split(' ')
        column = column[1:-1]  # remove the curly braces

        #sql_operator = operator_mapping[operator]
        sql_operator = operator_mapping.get(operator)
        if sql_operator is None and operator[0] == 's':
            sql_operator = operator_mapping.get(operator[1:])

        if sql_operator is None:
            raise ValueError(f"Invalid operator: {operator}")

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


#filter_query="{name} scontains John && {id} sgt 5"
#filter_query="{id} s> 4"
#parsed_filter_query=parse_filter_query(filter_query)
#logger.info(f"filter_query: {filter_query}")
#logger.info(f"parsed_filter_query: {parsed_filter_query}")