from priority_classes.ssw.ssw_v2 import SswRequest
from urllib.parse import unquote
import re
import logging

class Ssw101(SswRequest):
    def __init__(self,name_instance='ssw101', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def op101_danfes(self, *args, **kwargs):
        verbose = kwargs.get('verbose',True)
        html = unquote(self.html_text)
        # query filters to request record
        query_model = ("act=A&aviso_resgate=%23aviso_resgate%23&g_ctrc_ser_ctrc=MLV&g_ctrc_nro_ctrc=812&gw_nro_nf_ini"
                       "=0&g_ctrc_nf_vol_ini=0&gw_ctrc_nr_sscc=&g_ctrc_nro_ctl_form=0&gw_ctrc_parc_nro_ctrc_parc=0"
                       "&g_ctrc_c_chave_fis=&local=Q&data_ini_inf=28%2F3%2F23&data_fin_inf=26%2F6%2F23&seq_ctrc"
                       "=21039986&FAMILIA=OTC&dummy=1687794951538")
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act='A',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        if verbose:
            logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053",
                                     headers=self.headers,
                                     data=data)
        self.html_text = response.text
        return self

    def op101_danfes_download(self, *args, **kwargs):
        verbose = kwargs.get('verbose', True)
        ser_nf, nf_nro = self.scrap_tags_from_xml(self.html_text, '<f0>', '</f0>')[1].split('/')

        ser_nf = self.add_left_zero(ser_nf, 3)

        nf_nro = self.add_left_zero(nf_nro, 6)

        chave_nfe = ''.join(re.findall('\d', self.scrap_tags_from_xml(self.html_text,
                                                                      '<f11>',
                                                                      '</f11>')[1].split('&')[3]))

        # &ger_xml=S param to get the file in xml format without it will get in .sswPrintDANFE
        data = (f"opcao=EXT&chave_nfe={chave_nfe}&serNF={ser_nf}&nroNF={nf_nro}&ger_xml=S&dummy=1687796390008&dummy"
                f"=1687796390009")
        if verbose:
            logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1419", headers=self.headers, data=data)
        name_file = None if not 'name_file' in kwargs else kwargs.pop('name_file')

        self.direct_download(response.text, name_file)

    def op101_dacte_download(self, *args, **kwargs):
        verbose = kwargs.get('verbose', True)
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ATALHO_IMP'
        query_model = "act=ATALHO_IMP&seq_ctrc=21263102&FAMILIA=&dummy=1688659540624"
        data = self.update_query_values(self.html_text, query_model, 'name', act=act, dummy='1687793128084', **kwargs)
        if verbose:
            logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0767", headers=self.headers, data=data)

        self.handle_download(response.text, **kwargs)

    def op101_dacte_xml_download(self, *args, **kwargs):
        verbose = kwargs.get('verbose', True)
        query_model = "act=XML&aviso_resgate=%23aviso_resgate%23&g_ctrc_ser_ctrc=&g_ctrc_nro_ctrc=0&gw_nro_nf_ini=0&g_ctrc_nf_vol_ini=0&gw_ctrc_nr_sscc=&g_ctrc_nro_ctl_form=0&gw_ctrc_parc_nro_ctrc_parc=0&g_ctrc_c_chave_fis=&gw_gaiola_codigo=0&gw_pallet_codigo=0&local=Q&data_ini_inf=29%2F2%2F24&data_fin_inf=29%2F5%2F24&seq_ctrc=25692116&FAMILIA=OTC&dummy=1716990555686"
        data = self.update_query_values(self.html_text,
                                        query_model,
                                        'name',
                                        act='XML',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        if verbose:
            logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053", headers=self.headers, data=data)
        try:
            self.handle_download(response.text, **kwargs)
            return True
        except TypeError:
            return 'Sem xml'

    def op101_filter_ocorrences(self, filter_key_word):
        content = self.html_text
        tag_inicio_xml = '<xml'
        tag_final_xml = '</xml>'
        idx_inicio = content.find(tag_inicio_xml)
        idx_final = content.find(tag_final_xml) + len(tag_final_xml)
        xml_user = content[idx_inicio:idx_final]

        # Find number of rows
        rows = xml_user.split('<r>')
        filtered = [row for row in rows if filter_key_word in row]
        return '<r>'.join(filtered)

    def op101_receipts_download(self, *args, **kwargs):
        verbose = kwargs.get('verbose', True)
        filter_key_word = kwargs.pop('filter_key_word') if 'filter_key_word' in kwargs else ''
        html_filtered = self.op101_filter_ocorrences(filter_key_word)
        if verbose:
            logging.info(html_filtered)
        # query filters to request record
        key_ini = 'foto='
        key_fim = 'act=FOT'

        name_file = kwargs.pop('name_file') if 'name_file' in kwargs else 'ssw_receipts.png'

        ocurrences = self.find_all_ocurrences(html_filtered, key_ini)

        for i, index_ini in enumerate(ocurrences):
            index_fim = html_filtered[index_ini:].find(key_fim)
            if -1 != index_fim:
                foto_cod = html_filtered[index_ini + len(key_ini):index_ini + index_fim].split('&')[0]
                if verbose:
                    logging.info(foto_cod)
                act = kwargs.pop('act') if 'act' in kwargs else 'FOT'
                query_model = "seq_ctrc=21578449&foto=OTCQUUFHPY&act=FOT&dummy=1691067918194"

                data = self.update_query_values(self.html_text, query_model, 'name', act=act, dummy='1691067918194',
                                                foto=foto_cod,verbose=verbose)
                response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0122", headers=self.headers, data=data)

                html2 = response.text
                key_ini2 = 'https://ssw.inf.br/cgi-local/ssw0637?'
                key_fim2 = '";}'
                index_ini2 = html2.find(key_ini2)
                index_fim2 = html2[index_ini2:].find(key_fim2)

                if -1 not in (index_ini2, index_fim2):
                    link = html2[index_ini2:index_ini2 + index_fim2]
                    if verbose:
                        logging.info(link)
                    name_list = name_file.split('.')
                    file_ = name_list[0] + f'_{i + 1}.' + name_list[1]
                    self.request_download(link, file_)

    def op101_get_occurrences(self, *args, **kwargs):
        verbose = kwargs.get('verbose', True)
        # query filters to request record
        html = unquote(self.html_text)
        act = kwargs.pop('act') if 'act' in kwargs else 'O'
        query_model = ("act=O&aviso_resgate=%23aviso_resgate%23&g_ctrc_ser_ctrc=CVL&g_ctrc_nro_ctrc=767039"
                       "&gw_nro_nf_ini=0&g_ctrc_nf_vol_ini=0&gw_ctrc_nr_sscc=&g_ctrc_nro_ctl_form=0"
                       "&gw_ctrc_parc_nro_ctrc_parc=0&g_ctrc_c_chave_fis=&gw_gaiola_codigo=0&gw_pallet_codigo=0&local"
                       "=Q&data_ini_inf=5%2F5%2F23&data_fin_inf=3%2F8%2F23&seq_ctrc=21578449&FAMILIA=OTC&dummy"
                       "=1691069254175")
        data = self.update_query_values(html, query_model, 'name', act=act, dummy='1691069254175',verbose=verbose)
        if verbose:
            logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053", headers=self.headers, data=data)
        if verbose:
            logging.info(response.text)
        self.html_text = response.text
        self.html_content = response.content
        return self

    def op101_get_last_operation(self, *args, **kwargs):
        verbose = kwargs.get('verbose', True)
        # query filters to request record
        html = unquote(self.html_text)
        act = kwargs.pop('act') if 'act' in kwargs else 'S'
        query_model = ("act=S&aviso_resgate=%23aviso_resgate%23&g_ctrc_ser_ctrc=POA&g_ctrc_nro_ctrc=35081"
                       "&gw_nro_nf_ini=0&g_ctrc_nf_vol_ini=0&gw_ctrc_nr_sscc=&g_ctrc_nro_ctl_form=0"
                       "&gw_ctrc_parc_nro_ctrc_parc=0&g_ctrc_c_chave_fis=&gw_gaiola_codigo=0&gw_pallet_codigo=0&local"
                       "=Q&data_ini_inf=5%2F5%2F23&data_fin_inf=3%2F8%2F23&seq_ctrc=21105848&FAMILIA=OTC&dummy"
                       "=1691092683729")
        data = self.update_query_values(html, query_model, 'name', act=act, dummy='1691069254175',verbose=verbose)
        if verbose:
            logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053", headers=self.headers, data=data)
        if verbose:
            logging.info(response.text)
        return self.get_table(response.text, 24)

    def op101_throw_ocurrence(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - f3: ocorrencia
                - f4: data
                - f5: hora
                - f6: informação complementar
                - f8: segregar ctrc (S/N)
                - f11: resposta a um fale conosco(S/N)
            hidden:
                - detalhe_oco:
                - detalhe_ins:
                - tipoFoto:
                - nomeFoto:
                - extraFoto:
                - nomeFotoUsed:
                - ctrl_gelo_tp_produto:
                - ctrl_gelo_tp_gelo:
                - ctrl_gelo_data_inicio:
                - ctrl_gelo_hora_inicio:
                - ctrl_gelo_prazo:
                - seq_ctrc:
                - data_ini_inf:
                - data_fin_inf:
                - local:
                - FAMILIA:
            :type kwargs: dict
            :return: None
        """

        verbose = kwargs.get('verbose', True)
        #go to occurrence page
        self.op101_get_occurrences()
        # query filters to request record
        html = unquote(self.html_text)
        # act = kwargs.pop('act') if 'act' in kwargs else 'II3'
        query_model = (
            "act=II3&observ=.&f3=&f4=240823&f5=1712&f6=.&f8=N&f11=N&detalhe_oco=&detalhe_ins=&tipoFoto=avaria"
            "&nomeFoto=DWCOTUE&extraFoto=CA1%2F2308%2F22&nomeFotoUsed=&ctrl_gelo_tp_produto"
            "=&ctrl_gelo_tp_gelo=&ctrl_gelo_data_inicio=&ctrl_gelo_hora_inicio=&ctrl_gelo_prazo=&seq_ctrc"
            "=21912616&data_ini_inf=26%2F5%2F23&data_fin_inf=30%2F12%2F99&local=&FAMILIA=OTC&dummy"
            "=1692912159915")
        data = self.update_query_values(html, query_model, 'name', act='II3', dummy='1692911565101', **kwargs)
        if verbose:
            logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0122", headers=self.headers, data=data)
        if verbose:
            logging.info(response.text)
        self.html_text = response.text
        return self

    def op101_throw_instruction(self,*args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f4: Informaçõescomplementares:
                - f5: Informaçõescomplementares:
                - f8: (S/N)
                - observ: Texto da instrução
                - f11: (S/N)
                - detalhe_oco:
                - detalhe_ins:
                - tipoFoto:
                - nomeFoto:
                - extraFoto:
                - nomeFotoUsed:
                - ctrl_gelo_tp_produto:
                - ctrl_gelo_tp_gelo:
                - ctrl_gelo_data_inicio:
                - ctrl_gelo_hora_inicio:
                - ctrl_gelo_prazo:
                - seq_ctrc:
                - data_ini_inf:
                - data_fin_inf:
                - local:
                - FAMILIA:
            :type kwargs: dict
            :return: None
        """
        verbose = kwargs.get('verbose', True)
        self.op101_get_occurrences()
        query_model = ("act=II4&observ=.&f4=250823&f5=0845&f8=N&f11=N&detalhe_oco=&detalhe_ins=&tipoFoto=avaria"
                       "&nomeFoto=BYAXREW&extraFoto=CA1%2F2308%2F22&nomeFotoUsed=&ctrl_gelo_tp_produto"
                       "=&ctrl_gelo_tp_gelo=&ctrl_gelo_data_inicio=&ctrl_gelo_hora_inicio=&ctrl_gelo_prazo=&seq_ctrc"
                       "=21912616&data_ini_inf=27%2F5%2F23&data_fin_inf=30%2F12%2F99&local=&FAMILIA=OTC&dummy"
                       "=1692967586974")
        data1 = self.update_query_values(self.html_text,
                                         query_model,
                                         'name',
                                         act='II4',
                                         dummy=self.get_dummy(),
                                         **kwargs)
        if verbose:
            logging.info(data1)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0122", headers=self.headers, data=data1)
        if verbose:
            logging.info(response.text)
        text_resp = response.text

        key_ini = "<!--GoBack-->"
        index_ini = text_resp.find(key_ini)

        msgx = text_resp[index_ini + len(key_ini):].strip()
        if verbose:
            logging.info('#' * 20, msgx, '#' * 20)

        data2 = "seq_ctrc=21912616&accept_tel=&gw_ocor_entrega_codigo=0&seq_manifesto=0&act=O&msg=&dummy=1692967587078"
        data2 = self.update_query_values(response.text, data2, 'name', dummy=self.get_dummy(),verbose=verbose)
        data2 = data2.replace('msg=', f'msgx={msgx}')
        if verbose:
            logging.info(data2)

        query_model = ("act=&observ=.&f4=250823&f5=0845&f8=N&f11=N&detalhe_oco=&detalhe_ins=&tipoFoto=avaria&nomeFoto"
                       "=BYAXREW&extraFoto=CA1%2F2308%2F22&nomeFotoUsed=&ctrl_gelo_tp_produto=&ctrl_gelo_tp_gelo"
                       "=&ctrl_gelo_data_inicio=&ctrl_gelo_hora_inicio=&ctrl_gelo_prazo=&seq_ctrc=21912616"
                       "&data_ini_inf=27%2F5%2F23&data_fin_inf=30%2F12%2F99&local=&FAMILIA=OTC")
        data3 = self.update_query_values(self.html_text, query_model, 'name', act='', **kwargs)
        if verbose:
            logging.info(data3)

        data = data3 + "&" + data2  # +"&" + data3
        if verbose:
            logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053", headers=self.headers, data=data)

        text_resp = response.text  # unquote(response.text)
        if verbose:
            logging.info(text_resp)
        self.html_text = response.text
        return self

    def op101_select_ctrc_family(self, *args, **kwargs):
        verbose = kwargs.get('verbose', True)
        df = self.get_table(self.html_text, 14)
        if verbose:
            logging.info(len(df), df)
        df.to_csv('ssw101_indexes.csv', sep=';')
        if len(df) > 0 and 'if_many_ctrc_filter_by' in kwargs:
            df = self.filter_df_by_values(df, kwargs['if_many_ctrc_filter_by'])
            if len(df) > 0:
                family = df.loc[0, '<f13>'].replace('>', '')
                if verbose:
                    logging.info(family)
                query_model = (
                    "act=FAMILIA@OTC@25960779@30/05/2024&g_ctrc_ser_ctrc=&g_ctrc_nro_ctrc=0&gw_nro_nf_ini=29743&g_ctrc_nf_vol_ini=0&gw_ctrc_nr_sscc=&g_ctrc_nro_ctl_form=0&gw_ctrc_parc_nro_ctrc_parc=0&g_ctrc_c_chave_fis=&gw_gaiola_codigo=0&gw_pallet_codigo=0&data_ini_inf=2%2F3%2F24&data_fin_inf=31%2F5%2F24&seq_ctrc=0&local=&FAMILIA=&dummy=1717179517193")
                data = self.update_query_values(self.html_text,
                                                query_model,
                                                'name',
                                                act=family,
                                                dummy=self.get_dummy(),
                                                **kwargs)
                if verbose:
                    logging.info(data)
                response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053",
                                             headers=self.headers,
                                             data=data)
                if verbose:
                    logging.info(response.text)
                self.html_text = response.text
                self.html_content = response.content
        return self

    def get_info(self):
        if 'ssw0053.35' in self.html_text:
            return self.html_text
        else:
            return 'Cte não encontrado!'


    def op101(self, *args, **kwargs):
        """
        :param kwargs:
        Possible keys include:
            - act: 'P1','P2','P6','P5','BAR'...
            - t_ser_ctrc: sigla ctrc -> act: 'P1'
            - t_nro_ctrc: numero ctrc -> act: 'P1'
            - t_nro_nf: nº da nota -> act: 'P2'
            - t_data_ini: data_ini
            - t_data_fin: data_fin
            - t_ctrc_orig: Cte de origem -> act:'P5'
            - t_cod_barras: cod barras -> act: 'BAR'
            - t_nro_pedido: nº pedido -> act:'P6'
            - if_many_ctrc_filter_by: When the ctrc searched return more than one, will be selected those who match the value in the column {'<f0>':'EXT'}
            - seq_ctrc:
            - local:
            - FAMILIA:
            - name_file:
            - filter_key_word: keyword to filter the table ocurrences
        """
        self.last_opssw = '101'
        verbose = kwargs.get('verbose', True)
        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1687792297265"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1687792297391"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053", headers=self.headers, data=data)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'P1'
        query_model = (
            "act=P1&t_ser_ctrc=mlv&t_nro_ctrc=000812&t_ctrc_orig=&t_data_ini=280323&t_data_fin=260623&data_ini_inf=30"
            "%2F12%2F99&data_fin_inf=30%2F12%2F99&seq_ctrc=0&local=&FAMILIA=&dummy=1687793128084")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy='1687793128084',
                                        **kwargs)
        if verbose:
            logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0053",
                                     headers=self.headers,
                                     data=data)
        self.html_text = response.text
        self.html_content = response.content
        self.op101_select_ctrc_family(*args, **kwargs)
        if verbose:
            logging.info(self.html_text)
        return self


if __name__ == '__main__':
    with Ssw101() as ssw:
        ssw.init_browser()
        ssw.login()
        logging.info(ssw.op101('info',
                        t_ser_ctrc='JAR',
                        t_nro_ctrc='740872').text)
