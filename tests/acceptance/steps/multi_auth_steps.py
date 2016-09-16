"""Module implements pytest-bdd steps for authorization and mounting oneclient.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.utils.utils import get_function_name, handle_exception
from tests.utils.client_utils import ls, mount_users
from tests.utils.acceptance_utils import *

from pytest_bdd import given


@given(parsers.parse('{users} start oneclients {client_instances} in\n' +
                     '{mount_paths} on client_hosts\n' +
                     '{client_hosts} respectively,\n' +
                     'using {tokens}'))
def multi_mount(users, client_instances, mount_paths, client_hosts, tokens,
                request, onedata_environment, context, client_dockers,
                env_description_file, test_type, providers):
    mount_users(request, onedata_environment, context, client_dockers,
                env_description_file, test_type, providers,
                user_names=list_parser(users),
                client_instances=list_parser(client_instances),
                mount_paths=list_parser(mount_paths),
                client_hosts=list_parser(client_hosts),
                tokens=list_parser(tokens))


@then(parsers.parse('{spaces} are mounted for {user} on {client_nodes}'))
def check_spaces(spaces, user, client_nodes, context):
    spaces = list_parser(spaces)
    user = str(user)
    client_nodes = list_parser(client_nodes)
    function_name = get_function_name()

    for client_node in client_nodes:
        client = context.get_client(user, client_node)

        def condition():
            try:
                spaces_in_client = ls(client, path=client.mount_path)
                for space in spaces:
                    if space not in spaces_in_client:
                        return False
                    return True
            except Exception as e:
                handle_exception(e, function_name)
                return False

        assert client.perform(condition)


@when(parsers.parse('{user} remounts oneclient {client_node}'))
@then(parsers.parse('{user} remounts oneclient {client_node}'))
def remount_client(user, client_node, onedata_environment, context):
    user = context.get_user(user)
    client = user.get_client(client_node)
    assert client.remount(user) == 0