"""Common steps used in various GUI testing scenarios
"""

__author__ = "Jakub Liput"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import re
import time
import random

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from tests.utils.acceptance_utils import list_parser
from tests.gui.utils.generic import parse_url
from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as Wait

from ..utils.generic import enter_text


@given('user generates valid name string')
def name_string():
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    return ''.join(random.sample(chars, 6))


@when(parsers.parse('user should see that the page title contains "{text}"'))
@then(parsers.parse('user should see that the page title contains "{text}"'))
def title_contains(selenium, text):
    Wait(selenium, WAIT_FRONTEND).until(
        EC.title_contains(text),
        message='seeing that page title contains {:s}'.format(text)
    )


@when('user types given name on keyboard')
@then('user types given name on keyboard')
def type_valid_name_string_into_active_element(selenium, name_string):
    Wait(selenium, WAIT_FRONTEND).until(
        lambda s: enter_text(s.switch_to.active_element, name_string),
        message='entering {:s} to input box'.format(name_string)
    )


@when(parsers.parse('user types "{text}" on keyboard'))
@then(parsers.parse('user types "{text}" on keyboard'))
def type_string_into_active_element(selenium, text):
    Wait(selenium, WAIT_FRONTEND).until(
        lambda s: enter_text(s.switch_to.active_element, text),
        message='entering {:s} to input box'.format(text)
    )


@when(parsers.parse('user presses enter on keyboard'))
@then(parsers.parse('user presses enter on keyboard'))
def press_enter_on_active_element(selenium):
    selenium.switch_to.active_element.send_keys(Keys.RETURN)


@when(parsers.parse('user presses backspace on keyboard'))
@then(parsers.parse('user presses backspace on keyboard'))
def press_enter_on_active_element(selenium):
    selenium.switch_to.active_element.send_keys(Keys.BACKSPACE)


@then(parsers.parse('user should see {links_names} links'))
def link_with_text_present(selenium, links_names):
    for name in list_parser(links_names):
        assert selenium.find_element_by_link_text(name)


def _click_on_link_with_text(selenium, link_name):
    selenium.find_element_by_link_text(link_name).click()


@given(parsers.parse('user clicks on the "{link_name}" link'))
def g_click_on_link_with_text(selenium, link_name):
    _click_on_link_with_text(selenium, link_name)


@when(parsers.parse('user clicks on the "{link_name}" link'))
def w_click_on_link_with_text(selenium, link_name):
    _click_on_link_with_text(selenium, link_name)


@when(parsers.parse('user is idle for {seconds:d} seconds'))
def wait_n_seconds(seconds):
    time.sleep(seconds)


@when(parsers.re(r'user changes the relative URL to (?P<path>.+)'))
def visit_relative(selenium, path):
    selenium.get(parse_url(selenium.current_url).group('base_url') + path)


@then(parsers.parse('user should see a page with "{text}" header'))
def page_with_header(selenium, text):

    def header_with_text_presence(s):
        headers = s.find_elements_by_css_selector('h1, h2, h3, h4, h5')
        try:
            return any(map(lambda h: h.text == text, headers))
        except StaleElementReferenceException:
            return False

    Wait(selenium, WAIT_BACKEND).until(header_with_text_presence)


@when(parsers.parse('user sees an {notify_type} notify with text matching to: {text_regexp}'))
@then(parsers.parse('user sees an {notify_type} notify with text matching to: {text_regexp}'))
def notify_visible_with_text(selenium, notify_type, text_regexp):
    text_regexp = re.compile(text_regexp)

    def notify_with_text_present(s):
        try:
            notifiers = s.find_elements_by_css_selector(
                '.ember-notify.ember-notify-show.{t} .message'.format(t=notify_type)
            )
            if len(notifiers) > 0:
                matching_elements = [e for e in notifiers if text_regexp.match(e.text)]
                return len(matching_elements) > 0
            else:
                return None
        except NoSuchElementException:
            return None

    Wait(selenium, 2*WAIT_BACKEND).until(notify_with_text_present)


@when('user can see current url')
def get_current_url(selenium, get_url):
    get_url = selenium.current_url


@then('user sees that url has changed')
def check_if_url_changed(selenium, get_url):
    assert selenium.current_url != get_url


@when('user refreshes site')
@then('user refreshes site')
def refresh_site(selenium):
    selenium.refresh()


def select_button_from_buttons_by_name(name, buttons_selector):
    def _go_to_button(s):
        buttons = s.find_elements_by_css_selector(buttons_selector)
        for button in buttons:
            if button.text.lower() == name.lower():
                Wait(s, WAIT_FRONTEND).until(
                    EC.visibility_of(button)
                )
                if button.is_enabled():
                    return button
    return _go_to_button


def find_element_by_css_selector_and_text(selector, text):
    """finds element on site by css selector and element's text"""
    def _find_element(s):
        elements_list = s.find_elements_by_css_selector(selector)
        for elem in elements_list:
            if elem.text.lower() == text.lower():
                return elem
    return _find_element


# Below functions are currently unused and should not be used,
# because it involves a knowledge about internals...


@when(parsers.re(r'user changes application path to (?P<path>.+)'))
def on_ember_path(selenium, path):
    selenium.get(parse_url(selenium.current_url).group('base_url') + '/#' + path)
