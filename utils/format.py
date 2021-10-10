def format_to_psql_array(data):
    result = []
    for i in data:
        base = '{"' + '","'.join(i) + '"}'
        result.append(base)
    result = '{' + ','.join(result) + '}'
    return result
