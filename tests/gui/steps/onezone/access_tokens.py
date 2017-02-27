"""Steps for access tokens features in Onezone login page.
"""

import pyperclip

from tests.gui.conftest import WAIT_BACKEND, SELENIUM_IMPLICIT_WAIT
from tests.gui.utils.generic import repeat_failed, implicit_wait

from pytest_bdd import when, then, parsers
from pytest_selenium_multi.pytest_selenium_multi import select_browser


__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


@when(parsers.re(r'user of (?P<browser_id>.*?) clicks on (?P<btn>copy|remove) '
                 r'icon for (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in expanded "ACCESS TOKENS" Onezone panel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) clicks on (?P<btn>copy|remove) '
                 r'icon for (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in expanded "ACCESS TOKENS" Onezone panel'))
def click_on_btn_for_oz_access_token(selenium, browser_id, btn, ordinal, oz_page):
    driver = select_browser(selenium, browser_id)

    @repeat_failed(attempts=WAIT_BACKEND, timeout=True)
    def click_on_btn(d, btn_name):
        token = oz_page(d)['access tokens'][int(ordinal[:-2]) - 1]
        action = getattr(token, btn_name)
        action()

    click_on_btn(driver, btn)


@when(parsers.re(r'user of (?P<browser_id>.+?) sees that token for '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in expanded "ACCESS TOKENS" Onezone '
                 r'panel has been copied correctly'))
@then(parsers.re(r'user of (?P<browser_id>.+?) sees that token for '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in expanded "ACCESS TOKENS" Onezone '
                 r'panel has been copied correctly'))
def assert_oz_access_token_has_been_copied_correctly(selenium, browser_id,
                                                     ordinal, oz_page):
    driver = select_browser(selenium, browser_id)
    panel = oz_page(driver)['access tokens']
    displayed_val = panel[int(ordinal[:-2]) - 1].value
    copied_val = pyperclip.paste()

    err_msg = 'Token has been copied incorrectly. ' \
              'Expected {}, got {}'
    assert displayed_val == copied_val, err_msg.format(displayed_val,
                                                       copied_val)


@when(parsers.parse('user of {browser_id} sees exactly {num:d} item(s) '
                    'on tokens list in expanded "ACCESS TOKENS" Onezone panel'))
@then(parsers.parse('user of {browser_id} sees exactly {num:d} item(s) '
                    'on tokens list in expanded "ACCESS TOKENS" Onezone panel'))
def assert_oz_access_tokens_list_has_num_tokens(selenium, browser_id,
                                                num, oz_page):
    driver = select_browser(selenium, browser_id)

    @repeat_failed(attempts=WAIT_BACKEND, timeout=True)
    def assert_quantity(d, quantity, msg):
        with implicit_wait(d, 0.1, SELENIUM_IMPLICIT_WAIT):
            displayed = oz_page(d)['access tokens'].tokens_count
            assert displayed == quantity, msg.format(seen=displayed,
                                                     excepted=quantity)

    err_msg = 'Displayed tokens in ACCESS TOKENS oz panel: {seen} ' \
              'instead of excepted: {excepted}'
    assert_quantity(driver, num, err_msg)