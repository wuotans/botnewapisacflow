import os
import platform
from priority_classes.ssw.ssw import SswRequest
from priority_classes.ssw.ssw018 import Ssw018
import pytest
from pytest import mark
from selenium import webdriver


class TestClass:

    #@mark.skip('test')
    def test_chrome_driver_inicialization_if_is_instance_of_selenium_webdriver_chrome(self):
        entry_driver = 'chrome'
        entry_method = 'selenium'
        expected_driver = webdriver.Chrome

        test_ssw = SswRequest()
        test_ssw.init_browser(driver=entry_driver, method=entry_method)
        assert isinstance(test_ssw.driver, expected_driver)

    #@mark.skip('test')
    def test_edge_driver_inicialization_if_is_instance_of_selenium_webdriver_edge(self):
        entry_driver = 'edge'
        entry_method = 'selenium'
        expected_driver = webdriver.Edge

        test_ssw = SswRequest()
        test_ssw.init_browser(driver=entry_driver, method=entry_method)
        assert isinstance(test_ssw.driver, expected_driver)

    #@mark.skip('test')
    def test_login_ssw_if_is_user_logged_with_edge_selenium_driver(self):
        entry_driver = 'edge'
        entry_method = 'selenium'
        expected_url = 'https://sistema.ssw.inf.br/bin/menu01'

        test_ssw = SswRequest()
        test_ssw.init_browser(driver=entry_driver, method=entry_method)
        test_ssw.login()
        assert test_ssw.driver.current_url == expected_url

    #@mark.skip('test')
    def test_login_ssw_if_is_user_logged_with_chrome_selenium_driver(self):
        entry_driver = 'chrome'
        entry_method = 'selenium'
        expected_url = 'https://sistema.ssw.inf.br/bin/menu01'

        test_ssw = SswRequest()
        test_ssw.init_browser(driver=entry_driver, method=entry_method)
        test_ssw.login()
        assert test_ssw.driver.current_url == expected_url

    @mark.skip('test')
    def test_define_profile_path_if_is_test_path(self):
        entry_name_instace = 'teste'
        entry_system = platform.system()

        if entry_system == 'Windows':
            expected_profile_path_windows = os.path.abspath(os.path.join(os.path.dirname(os.getenv('APPDATA')),
                                                                         rf'profile_chrome\{entry_name_instace}'))
        elif entry_system == 'Linux':
            expected_profile_path_linux = f'bot_profile_chrome/{entry_name_instace}'

        test_ssw = SswRequest()
        test_profile_path = test_ssw.define_profile_path(entry_name_instace)

        if entry_system == 'Linux':
            assert test_profile_path == expected_profile_path_linux
        elif entry_system == 'Windows':
            assert test_profile_path == expected_profile_path_windows
        else:
            assert False

    #@mark.skip('test')
    def test_convert_query_url_to_dict_if_is_returning_json(self):
        entry_query = "act=NUM&f3=2659023&f6=V&f7=T&f8=T&f9=N&f17=280224&f18=280324&dummy=1711634275379"
        expected_json = {'act': '', 'f3': '', 'f6': '', 'f7': '', 'f8': '', 'f9': '', 'f17': '', 'f18': '', 'dummy': ''}

        test_ssw = SswRequest()
        test_json = test_ssw.convert_query_url_to_dict(entry_query)
        assert test_json == expected_json

    #@mark.skip('test')
    def test_convert_dict_to_query_url_if_is_returning_query(self):
        entry_json = {'act': '', 'f3': '', 'f6': '', 'f7': '', 'f8': '', 'f9': '', 'f17': '', 'f18': '', 'dummy': ''}
        expected_query = "act=&f3=&f6=&f7=&f8=&f9=&f17=&f18=&dummy="

        test_ssw = SswRequest()
        test_query = test_ssw.convert_dict_to_query_url(entry_json)
        assert test_query == expected_query

    #@mark.skip('test')
    def test_get_input_values_from_html_if_is_returning_json_ids(self):
        entry_html = """
        <input type="hidden" name="g_ctrc_ser_ctrc" id="g_ctrc_ser_ctrc" value="BOA">
        <input type="hidden" name="gw_gaiola_codigo" id="gw_gaiola_codigo" value="0">
        """
        expected_json = {'g_ctrc_ser_ctrc': 'BOA', 'gw_gaiola_codigo': '0'}

        test_ssw = SswRequest()
        test_params = test_ssw.get_input_values_from_html(entry_html)
        assert test_params == expected_json

    def test_update_query_values_if_is_returning_query_updated(self):
        entry_html = """
        <input type="hidden" name="g_ctrc_ser_ctrc" id="g_ctrc_ser_ctrc" value="BOA">
        <input type="hidden" name="gw_gaiola_codigo" id="gw_gaiola_codigo" value="0">
        """
        entry_query = "g_ctrc_ser_ctrc=&gw_gaiola_codigo=&f18=&dummy="
        expected_query = "g_ctrc_ser_ctrc=BOA&gw_gaiola_codigo=0&f18=&dummy=1716931746296"

        test_ssw = SswRequest()
        test_query = test_ssw.update_query_values(entry_html, entry_query, dummy='1716931746296')
        assert test_query == expected_query

    def test_get_table_if_is_returning_data(self):
        entry_html = """
        <xml id="xmlsr"><rs>
        <r><f0>PYY3H83</f0><f1>Descarregar ROMANEIO</f1><f2>CGB279623, CGB279797, CGB279828, CGB279878, CGB279885</f2></r>
        <r><f0>RAV2E47</f0><f1>Descarregar MANIFESTO</f1><f2>CWB030374</f2></r>
        </rs></xml>
        """
        expected_data = {'<f0>': {0: '', 1: 'PYY3H83', 2: 'RAV2E47'},
                         '<f1>': {0: '', 1: 'Descarregar ROMANEIO', 2: 'Descarregar MANIFESTO'},
                         '<f2>': {0: '', 1: 'CGB279623, CGB279797, CGB279828, CGB279878, CGB279885', 2: 'CWB030374'}}

        test_ssw = SswRequest()
        test_table = test_ssw.get_table(entry_html, 3)
        assert test_table.to_dict() == expected_data

    def test_extract_html_values_if_is_returning_extracted_val(self):
        entry_html = """
        <xml id="xmlsr"><rs>
        <r><f0>PYY3H83</f0><f1>Descarregar ROMANEIO</f1><f2>CGB279623, CGB279797, CGB279828, CGB279878, CGB279885</f2></r>
        <r><f0>RAV2E47</f0><f1>Descarregar MANIFESTO</f1><f2>CWB030374</f2></r>
        </rs></xml>
        """
        expected_data = 'PYY3H83'

        test_ssw = SswRequest()
        test_extracted = test_ssw.extract_html_values(entry_html, '<f0>','</f0>')
        assert test_extracted == expected_data
