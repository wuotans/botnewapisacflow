import logging
import time
from priority_classes.decorators.decorators import time_out
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from priority_classes.ssw.ssw import SswRequest
from priority_classes.ssw.ssw_v2 import SswRequest as sv2


class Ssw520(SswRequest):
    def __init__(self):
        super().__init__()

    def _op520_click_emit_subs(self):
        script="""
        ajaxEnvia('', 1, 'ssw0011?act=SUB');return false;
        """
        self.driver.execute_script(script)
    @time_out(3)
    def _op520_write_sigla(self,**kwargs):
        script=f"""
        document.getElementById('1').value='{kwargs['sigla']}'
        """
        self.driver.execute_script(script)

    @time_out(3)
    def _op520_write_nro(self,**kwargs):
        script=f"""
        document.getElementById('2').value='{kwargs['nro']}'
        """
        self.driver.execute_script(script)

    def _op520_click_submit_ctrc(self,**kwargs):
        script = """
        ajaxEnvia('PES', 0);return false;
        """
        self.driver.execute_script(script)
    @time_out(3)
    def _op520_write_conferente(self,**kwargs):
        script = f"""
        document.getElementById('15').value='{kwargs['conferente']}'
        """
        self.driver.execute_script(script)

    def _op520_click_submit_substitute(self,**kwargs):
        script = """
        calculafrete(this);return false;
        """
        self.driver.execute_script(script)
    @time_out()
    def _op520_send_order(self,**kwargs):
        script = f"""
        document.getElementById('errormsglabel').querySelector('input').value='{kwargs['order']}'
        """
        self.driver.execute_script(script)

    @time_out()
    def _op520_click_send_order(self):
        script = f"""
        document.getElementById('0').click()
        """
        self.driver.execute_script(script)
    @time_out()
    def _op520_skip_email(self,**kwargs):
        script = """
        goEmailPagPassa();
        """
        self.driver.execute_script(script)

    @time_out()
    def _op520_save_substitute(self,**kwargs):
        try:
            script = """
            concluindo('C');
            """
            self.driver.execute_script(script)
        except Exception as e:
            logging.exception(e)
            script = """
            continuaResumo();
            """
            self.driver.execute_script(script)
            raise  e

    @time_out()
    def _op520_click_and_edit_receb(self,**kwargs):
        script = f"""
        document.getElementById('lnk_tela_receb').click()
        return document.getElementById('receb')
        """
        receb = self.driver.execute_script(script)
        if not receb.is_displayed():
            raise Exception('Element not found')
        else:
            script = f"""
            document.getElementById('fld_cgc_receb').value=document.getElementById('id_cli_des_cnpj').value
            return document.getElementById('lnk_receb_env')
            """
            play = self.driver.execute_script(script)
            play.click()


    @time_out()
    def _op520_click_and_edit_loc_cep(self,**kwargs):
        script = f"""
        document.getElementById('lnk_cep_calculo').click()
        return document.getElementById('errormsg')
        """
        warn = self.driver.execute_script(script)
        if not warn.is_displayed():
            raise Exception('Element not found')
        else:
            script = f"""
            return document.getElementById('-1')
            """
            city = self.driver.execute_script(script)
            city.click()
            logging.info(kwargs["loc_delivery"])
            city.send_keys(kwargs["loc_delivery"],Keys.ENTER)


    @time_out()
    def _op520_edit_cep(self,**kwargs):
        # ceps = self.get_cep_from_ssw_for_city_name(kwargs["loc_delivery"])
        # rows = ceps['rs']['r']
        # if isinstance(rows,list):
        #     cep = [cep['c'] for cep in rows if cep['n']==kwargs["loc_delivery"]][0]
        # else:
        cep =  kwargs['cep']
        logging.info(cep)
        script = f"""
        document.getElementById('fld_cep_entrega').value='{cep}'
        """
        self.driver.execute_script(script)

    @time_out()
    def _op520_click_expedidor(self,**kwargs):
        script = """
        document.getElementById('lnk_exped').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _op520_edit_cep_expedidor(self,**kwargs):
        script = f"""
        document.getElementById('id_cli_exp_cep_ori').click()
        document.getElementById('id_cli_exp_cep_ori').value='{kwargs['cep_exped']}'
        dadosCepOri();
        document.getElementById('lnk_exped_env').click()
        """
        self.driver.execute_script(script)

    def _op520_(self,**kwargs):
        script = """

        """
        self.driver.execute_script(script)
        
    def _op520_emit_substitute(self,**kwargs):
        self.driver.get("https://sistema.ssw.inf.br/bin/ssw0011")
        self._op520_click_emit_subs()
        self.next_window(1)
        self._op520_write_sigla(**kwargs)
        self._op520_write_nro(**kwargs)
        self._op520_click_submit_ctrc()
        self._op520_write_conferente(**kwargs)
        self._op520_click_and_edit_receb(**kwargs)
        self._op520_click_expedidor()
        self._op520_edit_cep_expedidor(**kwargs)
        self._op520_edit_cep(**kwargs)
        self._op520_click_submit_substitute()
        #self._op520_send_order(**kwargs)
        #self._op520_click_send_order()
        #self._op520_skip_email()
        self._op520_save_substitute()
        #input()


    def op520(self, *args, **kwargs):
        """
        Perform the ssw520 operation.
        :param args: 'emit_substitute'
        :param kwargs:
            - sigla: the first 3 digits from ctrc code.
            - nro: the last numbers from ctrc code.
            - conferente: the number associate to the conferente name.
            - loc_delivery: The loc_delivery address
            - cep: cep

        :return: None
        """
        self.last_opssw = '520'

        if 'emit_substitute' in args:
            self._op520_emit_substitute(**kwargs)



if __name__ == '__main__':
    with sv2() as ssw:
        ssw.get_cep_from_ssw_for_city_name('AMAMBAI')
