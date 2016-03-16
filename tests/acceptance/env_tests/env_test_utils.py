import sys
import socket
from tests import test_utils


def check_appmock_up(env, dockers_num):
    key = 'appmock_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)
    # Check connectivity to nodes using the DNS
    # node is in form name@name.timestamp.dev.docker
    for node in env[key]:
        (name, sep, hostname) = node.partition('@')
        ip = test_utils.dns_lookup(hostname, dns)
        assert test_utils.ping(ip)
        assert test_utils.check_http_connectivity(ip, 443, '/test2', 200,
                                                  number_of_retries=50)


def check_client_up(env, dockers_num):
    key = 'client_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)
    # Check client nodes
    # oc_node is in form name.timestamp.dev.docker
    for oc_node in env[key]:
        oc_ip = test_utils.dns_lookup(oc_node, dns)
        assert test_utils.ping(oc_ip)


def check_cluster_manager_up(env, dockers_num):
    key = 'cluster_manager_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)
    # Check connectivity to nodes using the DNS
    # Check OP CM nodes
    # cm_node is in form name@name.timestamp.dev.docker
    for cm_node in env[key]:
        (cm_name, sep, cm_hostname) = cm_node.partition('@')
        cm_ip = test_utils.dns_lookup(cm_hostname, dns)
        assert test_utils.ping(cm_ip)


def check_cluster_up(env, dockers_num):
    check_cluster_manager_up(env, dockers_num['cm_nodes'])
    check_cluster_worker_up(env, dockers_num['cw_nodes'])


def check_cluster_worker_up(env, dockers_num):
    key = 'op_worker_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)
    for node in env[key]:
        (name, sep, hostname) = node.partition('@')
        ip = test_utils.dns_lookup(hostname, dns)
        assert test_utils.ping(ip)
        assert test_utils.check_http_connectivity(ip, 6666, '/nagios', 200,
                                                  use_ssl=False,
                                                  number_of_retries=50)


def check_onezone_up(env, dockers_num):
    key = 'oz_worker_nodes'
    print "ENV: ", env
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)
    # Check connectivity to nodes using the DNS
    # Check OZ nodes
    # oz_node is in form name@name.timestamp.dev.docker
    for oz_node in env[key]:
        (oz_name, sep, oz_hostname) = oz_node.partition('@')
        oz_ip = test_utils.dns_lookup(oz_hostname, dns)
        assert test_utils.ping(oz_ip)
        assert test_utils.check_http_connectivity(oz_ip, 443, '/', 200,
                                                  number_of_retries=50)

    # Check OZ DB nodes
    # oz_db_node is in form name@name.timestamp.dev.docker
    for oz_db_node in env['oz_db_nodes']:
        (oz_db_name, sep, oz_db_hostname) = oz_db_node.partition('@')
        oz_db_ip = test_utils.dns_lookup(oz_db_hostname, dns)
        assert test_utils.ping(oz_db_ip)
        assert test_utils.check_http_connectivity(oz_db_ip, 5984, '/_utils/',
                                                  200, use_ssl=False,
                                                  number_of_retries=50)


def check_provider_up(env, dockers_num):
    check_cluster_manager_up(env, dockers_num['cm_nodes'])
    check_provider_worker_up(env, dockers_num['op_worker'])


def check_provider_worker_up(env, dockers_num):
    key = 'op_worker_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)
    for w_node in env[key]:
        (w_name, sep, w_hostname) = w_node.partition('@')
        w_ip = test_utils.dns_lookup(w_hostname, dns)
        assert test_utils.ping(w_ip)
        assert test_utils.check_http_connectivity(w_ip, 6666, '/nagios', 200,
                                                  use_ssl=False,
                                                  number_of_retries=50)


def check_riak_up(env, dockers_num):
    key = 'riak_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)
    for node in env[key]:
        ip = test_utils.dns_lookup(node, dns)
        assert test_utils.ping(ip)


def check_couchbase_up(env, dockers_num):
    key = 'couchbase_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)

    for node in env[key]:
        ip = test_utils.dns_lookup(node, dns)
        assert test_utils.ping(ip)


def check_panel_up(env, dockers_num):
    key = 'onepanel_nodes'
    assert dockers_num == len(env[key])
    dns = env['dns']
    # Will throw if the dns address is not legal
    socket.inet_aton(dns)

    for node in env[key]:
        (name, sep, hostname) = node.partition('@')
        ip = test_utils.dns_lookup(hostname, dns)
        assert test_utils.ping(ip)


def get_module(name):
    return sys.modules[name]


def get_function(function_name):
    return getattr(get_module(__name__), function_name)