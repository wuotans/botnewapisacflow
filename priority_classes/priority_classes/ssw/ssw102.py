from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw102(SswRequest):
    def __init__(self):
        super().__init__()

    def _op102_get_report(self, html, act, **kwargs):
        # query filters to request record
        query_model = ("act=PAG&data_ini=010123&data_fin=060723&c_selecionar=T&c_entrega=T&c_listar=e&c_tipo=E"
                       "&cliente_cgc=&btn_1243=S&seq_cliente=948295&cliente=CHICO%20SALGADO%20TRANSPORTES%20%28%2E"
                       "%2E%29&dummy=1688651775129")
        data = self.update_query_values(html,
                                        query_model,
                                        'name',
                                        act=act,
                                        btn_1243='S',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0054", headers=self.headers, data=data)
        logging.info(response.text)
        if 'informados selecionam um grande volume de dados' in response.text:
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0054", headers=self.headers, data=data)
            logging.info(response.text)

        if 'N&atilde;o h&aacute; movimento para per&iacute;odo informado.' not in response.text:
            # download the report
            self.handle_download(response.text, **kwargs)

    def op102(self, *args, **kwargs):
        """
            :param args:
                - 'info'
                - 'pagador'
                - 'remetente'
            :param kwargs:
            Possible keys include:
                - act: 'E', 'RAI'
                - cnpj_cliente: cnpj do cliente e param ->  act: 'E'
                - nome_cliente: none do cliente:
                - nome_cidade: cidade:
                - numero_telefone: telefone:
                - numero_cnpj_grupo: cnpj do grupo:
                - numero_cnpj_raiz: raiz do cnpj, e param -> act: 'RAI'
                - login_resp:
                - tipo:
                - automatico:
                - programa:
                - fld:
                - seq_cliente:
                - cliente:
            Possible keys include report:
                - data_ini: data inicial
                - data_fin: data final
                - c_selecionar: (T-todos,N-Nãoentregues,E-entregues)
                - c_entrega: (T-todos,D-TDE)
                - c_listar: (V-vídeo,R-relatório,E-Excel,G-ExceldoGrupo)
                - c_tipo: (E-emissãodoCTRC,U-UF,M-mercadoria)
                - cliente_cgc:
                - name_file: name to the report
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '102'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0054", headers=self.headers, data=data)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'E'
        query_model = ("act=E&cnpj_cliente=6546&nome_cliente=545&nome_cidade=456456&numero_telefone=456"
                       "&numero_cnpj_grupo=456&numero_cnpj_raiz=456&login_resp=botcvl&tipo=cliente&automatico=S"
                       "&programa=ssw0054&fld=1&seq_cliente=0&cliente=&dummy=1688651367689")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0054", headers=self.headers, data=data)

        if 'recebedor' in args:
            self._op102_get_report(response.text, 'CEB', **kwargs)
        
        if 'pagador' in args:
            self._op102_get_report(response.text, 'PAG', **kwargs)

        if 'remetente' in args:
            self._op102_get_report(response.text, 'REM', **kwargs)

        if 'destinatario' in args:
            self._op102_get_report(response.text, 'DES', **kwargs)

        if 'info' in args:
            return response


if __name__ == '__main__':
    with Ssw102() as ssw:
        ssw.init_browser()
        ssw.login()
        logging.info(ssw.op102('info').text)
