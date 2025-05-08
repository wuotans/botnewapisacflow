from priority_classes.ssw.ssw_v2 import SswRequest
import logging
import re
import requests
import gc
from datetime import datetime
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote
import urllib.parse
import logging


DESATIVADO = 'Acesso ao mobile desativado.'
TOKEN = 'Token para ativacao do SSWMobile'
INVALIDO = 'Telefone inv&aacute;lido'

class TryAgain(Exception):
    pass


class Ssw925(SswRequest):
    def __init__(self,name_instance='ssw925', **kwargs):
        super().__init__(name_instance=name_instance,prefix_env='SSW_MASTER',**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def op925(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '925'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        return self
    
    def urlencode(self,params):
        query = ''
        for key in params:
            query += f'&{key}={params[key]}'
        return query

    def get_user_login(self,*args, **kwargs):
        data=f'act=PES&dummy={self.get_dummy()}'
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)

        act = kwargs.pop('act') if 'act' in kwargs else 'PE1'
        query_model = f"act=PE1&f5=05153726177&f6=N&dummy=1686144761370"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)
        logging.info(response.text)
        return response.text

    def get_login_info(self, login):
        data = f"act=ALT|{login}&dummy=1686157442309"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)
        return response.text

    def change_login_info(self, query):
        data = f"{query}"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)
        return response.text

    def _build_user_query_change_password(self,html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find all input tags in the HTML
        inputs = soup.find_all('input')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get('id'): input_tag.get('value') for input_tag in inputs}

        # Update the dictionary with any additional parameters
        additional_params = {
            'login_usuario': '',
            'cod_emp_ctb': '',
            'nome': '',
            'cpf': '',
            'grupo': '',
            'nomegrupo': '',
            'unid': '',
            'sel_unid': '',
            'inf_frete': '',
            'emit_cort': '',
            'desbloq_resul': '',
            'ssw_mod_livre': '',
            'apon_opc20': '',
            'inc_cli': '',
            'alt_cli': '',
            'alt_res_cli': '',
            'con_cli': '',
            'inc_outros': '',
            'alt_outros': '',
            'alt_res_outros': '',
            'con_outros': '',
            'geren_seg': '',
            'senha_expira': '',
            'dias_senha_expira': '',
            'forca_troca_senha': '',
            'tentativas_bloqueio': '',
            'email': '',
            'acesso_local': '',
            'dias_trab': '',
            'act': 'ENV',
            'f2': '',
            'msgx': '',
            'dummy': '1686144580208'
        }
        for key in additional_params:
            try:
                additional_params[key] = params[key]
            except KeyError:
                pass
        additional_params['f2'] = additional_params['login_usuario']
        additional_params['senha'] = '1234'
        additional_params['senha_confirma'] = '1234'

        # Use self.urlencode to create the query string
        query = 'act=&' + self.urlencode(additional_params)

        return query

    def _build_user_query_unblock(self,html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find all input tags in the HTML
        inputs = soup.find_all('input')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get('id'): input_tag.get('value') for input_tag in inputs}

        # Update the dictionary with any additional parameters
        additional_params = {
            'login_usuario': '',
            'cod_emp_ctb': '',
            'nome': '',
            'cpf': '',
            'grupo': '',
            'nomegrupo': '',
            'unid': '',
            'sel_unid': '',
            'inf_frete': '',
            'emit_cort': '',
            'desbloq_resul': '',
            'ssw_mod_livre': '',
            'apon_opc20': '',
            'inc_cli': '',
            'alt_cli': '',
            'alt_res_cli': '',
            'con_cli': '',
            'inc_outros': '',
            'alt_outros': '',
            'alt_res_outros': '',
            'con_outros': '',
            'geren_seg': '',
            'senha_expira': '',
            'dias_senha_expira': '',
            'forca_troca_senha': '',
            'tentativas_bloqueio': '',
            'email': '',
            'acesso_local': '',
            'dias_trab': '',
            'dummy': '1686315933214'
        }
        for key in additional_params:
            try:
                additional_params[key] = params[key]
            except KeyError:
                pass
        additional_params['act'] = 'BLOQ'
        additional_params['senha'] = '1234'
        additional_params['senha_confirma'] = '1234'

        # Use self.urlencode to create the query string
        query = self.urlencode(additional_params)

        return query, additional_params

    def _build_user_query_record(self,html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find all input tags in the HTML
        inputs = soup.find_all('input')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get('id'): input_tag.get('value') for input_tag in inputs}

        # Update the dictionary with any additional parameters
        additional_params = {
            'login_usuario': '',
            'cod_emp_ctb': '',
            'nome': '',
            'cpf': '',
            'grupo': '',
            'nomegrupo': '',
            'unid': '',
            'sel_unid': '',
            'inf_frete': '',
            'emit_cort': '',
            'desbloq_resul': '',
            'ssw_mod_livre': '',
            'apon_opc20': '',
            'inc_cli': '',
            'alt_cli': '',
            'alt_res_cli': '',
            'con_cli': '',
            'inc_outros': '',
            'alt_outros': '',
            'alt_res_outros': '',
            'con_outros': '',
            'geren_seg': '',
            'senha_expira': '',
            'dias_senha_expira': '',
            'forca_troca_senha': '',
            'tentativas_bloqueio': '',
            'email': '',
            'acesso_local': '',
            'dias_trab': '',
            'dummy': '1686318934193'
        }
        for key in additional_params:
            try:
                additional_params[key] = params[key]
            except KeyError:
                pass
        additional_params['act'] = 'EN2'
        additional_params['senha'] = '1234'
        additional_params['senha_confirma'] = '1234'
        additional_params['forca_troca_senha'] = 'S'

        # Use self.urlencode to create the query string
        query = self.urlencode(additional_params)

        return query

    def _build_user_query_enable_mobile(self,html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find all input tags in the HTML
        inputs = soup.find_all('input')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get('id'): input_tag.get('value') for input_tag in inputs}

        # Update the dictionary with any additional parameters
        additional_params = {
            'act': 'HAB',
            'login_usuario': '',
            'cod_emp_ctb': '',
            'nome': '',
            'cpf': '',
            'grupo': '',
            'nomegrupo': '',
            'unid': '',
            'sel_unid': '',
            'inf_frete': '',
            'emit_cort': '',
            'desbloq_resul': '',
            'ssw_mod_livre': '',
            'apon_opc20': '',
            'inc_cli': '',
            'alt_cli': '',
            'alt_res_cli': '',
            'con_cli': '',
            'inc_outros': '',
            'alt_outros': '',
            'alt_res_outros': '',
            'con_outros': '',
            'geren_seg': '',
            'senha_expira': '',
            'dias_senha_expira': '',
            'forca_troca_senha': '',
            'tentativas_bloqueio': '',
            'email': '',
            'ddd_telefone': '',
            'telefone': '',
            'ddd_celular': '',
            'celular': '',
            'acesso_local': '',
            'dias_trab': '',
            'dummy': '1686571923385'
        }
        for key in additional_params:
            try:
                additional_params[key] = params[key]
            except KeyError:
                pass
        # additional_params['act'] = 'HAB'

        # Use self.urlencode to create the query string
        query = self.urlencode(additional_params)

        return query, additional_params

    def _build_user_query_send_token(self,html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find all input tags in the HTML
        inputs = soup.find_all('input')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get('id'): input_tag.get('value') for input_tag in inputs}

        # Update the dictionary with any additional parameters
        additional_params = {
            'act': '',
            'h_cpf': '',
            'inp_1535': '',
            'login_usuario': '',
            'cod_emp_ctb': '',
            'nome': '',
            'cpf': '',
            'grupo': '',
            'nomegrupo': '',
            'unid': '',
            'sel_unid': '',
            'inf_frete': '',
            'emit_cort': '',
            'desbloq_resul': '',
            'ssw_mod_livre': '',
            'apon_opc20': '',
            'inc_cli': '',
            'alt_cli': '',
            'alt_res_cli': '',
            'con_cli': '',
            'inc_outros': '',
            'alt_outros': '',
            'alt_res_outros': '',
            'con_outros': '',
            'geren_seg': '',
            'senha_expira': '',
            'forca_troca_senha': '',
            'tentativas_bloqueio': '',
            'email': '',
            'ddd_telefone': '',
            'telefone': '',
            'ddd_celular': '',
            'celular': '',
            'acesso_local': '',
            'dias_trab': '',
            'dummy': '',
            'remember': '',
            'useri': '',
            'ssw_dom': '',
            'token': ''
        }
        for key in additional_params:
            try:
                additional_params[key] = params[key]
            except KeyError:
                pass
        # Removendo formatação de urls
        for key in additional_params:
            additional_params[key] = urllib.parse.unquote(additional_params[key])

        additional_params['act'] = 'HAB'
        additional_params['inp_1535'] = additional_params['ddd_celular'] + additional_params['celular']
        additional_params['dummy'] = '1686571923385'

        query_format = []
        for key in additional_params:
            query_format.append(f'{key}={additional_params[key]}')
        query = '&'.join(query_format) + '&dummy=1686571928392'

        return query

    def _scrap_user_from_html(self,text):
        # Finding the desired elements
        content = text
        tag_inicio = '<xml'
        tag_final = '</xml>'
        idx_inicio = content.find(tag_inicio)
        idx_final = content.find(tag_final) + len(tag_final)
        xml_user = content[idx_inicio:idx_final]

        # Find number of rows
        rows = xml_user.split('<r>')

        for row in rows:

            # Finding user group
            tag_inicio = '<f5>'
            tag_final = '</f5>'
            idx_inicio = row.find(tag_inicio)
            idx_final = row.find(tag_final)

            if -1 not in (idx_inicio, idx_final):
                group = row[idx_inicio + 4:idx_final]

                if '046' not in group and '092' not in group:
                    # Finding user login
                    tag_inicio = '<f0>'
                    tag_final = '</f0>'
                    idx_inicio = row.find(tag_inicio)
                    idx_final = row.find(tag_final)
                    login = row[idx_inicio + 4:idx_final]

                    return login
        return None

    def desbloquer_usuario_by_request_session(self,cpf):
        logging.info('Iniciando desbloqueio')
        html_txt = self.get_user_login(f5=cpf)
        logging.info(html_txt)
        login = self._scrap_user_from_html(html_txt)

        if login is not None:
            html_txt = self.get_login_info(login)
            query, dict_params = self._build_user_query_unblock(html_txt)
            if dict_params['grupo'] not in ('046', '092'):
                html_txt = self.change_login_info(query)

                query = self._build_user_query_change_password(html_txt)
                html_txt = self.change_login_info(query)

                query = self._build_user_query_record(html_txt)
                html_txt = self.change_login_info(query)
                logging.info('saindo...')
                return 'Nova senha: 1234'
        else:
            return 'Cpf nao foi encontrado ou esta desativado'


    def gerar_token_by_request_session(self,cpf):
        logging.info('Iniciando token')
        html_txt = self.get_user_login(f5=cpf)
        logging.info(html_txt)

        login = self._scrap_user_from_html(html_txt)
        if login is not None:
            html_txt = self.get_login_info(login)

            query, dict_params = self._build_user_query_enable_mobile(html_txt)
            if dict_params['grupo'] not in ('046', '092'):

                html_txt = self.change_login_info(query)
                status_enable_mobile = html_txt

                # response.content here cause ignore url formating
                query = self._build_user_query_send_token(html_txt)
                html_txt = self.change_login_info(query)
                status_send_token = html_txt

                if DESATIVADO in status_enable_mobile:
                    resp = self.gerar_token_by_request_session(cpf)
                    return resp
                elif TOKEN in status_send_token:
                    codigo = status_send_token[status_send_token.find(TOKEN):]
                    return str(codigo).replace('\n', '')
                elif INVALIDO in status_send_token:
                    return 'Telefone invalido'
                else:
                    return 'Comportamento Inesperado entre em contato com o resposavel'
        else:
            return 'cpf nao foi encontrado ou esta desativado'



if __name__ == '__main__':
    with Ssw925() as ssw:
        ...

