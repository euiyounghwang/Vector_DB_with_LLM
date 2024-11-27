
import json

def response_payload_transform(diff):
    response = {}
    if not diff:
        response.update({'diff' : 'Same mapping'})
    else:
        response.update({'diff' : 'Different mapping', 'result' : diff})

    return response


def make_port(source_host):
    ''' make port if it doesn't exist'''
    if str(source_host).replace("http://", "").__contains__(":"):
        return source_host
    else:
        return str(source_host)+":9200"


def source_hosts_with_http(source_hosts_list):
    ''' split string source host with "," to list'''
    transform_source_hosts = []
    for source_host in source_hosts_list: 
        '''
        if not str(source_host).strip().startswith("http://"):
            transform_source_hosts.append(make_port("http://{}".format(str(source_host).replace(" ", ""))))
        else:
            transform_source_hosts.append(make_port(str(source_host).replace(" ", "")))
        '''
        transform_source_hosts.append(make_port(str(source_host).replace(" ", "")))

    print('source_hosts_with_http - ', json.dumps(transform_source_hosts, indent=2))
    return transform_source_hosts


def generate_es_host(hosts, es_host):
    ''' getnerateo es_host list by splitting |'''
    print(source_hosts_with_http(hosts.get(es_host).split("|")))
    return  source_hosts_with_http(hosts.get(es_host).split("|"))

