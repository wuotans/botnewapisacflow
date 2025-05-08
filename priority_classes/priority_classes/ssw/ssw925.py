from priority_classes.ssw.ssw import SswRequest
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlencode
import logging


class Ssw925(SswRequest):
    def __init__(self):
        super().__init__()

    def _op925_get_user_login(self, cpf):
            data = f"act=PE1&f5={cpf}&f6=N&dummy=1686144761370"
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)
            return response


    def _op925_get_login_info(self, login):
            data = f"act=ALT|{login}&dummy=1686157442309"
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)
            return response


    def _op925_change_login_info(self, data):
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=headers, data=data)
            return response


    def _op925_build_user_query_change_password(self,html):
        """
            Build the query string to change the user's password.

            This function parses the HTML and extracts the input fields. It builds a query string with the necessary parameters
            to change the user's password.

            :param html: The HTML content.
            :type html: str
            :return: The query string.
            :rtype: str

            :process:
                1. Parse the HTML using BeautifulSoup.
                2. Find all input tags in the HTML.
                3. Build a dictionary with the ids and values from the input tags.
                4. Update the dictionary with additional parameters.
                5. Use urlencode to create the query string.
                6. Return the query string.

            Example:
                >>> build_user_query_change_password(html_content)
        """

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

        # Use urlencode to create the query string
        query = 'act=&' + urlencode(additional_params)

        return query

    def _op925_build_user_query_unblock(self,html):
        """
            Build the query string to unblock a user.

            This function parses the HTML and extracts the input fields. It builds a query string with the necessary parameters
            to unblock a user.

            :param html: The HTML content.
            :type html: str
            :return: The query string and additional parameters.
            :rtype: tuple

            :process:
                1. Parse the HTML using BeautifulSoup.
                2. Find all input tags in the HTML.
                3. Build a dictionary with the ids and values from the input tags.
                4. Update the dictionary with additional parameters.
                5. Use urlencode to create the query string.
                6. Return the query string and additional parameters.

            Example:
                >>> build_user_query_unblock(html_content)
        """
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

        # Use urlencode to create the query string
        query = urlencode(additional_params)

        return query, additional_params

    def _op925_build_user_query_record(self,html):
        """
            Build the query string to record a user.

            This function parses the HTML and extracts the input fields. It builds a query string with the necessary parameters
            to record a user.

            :param html: The HTML content.
            :type html: str
            :return: The query string.
            :rtype: str

            :process:
                1. Parse the HTML using BeautifulSoup.
                2. Find all input tags in the HTML.
                3. Build a dictionary with the ids and values from the input tags.
                4. Update the dictionary with additional parameters.
                5. Use urlencode to create the query string.
                6. Return the query string.

            Example:
                >>> build_user_query_record(html_content)
        """
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

        # Use urlencode to create the query string
        query = urlencode(additional_params)

        return query

    def _op925_build_user_query_enable_mobile(self,html):
        """
            Build the query string to enable mobile access for a user.

            This function parses the HTML and extracts the input fields. It builds a query string with the necessary parameters
            to enable mobile access for a user.

            :param html: The HTML content.
            :type html: str
            :return: The query string and additional parameters.
            :rtype: tuple

            :process:
                1. Parse the HTML using BeautifulSoup.
                2. Find all input tags in the HTML.
                3. Build a dictionary with the ids and values from the input tags.
                4. Update the dictionary with additional parameters.
                5. Use urlencode to create the query string.
                6. Return the query string and additional parameters.

            Example:
                >>> build_user_query_enable_mobile(html_content)
        """
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

        # Use urlencode to create the query string
        query = urlencode(additional_params)

        return query, additional_params

    def _op925_build_user_query_send_token(self,html):
        """
            Build the query string to send a token for user activation.

            This function parses the HTML and extracts the input fields. It builds a query string with the necessary parameters
            to send a token for user activation.

            :param html: The HTML content.
            :type html: str
            :return: The query string.
            :rtype: str

            :process:
                1. Parse the HTML using BeautifulSoup.
                2. Find all input tags in the HTML.
                3. Build a dictionary with the ids and values from the input tags.
                4. Update the dictionary with additional parameters.
                5. Remove URL formatting from the values.
                6. Format the query string.
                7. Return the query string.

            Example:
                >>> build_user_query_send_token(html_content)
        """
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

    def _op925_scrap_user_from_html(self,text):
        """
            Scrape the user login from HTML text.

            This function searches for the desired elements in the HTML text to extract the user login.
            It finds the XML section, identifies the user group, and returns the user login if the group is not '046' or '092'.

            :param text: The HTML text to scrape.
            :type text: str
            :return: The user login if found, or None if not found.
            :rtype: str or None

            :process:
                1. Find the XML section in the HTML text.
                2. Split the XML section into rows.
                3. Iterate over each row.
                4. Find the user group in each row.
                5. If the group is not '046' or '092', find and return the user login.
                6. Return None if the login is not found.

            Example:
                >>> scrap_user_from_html(html_text)
        """
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
    def _op925_update_user_info(self,html,**kwargs):
        act = kwargs.pop('act') if 'act' in kwargs else 'EN2'
        query_model = "act=EN2&login_usuario=benhursa&cod_emp_ctb=0&nome=BEN%20HUR%20PEREIRA%20BORGES%20DOS%20S.&cpf=05153726177&grupo=018&nomegrupo=ADMINISTRATIVO%20GERAL&unid=MTZ&sel_unid=S&inf_frete=N&emit_cort=n&desbloq_resul=n&ssw_mod_livre=S&apon_opc20=S&inc_cli=S&alt_cli=S&alt_res_cli=N&con_cli=S&inc_outros=S&alt_outros=S&alt_res_outros=N&con_outros=S&geren_seg=N&senha_expira=3&dias_senha_expira=30&forca_troca_senha=S&tentativas_bloqueio=0&email=CONTROLADORIA.10@CARVALIMA.COM.BR&acesso_local=N&dias_trab=A&dummy=1702317386934"
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

    def op925(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - login_usuario:
                - cod_emp_ctb:
                - nome:
                - cpf:
                - grupo:
                - nomegrupo:
                - unid: (paraClientesdeixeestecampoembranco)
                - sel_unid: (S/N)
                - inf_frete: (S/N)
                - emit_cort: (S/N)
                - desbloq_resul: (S/N)
                - ssw_mod_livre: (S/N)
                - apon_opc20: (S/N)
                - inc_cli: (S/N)
                - alt_cli: (S/N)
                - alt_res_cli: (S/N)
                - con_cli: (S/N)
                - inc_outros: (S/N)
                - alt_outros: (S/N)
                - alt_res_outros: (S/N)
                - con_outros: (S/N)
                - geren_seg: (S/N)
                - senha_expira: (1-nunca,2-nadatadefinidaabaixo,3-naquantidadedediasdefinidaabaixo)
                - dias_senha_expira: (dias)
                - forca_troca_senha: (S/N)-Usuárioseráobrigadoatrocarsuasenhanopróximologin.
                - tentativas_bloqueio: (tentativas)
                - email: Telefone:
                - acesso_local: (S/N)
                - dias_trab: (S-sábado,D-domingo,A-ambos,N-nenhum)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '925'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0384", headers=self.headers, data=data)

        if 'update_info' in args:
            user_html = self._op925_get_login_info(kwargs['login_usuario']).text
            self._op925_update_user_info(user_html,**kwargs)



if __name__ == '__main__':
    with Ssw925() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op925()
