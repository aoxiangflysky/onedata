"""Steps used in login page"""

from itertools import izip

from pytest_bdd import given, parsers
from pytest_selenium_multi.pytest_selenium_multi import select_browser

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import repeat_failed, parse_seq


__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


@given(parsers.parse('user of {browser_id_list} entered credentials for '
                     '{users_list} in login form'))
@given(parsers.parse('users of {browser_id_list} entered credentials for '
                     '{users_list} in login form'))
@repeat_failed(timeout=WAIT_FRONTEND)
def g_enter_user_credentials_to_login_form(selenium, browser_id_list,
                                           users_list, users, login_page):
    for browser_id, username in izip(parse_seq(browser_id_list),
                                     parse_seq(users_list)):
        login = login_page(select_browser(selenium, browser_id))
        login.username = username
        login.password = users[username]


@given(parsers.parse('user of {browser_id_list} pressed Sign in button'))
@given(parsers.parse('users of {browser_id_list} pressed Sign in button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def g_press_sign_in_btn_on_login_page(selenium, browser_id_list,
                                      users_list, login_page):
    for browser_id, username in izip(parse_seq(browser_id_list),
                                     parse_seq(users_list)):
        login_page(select_browser(selenium, browser_id)).sign_in()