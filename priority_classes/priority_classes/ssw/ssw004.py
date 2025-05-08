import time
import logging
from priority_classes.ssw.ssw import SswRequest
from priority_classes.decorators.decorators import time_out
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote
import os
import json


class Ssw004(SswRequest):
    def __init__(self):
        super().__init__()
        self.action = ActionChains(self.driver)

    def _op004_(self,*args,**kwargs):
        script="""
        
        """
        self.driver.execute_script(script)
    @time_out()
    def _op004_click_normal_emission(self, *args, **kwargs):
        script = """
        ajaxEnvia('NORMAL', 1);return false;
        """
        self.driver.execute_script(script)

    @time_out()
    def _op004_post_plate(self, *args, **kwargs):
        script = f"""
        var plate = document.getElementById('13')
        return plate
        """
        plate = self.driver.execute_script(script)
        plate.send_keys(kwargs['plate'])
        plate.send_keys(Keys.ENTER)

    @time_out()
    def _op004_post_operator(self, *args, **kwargs):
        script = f"""
        var operator = document.getElementById('15');
        return operator
        """
        operator = self.driver.execute_script(script)
        operator.send_keys(kwargs['operator'])
        operator.send_keys(Keys.ENTER)

    @time_out()
    def _op004_post_nfe(self, *args, **kwargs):
        script = f"""
        var chaveAcesso = document.querySelector('input[name="chaveAcesso"]')
        return chaveAcesso
        """
        chaveAcesso = self.driver.execute_script(script)
        chaveAcesso.send_keys(kwargs['chave'])
        chaveAcesso.send_keys(Keys.ENTER)
        self._op004_wait_chave_acesso_hide()
    @time_out(raise_exception=False)
    def _op004_wait_chave_acesso_hide(self):
        script = f"""
        var parent = document.querySelector('#nfepnl');
        return parent.style.visibility ==='visible'
        """
        visibility = self.driver.execute_script(script)
        logging.info(visibility)
        if visibility:
            raise TimeoutError

    @time_out()
    def _op004_post_freight(self, *args, **kwargs):
        script = """
        var freight = document.getElementById('16');
        if (freight.value){
            console.log('Tem')
        }
        else{
            return freight
        }
        """
        freight = self.driver.execute_script(script)
        if freight is not None:
            logging.info('Alterando frete...')
            self.action.double_click(freight).perform()
            self.action.send_keys(Keys.BACK_SPACE).perform()
            self.action.move_to_element(freight).perform()
            self.action.click(freight).perform()
            self.action.send_keys(kwargs['freight']).perform()
    @time_out(5)
    def _op004_post_type_merc(self, *args, **kwargs):
        script = f"""
        var merc = document.getElementById('id_mercadoria');
        return merc
        """
        merc = self.driver.execute_script(script)
        self.action.double_click(merc).perform()
        self.action.send_keys(Keys.BACK_SPACE).perform()
        self.action.move_to_element(merc).perform()
        self.action.send_keys(kwargs['type_merc']).perform()
        self.action.click(merc).perform()
        if not self._op004_was_type_merc_change(*args, **kwargs):
            raise TimeoutError
    def _op004_was_type_merc_change(self, *args, **kwargs):
        script = """
        var merc = document.getElementById('id_mercadoria');
        return merc.value
        """
        merc_value = self.driver.execute_script(script)
        logging.info(merc_value,kwargs['type_merc'])
        if str(kwargs['type_merc']) == str(merc_value):
            return True
        else:
            return False
    @time_out()
    def _op004_post_weight(self, *args, **kwargs):
        script = f"""
        var weight = document.getElementById('id_peso_real');
        return weight
        """
        weight = self.driver.execute_script(script)
        self.action.double_click(weight).perform()
        self.action.send_keys(Keys.BACK_SPACE).perform()
        #self.action.send_keys(kwargs['weight']).perform()
        weight.send_keys(kwargs['weight'],Keys.ENTER)

    @time_out()
    def _op004_post_vols(self, *args, **kwargs):
        script = f"""
        var vol = document.getElementById('id_qtde_vol');
        vol.value = ''
        return vol
        """
        vol=self.driver.execute_script(script)
        self.action.double_click(vol).perform()
        self.action.send_keys(Keys.BACK_SPACE).perform()
        #self.action.send_keys(kwargs['vol']).perform()
        vol.send_keys(kwargs['vol'],Keys.ENTER)

    def _op004_download_obs(self, *args, **kwargs):
        parameters = self.convert_query_url_to_dict(unquote(self.get_all_type_input_values()),False)
        data = f"act=OBS0&notas={parameters['agrupamento']}&dummy={self.get_dummy()}"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0024", headers=self.headers, data=data)
        logging.info(response.text)
        if 'Observa&ccedil;&atilde;o da nota fiscal n&atilde;o encontrada.' not in response.text:
            self .handle_download(response.text)
            return   True

    def _op004_read_obs(self):
        with open(f'downloads/{os.listdir("downloads")[0]}','r') as f:
            logging.info(f.read())
    def _op004_click_emit(self, *args, **kwargs):
        script = """
        document.getElementById('lnk_env').click()
        """
        self.driver.execute_script(script)
    @time_out(5,raise_exception=False,verbose=True)
    def _op004_confirm_warnings(self, *args, **kwargs):
        script = """
        var scontentbar = document.getElementById('scontentbar')
        console.log(scontentbar.textContent)
        var warn = document.getElementById('errormsg')
        var text = warn.textContent
        console.log(text)
        warn.querySelectorAll('a[class="dialog"]').forEach(item=>{
            console.log(item.innerText.toLowerCase())
            if(item.innerText.toLowerCase().includes('continuar')||item.innerText.toLowerCase().includes('gravar')){
                console.log('clickando...')
                item.click()
            }
        })
        return text
        """
        text =self.driver.execute_script(script)
        logging.info(text)
        return True
    def _op004_confirm_all_warnings(self):
        conter=0
        while not self._op004_confirm_warnings() and conter <20:
            logging.info('Resolvendo warnings...')
            conter+=1
            time.sleep(1)


    def _op004_(self, *args, **kwargs):
        script = """

        """
        self.driver.execute_script(script)

    def _op004_normal_emission(self,*args, **kwargs):
        self.driver.get('https://sistema.ssw.inf.br/bin/ssw0024')
        self._op004_click_normal_emission()
        self.next_window(1)
        self._op004_post_plate(*args, **kwargs)
        self._op004_post_operator(*args, **kwargs)
        self._op004_post_nfe(*args, **kwargs)
        self._op004_post_freight(*args, **kwargs)
        self._op004_post_weight(*args, **kwargs)
        self._op004_post_vols(*args, **kwargs)
        self._op004_post_type_merc(*args, **kwargs)
        if self._op004_download_obs(*args, **kwargs):
            logging.info('Analisar nota de rodape')
            self._op004_read_obs()
            #self._op004_normal_emission_request()
        self._op004_click_emit()
        logging.info(kwargs)
        #self._op004_confirm_warnings()

    def _op004_normal_emission_request(self):
        parameters =self.get_all_type_input_values().split('null?')[1]
        logging.info(parameters)
        #data = f"act=OBS0&notas={parameters['agrupamento']}&dummy={self.get_dummy()}"
        #logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1600", headers=self.headers, data=parameters)
        logging.info(response.text)



    def op004(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '4'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0024", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self._op004_normal_emission(*args, **kwargs)
        input()





if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
