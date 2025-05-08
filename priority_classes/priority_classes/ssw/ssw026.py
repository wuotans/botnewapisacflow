from priority_classes.decorators.decorators import time_out
from priority_classes.ssw.ssw import SswRequest
import time
import logging

class Ssw026(SswRequest):
    def __init__(self):
        super().__init__()

    @time_out()
    def _op026_search_vehicle(self, plate):
        script = f"""
        document.getElementById('2').value = '{plate}'
        document.getElementById('3').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_change_infos(self, **kwargs):
        script = f"""
        document.getElementById('marca_veic').value='{kwargs['marca_veic']}'
        document.getElementById('tp_carroceria').value='{kwargs['tp_carroceria']}'
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_click_more_trackers(self, **kwargs):
        script = f"""
        var tracker = document.getElementById('fg_rastreador')
        tracker.value = tracker.value = '{kwargs["rastreador_nome"]}' != '' ? tracker.value: 'N'
        document.getElementById('link_mais_rastreador').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_update_tracker_values(self, **kwargs):
        script = f"""
        document.getElementById('1').value='{kwargs['rastreador_nome']}'
        document.getElementById('2').value='{kwargs['rastreador_id']}'
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_click_save_trackers(self):
        script = """
        document.getElementById('5').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_click_risk_manager(self):
        script = """
        document.getElementById('link_demais').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_update_risk_manager(self, num):
        script = f"""
        document.getElementById('cod_gen_risco').value = '{num}'
        document.getElementById('link_env').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_click_save(self):
        script = """
        document.getElementById('btn_env').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_click_ask_authorization_gr(self):
        script = """
        document.getElementById('link_solic_aut_gr').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op026_model(self):
        script = """

        """
        self.driver.execute_script(script)

    def _op026_update_info_vehicles(self, **kwargs):
        url = "https://sistema.ssw.inf.br/bin/ssw0019"
        self.driver.get(url)
        self._op026_search_vehicle(kwargs['f2'])
        self.next_window(1)
        self._op026_change_infos(**kwargs)
        self._op026_click_more_trackers(**kwargs)
        self.next_window(2)
        self._op026_update_tracker_values(**kwargs)
        self._op026_click_save_trackers()
        self.driver.close()
        self.next_window(1)
        self._op026_click_risk_manager()
        self.next_window(2)
        self._op026_update_risk_manager(5)
        time.sleep(1)
        warnings = self._confirm_all_warnings(0)
        logging.info(warnings)
        self.next_window(1)
        self._op026_click_save()
        time.sleep(1)
        warnings += self._confirm_all_warnings(0)
        self.next_window(0)
        warnings += [self._wait_to_confirm_warning(0)]
        return warnings

    def _op026_ask_authorization_gr(self, **kwargs):
        url = "https://sistema.ssw.inf.br/bin/ssw0019"
        self.driver.get(url)
        self._op026_search_vehicle(kwargs['f2'])
        self.next_window(1)
        self._op026_click_ask_authorization_gr()
        warnings = [str(self._wait_to_confirm_warning(-1))]
        logging.info(warnings)
        if 'pesquisa' in ''.join(warnings).lower():
            warnings += [str(self._wait_to_confirm_warning(0))]
        self.next_window(0)
        logging.info(warnings)
        return '|'.join(warnings)

    def _op026_get_info(self, html_text, **kwargs):
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'P'
        query_model = "act=P&f2=BPS6B62&2a_vez=1&dummy=1699628522666"
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0019", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        return response.text

    def op026(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '026'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0019", headers=self.headers, data=data)

        # showing results
        html_text = response.text
        logging.info(html_text)

        if 'get_info' in args:
            return self._op026_get_info(html_text, **kwargs)
        if 'update_info' in args:
            return self._op026_update_info_vehicles(**kwargs)
        if 'ask_authorization_gr' in args:
            return self._op026_ask_authorization_gr(**kwargs)


if __name__ == '__main__':
    with Ssw026() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op026()
