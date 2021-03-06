from django.conf import settings
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')

        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Reticulate splines' + Keys.ENTER)
        self.get_item_input_box().send_keys('Immanentize eschaton' + Keys.ENTER)
        first_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()

        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.current_url, first_list_url))

        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Click cows' + Keys.ENTER)
        second_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()
        self.browser.find_element_by_link_text('Click cows').click()
        self.assertEqual(self.browser.current_url, second_list_url)

        self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(self.browser.find_elements_by_link_text('My lists'), [])
