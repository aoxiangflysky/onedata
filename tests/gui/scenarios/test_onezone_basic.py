"""Test suite for features of Onezone login page.
"""
__author__ = "Jakub Liput, Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import pytest
from pytest_bdd import scenarios, scenario

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

from . import USING_BASE_URL


@pytest.fixture(scope='module')
def screens():
    return [0]


SKIP_REASON_BASE_URL = 'skipping test due to --base-url usage (external environment)'


@pytest.mark.skipif(USING_BASE_URL, reason=SKIP_REASON_BASE_URL)
@scenario('../features/onezone_gui.feature',
          'User sees that non working providers have gray icon in '
          '"GO TO YOR FILES" panel and appropriate msg is shown')
def test_user_sees_that_when_no_provider_is_working_appropriate_msg_is_shown():
    pass


scenarios('../features/onezone_login.feature')
scenarios('../features/onezone_gui.feature')
