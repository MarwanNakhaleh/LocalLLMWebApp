from flask import jsonify

def json_response(args: str, path: str, data: list, time: float):
    payload =  {
        "metadata": {
            "path": path,
            "query": args,
            "execution_time": time
        },
        "num_results": len(data),
        "results": data
    }
    return jsonify(payload)

def api_response(payload, endpoint, start=None, limit=None, status=200):
    if start and limit:
        payload = get_paginated_list(payload, endpoint, start, limit)
    return (payload, status, {'content-type': 'application/json'})

def get_paginated_list(results, url, start, limit):
    count = len(results["results"])
    if count < start or limit < 0:
        return results
    
    paginated_response = {}
    paginated_response['start'] = start
    paginated_response['limit'] = limit
    paginated_response['num_results'] = count
    paginated_response["metadata"] = results["metadata"]
    
    # starting from 1 for results insteaf of 0 for programming
    if start == 1:
        paginated_response['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        paginated_response['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    
    if start + limit > count:
        paginated_response['next'] = ''
    else:
        start_copy = start + limit
        paginated_response['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    
    paginated_response['results'] = results["results"][(start - 1):(start - 1 + limit)]
    return paginated_response