import logging

from priority_classes.ssw.ssw import SswRequest, EmptyValue
from priority_classes.decorators.decorators import time_out
import time


class Ssw475(SswRequest):
    def __init__(self):
        super().__init__()

    def _op475_available_to_schedule(self, html, **kwargs):
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'DISP'
        query_model = ("act=DISP&f1=S&sefaz=NF-e%20Disponivel&f3=MTZ&unidade3=CARVALIMA%20TRANSPORTES&f11=MTZ"
                       "&unidade11=CARVALIMA%20TRANSPORTES&f16=MTZ&unidade16=CARVALIMA%20TRANSPORTES&f17=160823&f18"
                       "=160823&f21=T&f22=V&f26=MTZ&unidade26=CARVALIMA%20TRANSPORTES&f27=160823&f28=160823&estorna"
                       "=&orig_dest=&dummy=1692191277130")
        data = self.update_query_values(html, query_model, 'name', act=act, dummy='1692191277130', **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0094", headers=self.headers, data=data)

        # showing results
        logging.info(response.text)
        table = self.get_table(response.text, 13)
        table.to_excel('ssw_475_indexes.xlsx')
        return table

    def _op475_danfes_download(self, *args, **kwargs):
        dict_infos_danfes = kwargs.pop('dict_infos_danfes')
        # &ger_xml=S param to get the file in xml format without it will get in .sswPrintDANFE
        ger_xml = kwargs.pop('ger_xml') if 'ger_xml' in kwargs else True
        if ger_xml:
            ger_xml = f'&ger_xml=S'
        else:
            ger_xml = ''
        for i, chave_nfe in enumerate(dict_infos_danfes['chave_nfe']):
            try:
                data = f"opcao=EXT&chave_nfe={chave_nfe}&serNF={dict_infos_danfes['serNF'][i]}&nroNF={dict_infos_danfes['nroNF'][i]}{ger_xml}&dummy=1687796390008&dummy=1687796390009"
                logging.info(data)

                response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1419", headers=self.headers, data=data)
                filename = dict_infos_danfes['chave_nfe'][i]
                name_file = filename if not 'name_file' in kwargs else kwargs.pop('name_file')

                self.direct_download(response.text, name_file)
            except Exception as e:
                logging.exception(e)

    @time_out()
    def _op475_post_unit_event(self, unit, event,cod_key):
        script = f"""
        document.getElementById('3').value='{unit}'
        document.getElementById('5').value='{event}'
        document.getElementById('chave_nfe').value='{cod_key}'
        ajaxEnvia('INC',1)
        """
        self.driver.execute_script(script)

    def load_cfops_to_ignore(self):
        return [
            '5949'
        ]

    @time_out()
    def _op475_post_cod_key(self, chave):
        script = f"""
        document.getElementsByName('chaveAcesso')[0].value='{chave}'
        isSSW('{chave}',1)
        """
        self.driver.execute_script(script)

    @time_out()
    def _op475_goto_change_products(self, cfop, data_venc, data_entry, hist):
        time.sleep(3)
        script = """
        var prd1 = document.getElementById('17').value
        var prd2 = document.getElementById('12').value
        console.log(prd1,prd2)
        return [prd1,prd2]
        """
        prd1, prd2 = self.driver.execute_script(script)
        logging.info(prd1, prd2)
        if prd1:
            script="""
            return document.getElementById('12').value
            """
            cfop_origin = self.driver.execute_script(script)
            if not str(cfop_origin).strip() in self.load_cfops_to_ignore():
                logging.info('alterando datas...')
                logging.info(data_entry,data_venc)
                script = f"""
                document.getElementById('17').value = '{data_entry}'
                document.getElementById('12').value = document.getElementById('12').value = document.getElementById('12').value != '' ? document.getElementById('12').value: '{cfop}'
                document.getElementById('34').value = '{data_venc}'
                document.getElementById('35').value = '{data_venc}'
                document.getElementById('36').value = '{data_venc[2:]}'
                document.getElementById('40').value = document.getElementById('40').value + '  NF ' + document.getElementById('5').value + '  {hist}'
                document.getElementById('37').value = document.getElementById('37').value != '' ? document.getElementById('37').value: document.getElementById('15').value
                ajaxEnvia('ITENS',1)
                """
                self.driver.execute_script(script)
        else:
            raise EmptyValue

    @time_out()
    def _op475_get_list_products(self):
        script = """
        var links = document.getElementsByTagName('u')
        var link_alt = []
        for (let i = 0;i<links.length;i++){
            var text = links[i].innerText
            console.log(text)
            if ('Alt'===text){
                console.log('Alterar',text)
                link_alt.push(links[i])
            }
        }
        return link_alt
        """
        return self.driver.execute_script(script)

    @time_out()
    def _op475_click_change_products(self):
        script = """
        document.getElementsByTagName('u')[1].click()
        """
        self.driver.execute_script(script)

    @time_out(time_out=3,raise_exception=False)
    def accept_alert(self):
        alerta = self.driver.switch_to.alert
        alerta.accept()

    @time_out(time_out=3)
    def _op475_wait_load_values(self):
        script = """
        var prd1 = document.getElementById('16').value
        var prd2 = document.getElementById('24').value
        var prd3 = document.getElementById('1').value
        console.log(prd1,prd2,prd3)
        return [prd1,prd2,prd3]
        """
        return self.driver.execute_script(script)

    @time_out(time_out=6)
    def _op475_change_values_products(self,**kwargs):
        #input()
        prd1, prd2,prd3 = self._op475_wait_load_values()
        prd1 = str(prd1).strip()
        prd2 = str(prd2).strip()
        prd3 = str(prd3).strip()
        logging.info(prd1, prd2,prd3)
        logging.info('icms_event: ',kwargs["icms_event"])
        if prd1 or prd2 or prd3:
            logging.info('Produtos carregados, alterando....')
            script = f"""
            document.getElementById('16').value='{kwargs["icms_event"]}'
            document.getElementById('24').value='3'
            
            if (document.getElementById('10').value === '1556' && document.getElementById('21').value !== '0,00' && document.getElementById('vlr_icms_st').value !== '0,00'){{
                document.getElementById('10').value = '1407'
            }}
            """
            self.driver.execute_script(script)
            #time.sleep(5)
            return True
        else:
            raise EmptyValue

    def _op475_apply_changes(self):
        script = """
        ajaxEnvia('INC_ITEM',1)
        //ajaxEnvia('FEC_ITEM',1)
        """
        self.driver.execute_script(script)
        self.accept_alert()

    @time_out(3)
    def _op475_process_changes_products(self,**kwargs):
        logging.info('#' * 20, 'clickando', '#' * 20)
        self._op475_click_change_products()
        logging.info('#' * 20, 'alterando', '#' * 20)
        if self._op475_change_values_products(**kwargs):
            logging.info('#' * 20, 'salvando', '#' * 20)
            self._op475_apply_changes()
            return True
        return False


    @time_out()
    def _op475_perform_changes_products(self,**kwargs):
        products = self._op475_get_list_products()
        results = []
        for product in products:
            results.append(self._op475_process_changes_products(**kwargs))
        return results

    @time_out()
    def _op475_click_save_throw(self):
        script = """
        document.getElementById('47').click()
        """
        self.driver.execute_script(script)

    def _op475_throw_cost(self, html, **kwargs):
        url = 'https://sistema.ssw.inf.br/bin/ssw0094'
        self.driver.get(url)
        self._op475_post_unit_event(kwargs['f3'], kwargs['f5'],kwargs['cd_barra'])
        self.next_window(1)
        time.sleep(1)
        #input()
        #self._op475_post_cod_key(kwargs['cd_barra'])
        self._op475_goto_change_products(kwargs['cfop'],
                                         kwargs['data_vencimento'],
                                         kwargs['data_entrada'],
                                         kwargs['historico'])
        self.next_window(2)
        results = self._op475_perform_changes_products(**kwargs)
        self.next_window(1)
        msg=''
        if results is not None and results and not False in results:
            logging.info(" Produtos alterados! Salvando lançamento")
            #input()
            self._op475_confirm_warning(0)
            #input()
            self._op475_click_save_throw()
            #input()
            msg = self._op475_confirm_warning(0)
            logging.info(msg)
            #input()
            if 'Data de Pagamento deve ser dia Útil. Será sugerido o próximo' in str(msg):
                logging.info('salvando novamente...')
                self._op475_click_save_throw()
                msg = self._op475_confirm_warning(0)
            self.next_window(0)

        return msg

        #

    @time_out()
    def _op475_post_unit_lanc(self, unit, num_lanc):
        script = f"""
        document.getElementById('11').value='{unit}'
        document.getElementById('12').value='{num_lanc}'
        document.getElementById('13').click()
        """
        self.driver.execute_script(script)

    @time_out(time_out=10)
    def _op475_cancel_lanc(self):
        script = """
            var prd1 = document.getElementById('chave_nfe_display').value
            return prd1
            """
        prd1 = self.driver.execute_script(script)
        if prd1:
            script = """
                document.getElementById('50').click()
                """
            self.driver.execute_script(script)
        else:
            raise EmptyValue

    @time_out(time_out=2, raise_exception=False)
    def _op475_confirm_warning(self, id):
        script = f"""
        var error = document.getElementById('errormsglabel')
        var innerText = error.innerText
        if (error){{
            document.getElementById('{id}').click()
            return innerText
        }}
        """
        return self.driver.execute_script(script)

    @time_out(time_out=2)
    def _op475_get_warning_msg(self):
        script = """
            if (document.getElementById('errormsglabel')){
                return document.getElementById('errormsglabel').innerText
                }
            """
        return self.driver.execute_script(script)

    def _op475_cancel_cost(self, html, **kwargs):
        url = 'https://sistema.ssw.inf.br/bin/ssw0094'
        self.driver.get(url)
        self._op475_post_unit_lanc(kwargs['f11'], kwargs['f12'])
        self.next_window(1)
        self._op475_cancel_lanc()
        self._op475_confirm_warning(-1)

    def _op475_click_open_products(self):
        script="""
        ajaxEnvia('ITENS',1)
        """
        self.driver.execute_script(script)

    @time_out()
    def _op475_get_csts_products(self):
        script="""
        var csts = document.getElementsByTagName('table')[0].querySelectorAll('#tblsr > tbody > tr > td:nth-child(10) > div')
        list_cst = [];
        for (let i = 1;i<csts.length;i++){
            list_cst.push(csts[i].innerText)
        }
        return list_cst
        """
        csts = self.driver.execute_script(script)
        if len(csts)>0:
            return csts
        return


    def _op475_update_cost(self,**kwargs):
        url = 'https://sistema.ssw.inf.br/bin/ssw0094'
        self.driver.get(url)
        self._op475_post_unit_lanc(kwargs['f11'], kwargs['f12'])
        self.next_window(1)
        self._op475_click_open_products()
        self.next_window(2)
        csts = self._op475_get_csts_products()
        if csts is not None and csts and ('90' in csts or '60' in csts):# or '61' in csts
            results = self._op475_perform_changes_products(**kwargs)
            self.next_window(1)
            if results is not None and results and not False in results:
                logging.info(" Produtos alterados! Salvando lançamento")
                input()
                self._op475_confirm_warning(0)
                self._op475_click_save_throw()
                input()
                msg = self._op475_confirm_warning(0)
                if 'Data de Pagamento deve ser dia Útil. Será sugerido o próximo' in str(msg):
                    logging.info('salvando novamente...')
                    self._op475_click_save_throw()
                    msg = self._op475_confirm_warning(0)
                self.next_window(0)
################################################## Update cfop #########################################################
    @time_out(3)
    def _op475_change_cfop_lanc(self, cfop):
        time.sleep(3)
        script = """
        var prd1 = document.getElementById('17').value
        var prd2 = document.getElementById('12').value
        console.log(prd1,prd2)
        return [prd1,prd2]
        """
        prd1, prd2 = self.driver.execute_script(script)
        logging.info(prd1, prd2)
        if prd1:
            script="""
            return document.getElementById('12').value
            """
            cfop_origin = self.driver.execute_script(script)
            if not str(cfop_origin).strip() in self.load_cfops_to_ignore():
                logging.info(f'alterando CFOP {cfop}...')
                script = f"""
                document.getElementById('14').value = '{cfop}'
                """
                self.driver.execute_script(script)
        else:
            raise EmptyValue

    @time_out(time_out=6)
    def _op475_change_values_products_cfop(self,**kwargs):
        prd1, prd2,prd3 = self._op475_wait_load_values()
        prd1 = str(prd1).strip()
        prd2 = str(prd2).strip()
        prd3 = str(prd3).strip()
        logging.info(prd1, prd2,prd3)
        if prd1 or prd2 or prd3:
            logging.info('Produtos carregados, alterando....')
            script = f"""
            document.getElementById('10').value='{kwargs["cfop"]}'
            """
            self.driver.execute_script(script)
            #time.sleep(5)
            return True
        else:
            raise EmptyValue


    @time_out(3)
    def _op475_process_changes_products_cfop(self,**kwargs):
        logging.info('#' * 20, 'clickando', '#' * 20)
        self._op475_click_change_products()
        logging.info('#' * 20, 'alterando', '#' * 20)
        if self._op475_change_values_products_cfop(**kwargs):
            logging.info('#' * 20, 'salvando', '#' * 20)
            self._op475_apply_changes()
            return True
        return False


    @time_out()
    def _op475_perform_changes_products_cfop(self,**kwargs):
        products = self._op475_get_list_products()
        results = []
        for product in products:
            results.append(self._op475_process_changes_products_cfop(**kwargs))
        return results

    def _op475_update_cfop(self,**kwargs):
        url = 'https://sistema.ssw.inf.br/bin/ssw0094'
        self.driver.get(url)
        self._op475_post_unit_lanc(kwargs['f11'], kwargs['f12'])
        self.next_window(1)
        self._op475_change_cfop_lanc(str(kwargs["cfop"]))
        self._op475_click_open_products()
        self.next_window(2)
        results = self._op475_perform_changes_products_cfop(**kwargs)
        self.next_window(1)
        if results is not None and results and not False in results:
            logging.info(" Produtos alterados! Salvando lançamento")
            #input()
            self._op475_confirm_warning(0)
            self._op475_click_save_throw()
            #input()
            msg = self._op475_confirm_warning(0)
            if 'Data de Pagamento deve ser dia Útil. Será sugerido o próximo' in str(msg):
                logging.info('salvando novamente...')
                self._op475_click_save_throw()
                msg = self._op475_confirm_warning(0)
            self.next_window(0)

##########################################################################################################################
    def op475(self, *args, **kwargs):
        """
            :param args:
                - 'available_schedule'
                - 'download_danfes'
                - 'throw_cost'
                - 'cancel_cost'
            :param kwargs:
            Possible keys include:
                - act:
                - f1: Unidade:
                - sefaz: Unidade:
                - f3: Evento:
                - unidade3: Evento:
                - f5: Despesasjácadastradas:
                - cd_barra: codigo de barras da nota
                - evento: Despesasjácadastradas:
                - cfop: numero do cfop
                - data_vencimento: data do vencimento
                - data_entrada: data de entrada da nota
                - historico: valor para colocar no historico da nota
                - icms_event: ICMS
                - f11: N°dolançamentoC.Pagar:
                - unidade11: N°dolançamentoC.Pagar:
                - f16: Períododepagamento(opc):
                - unidade16: Períododepagamento(opc):
                - f17: a
                - f18: Períododeinclusão(opc):
                - f21: (V-vencidas,A-avencer,T-todas)
                - f22: (V-vídeo,R-relatório)
                - f26: Períododepagamento:
                - unidade26: Períododepagamento:
                - f27: a
                - f28: CNPJdofornecedor(opc):
                - estorna:
                - orig_dest:
                - ger_xml:True or False if 'download_danfes' in args
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '475'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0094", headers=self.headers, data=data)

        # showing results

        # logging.info(response.text)

        if 'available_schedule' in args:
            return self._op475_available_to_schedule(response.text, **kwargs)
        if 'download_danfes' in args:
            return self._op475_danfes_download(**kwargs)
        if 'throw_cost' in args:
            return self._op475_throw_cost(response.text, **kwargs)
        if 'cancel_cost' in args:
            self._op475_cancel_cost(response.text, **kwargs)
        if 'update_cost' in args:
            self._op475_update_cost(**kwargs)
        if 'update_cfop' in args:
            self._op475_update_cfop(**kwargs)


if __name__ == '__main__':
    with Ssw475() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op475('available_schedule')
