"""Steps for features of Oneprovider's spaces.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import parsers, then
from tests.gui.steps.common import find_element_by_css_selector_and_text
from selenium.webdriver.support.ui import WebDriverWait as Wait
from tests.gui.conftest import WAIT_FRONTEND

from pytest_selenium_multi.pytest_selenium_multi import select_browser


@then(parsers.parse('user of {browser_id} sees that home space icon '
                    'has appeared next to displayed '
                    'name of space "{space_name}" in spaces list'))
def check_if_home_space_icon_next_to_spaces(selenium, browser_id, space_name):

    def _find_home_space_icon(s):
        spaces = s.find_elements_by_css_selector('.ember-view ul.spaces-list '
                                                 '.secondary-sidebar-item')
        for elem in spaces:
            if elem.find_element_by_css_selector('span.oneicon-space-home'):
                return elem
        return None

    driver = select_browser(selenium, browser_id)
    assert _find_home_space_icon(driver).text == space_name


@then(parsers.parse('user of {browser_id} sees that submenu for space '
                    'named "{space_name}" has appeared'))
def check_if_displayed_space_menu(selenium, browser_id, space_name):
    driver = select_browser(selenium, browser_id)
    space = find_element_by_css_selector_and_text('li.active .secondary-sidebar-item .truncate',
                                                  space_name)
    Wait(driver, WAIT_FRONTEND).until(space)