"""Test suite for tests using oneclient and browser
"""
__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from pytest_bdd import scenarios, scenario

from tests.acceptance.steps.env_steps import *
from tests.acceptance.steps.auth_steps import *
from tests.acceptance.steps.dir_steps import *
from tests.acceptance.steps.file_steps import *
from tests.acceptance.steps.reg_file_steps import *
from tests.utils.acceptance_utils import *

from tests.gui.steps.common import *
from tests.gui.steps.modal import *

from tests.gui.steps.generic.url import *
from tests.gui.steps.generic.browser_creation import *
from tests.gui.steps.generic.copy_paste import *

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_alias import *
from tests.gui.steps.onezone.access_tokens import *
from tests.gui.steps.onezone.data_space_management import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *

from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *

from tests.gui.steps.oneservices.cdmi import *

from tests.gui.steps.onezone_before_login import *
from tests.gui.steps.onezone_provider_popup import *
from tests.gui.steps.onezone_providers import *

from tests.gui.steps.oneprovider_common import *
from tests.gui.steps.oneprovider_data import *
from tests.gui.steps.oneprovider_spaces import *
from tests.gui.steps.oneprovider_shares import *
from tests.gui.steps.oneprovider_metadata import *
from tests.gui.steps.oneprovider_file_list import *
from tests.gui.steps.oneprovider_sidebar_list import *


@pytest.mark.xfail(reason="Timestamps does not change during renaming "
                          "file using GUI, VFS-3520")
@scenario('../features/oneprovider_files.feature',
          'User renames file using browser and using oneclient he sees that '
          'status-change time has changed')
def test_rename_file_using_browser_and_check_timestamps_using_client():
    pass


@pytest.mark.xfail(reason="Cannot recreate file in oneclient after deleting it"
                          "in browser.")
@scenario('../features/oneprovider_files.feature',
          'User creates file using oneclient, removes it using browser and then'
          ' recreates it using oneclient')
def test_recreate_file_using_oneclient_deleted_using_browser():
    pass


scenarios('../features/oneprovider_files.feature')