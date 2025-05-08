from priority_classes.decorators.decorators import time_out
from priority_classes.ssw.ssw import SswRequest, TryAgain
import time
import logging

class Ssw028(SswRequest):
    def __init__(self):
        super().__init__()

    @time_out()
    def _op028_search_driver(self, cpf):
        script = f"""
        document.getElementById('2').value = '{cpf}'
        document.getElementById('3').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op028_update_contacts(self, ddd, fone, contact, relative):
        script = f"""
        var ddd_fix = document.getElementById('10')
        var fone_fix = document.getElementById('11')
        var ddd_pri1 = document.getElementById('23')
        var fone_pri1 = document.getElementById('24')
        var contact_pri1 = document.getElementById('25')
        var relative_pri1 = document.getElementById('26')
        var ddd_pri2 = document.getElementById('27')
        var fone_pri2 = document.getElementById('28')
        var contact_pri2 = document.getElementById('29')
        var relative_pri2 = document.getElementById('30')
        var ddd_pri3 = document.getElementById('31')
        var fone_pri3 = document.getElementById('32')
        var contact_pri3 = document.getElementById('33')
        var relative_pri3 = document.getElementById('34')


        ddd_fix.value = ddd_fix.value = ddd_fix.value != '' ? ddd_fix.value: '{ddd}'
        fone_fix.value = fone_fix.value = fone_fix.value != '' ? fone_fix.value: '{fone}'
        ddd_pri1.value = ddd_pri1.value = ddd_pri1.value != '' ? ddd_pri1.value: '{ddd}'
        fone_pri1.value = fone_pri1.value = fone_pri1.value != '' ? fone_pri1.value: '{fone}'
        contact_pri1.value = contact_pri1.value = contact_pri1.value != '' ? contact_pri1.value: '{contact}'
        relative_pri1.value = relative_pri1.value = relative_pri1.value != '' ? relative_pri1.value: '{relative}'
        ddd_pri2.value = ddd_pri2.value = ddd_pri2.value != '' ? ddd_pri2.value: '{ddd}'
        fone_pri2.value = fone_pri2.value = fone_pri2.value != '' ? fone_pri2.value: '{fone}'
        contact_pri2.value = contact_pri2.value = contact_pri2.value != '' ? contact_pri2.value: '{contact}'
        relative_pri2.value = relative_pri2.value = relative_pri2.value != '' ? relative_pri2.value: '{relative}'
        ddd_pri3.value = ddd_pri3.value = ddd_pri3.value != '' ? ddd_pri3.value: '{ddd}'
        fone_pri3.value = fone_pri3.value = fone_pri3.value != '' ? fone_pri3.value: '{fone}'
        contact_pri3.value = contact_pri3.value = contact_pri3.value != '' ? contact_pri3.value: '{contact}'
        relative_pri3.value = relative_pri3.value = relative_pri3.value != '' ? relative_pri3.value: '{relative}'
        """
        self.driver.execute_script(script)

    @time_out()
    def _op028_click_risk_manager(self):
        script = f"""
        document.getElementById('66').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op028_update_risk_manager(self, num):
        script = f"""
        document.getElementById('2').value = '{num}'
        document.getElementById('10').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op028_click_save(self):
        script = f"""
        return document.getElementById('69')
        """
        self.driver.execute_script(script).click()

    @time_out(time_out=3, raise_exception=False)
    def _confirm_warning(self, id_):
        script = f"""
        var error = document.getElementById('errormsglabel')
        var innerText = error.innerText
        if (error){{
            document.getElementById('{id_}').click()
            return innerText
        }}
        """
        return self.driver.execute_script(script)

    @time_out(time_out=3, raise_exception=False)
    def _get_warning(self, id_):
        script = f"""
            var error = document.getElementById('errormsglabel')
            var innerText = error.innerText
            if (error){{
                return innerText
            }}
            """
        return self.driver.execute_script(script)

    @time_out()
    def _confirm_all_warnings(self, id_):
        results = []
        result = self._confirm_warning(id_)
        logging.info(result)
        while result is not None and result is not False:
            results.append(result)
            result = self._confirm_warning(id_)
            logging.info(result)
        return results

    @time_out()
    def _wait_to_confirm_warning(self, id_):
        result = self._get_warning(id_)
        if result is not None and result is not False:
            if not self._confirm_warning(id_):
                self._confirm_warning(0)
        else:
            raise TryAgain
        return result

    @time_out()
    def _op028_model(self):
        script = f"""

        """
        self.driver.execute_script(script)

    def _op028_update_info_drivers(self, **kwargs):
        url = 'https://sistema.ssw.inf.br/bin/ssw0021'
        self.driver.get(url)
        self._op028_search_driver(kwargs['f2'])
        self.next_window(1)
        self._op028_update_contacts(kwargs['ddd'], kwargs['fone'], kwargs['contact'], kwargs['relative'])
        self._op028_click_risk_manager()
        self.next_window(2)
        self._op028_update_risk_manager(5)
        time.sleep(1)
        warnings = self._confirm_all_warnings(0)
        logging.info(warnings)
        if warnings:
            self.next_window(1)
            self._op028_click_save()
            time.sleep(1)
            warnings += self._confirm_all_warnings(0)

        return warnings

    def _op028_click_ask_authorization_gr(self):
        script = """
        document.getElementById('75').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op028_change_relationship_transp(self):
        script = f"""
        document.getElementById('54').value='F'
        """
        self.driver.execute_script(script)

    def _op028_ask_authorization_gr(self, **kwargs):
        url = 'https://sistema.ssw.inf.br/bin/ssw0021'
        self.driver.get(url)
        self._op028_search_driver(kwargs['f2'])
        self.next_window(1)
        # time.sleep(2)
        self._op028_change_relationship_transp()
        self._op028_click_ask_authorization_gr()
        # time.sleep(2)
        warnings = [str(self._wait_to_confirm_warning(-1))]
        logging.info(warnings)
        if 'pesquisa' in ''.join(warnings).lower():
            warnings += [str(self._wait_to_confirm_warning(0))]
        self.next_window(0)
        return warnings

    def op028(self, *args, **kwargs):
        """
            :param args: 'update_info','get_info'
            :param kwargs:
            Possible keys include:
                - act:
                - f2: cpf motorista
                - ddd:
                - fone:
                - contact:
                - relative:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '028'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0021", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        if 'update_info' in args:
            return self._op028_update_info_drivers(**kwargs)
        if 'ask_authorization_gr' in args:
            return self._op028_ask_authorization_gr(**kwargs)
        if 'get_info' in args:
            # query filters to request record
            act = kwargs.pop('act') if 'act' in kwargs else 'PES'
            query_model = "act=PES&f2=78493749168&dummy=1699038579372"
            data = self.update_query_values(response.text, query_model, 'name', act=act, dummy=self.get_dummy(),
                                            **kwargs)
            logging.info(data)
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0021", headers=self.headers, data=data)

            # showing results

            logging.info(response.text)


if __name__ == '__main__':
    with Ssw028() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op028()
