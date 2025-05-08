import html
from urllib.parse import unquote
from priority_classes.ssw.ssw import SswRequest
import logging


class InvoiceNotPending(Exception):
    pass

class Ssw048(SswRequest):
    def __init__(self):
        super().__init__()

    def _op048_get_seq(self, html):
        logging.info(html)

    def _op048_get_table(self, html):
        self._op048_get_seq(html)
        return self.get_table(html, 15)

    def _op048_liquidate(self, list_seq_fatura, tot_liquid, acni):
        seq_fat = ['SRENV'] + list_seq_fatura
        seq_fat = '|'.join(seq_fat)

        formatted_number = (f'{tot_liquid:,.2f}'
                            .replace(',', '/')
                            .replace('.', ',')
                            .replace('/', '.')
                            )

        status_seq_fat = '&'.join(['=TRUE' for _ in list_seq_fatura])

        data = f"act={seq_fat}&{status_seq_fat}&totliq={formatted_number}&cod_emp_ctb=1&dummy=1691423233345"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)

        # showing results
        decoded_text = html.unescape(response.text)
        logging.info(decoded_text)

        query_model = f"act=LIQ_VIA_ACNI_PAG&valor_aliquidar={formatted_number}&vlr_juros=0%2C00&vlr_liquido={formatted_number}&f3=341&f4=01433&f5=1&f6=000024937&f7=0&vlr_debito=0&variaveis={seq_fat}&vlr_aliquidar={formatted_number}&creditar=T&cod_emp_ctb=1&dummy=1691428158097"
        data1 = self.update_query_values(response.text,
                                         query_model,
                                         'name',
                                         act='LIQ_VIA_ACNI_PAG',
                                         dummy='1691428158097',
                                         unquote=True)
        data1 = unquote(data1)
        logging.info(html.unescape(data1))
        response2 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data1)
        decoded_text2 = html.unescape(response2.text)
        logging.info(decoded_text2)

        logging.info(acni)

        query_model = f"act=LIQ_VIA_ACNI_PAG&vlr_debito=0&variaveis={seq_fat}&vlr_aliquidar={formatted_number}&creditar=T&cod_emp_ctb=1&vlr_aliquidar={formatted_number}&inp_98={acni}&valor_aliquidar={formatted_number}&vlr_juros=0,00&vlr_liquido={formatted_number}&f3=341&f4=01433&f5=1&f6=000024937&f7=0&vlr_debito=0&variaveis={seq_fat}&creditar=T&cod_emp_ctb=1&dummy=1691443107195&remember=1&useri=12345678909&lastcnpj_cotacao=&sr_pageno=40&ssw_dom=OTC&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTE0OTk0NzksInB4eSI6IjE3Mi4zMS4zOC4yMzYifQ.5hWR1iNTsgpPYx_6CEGbcjVYpnMISeZY4JW2APssTlE&dummy=1691443200650"
        data2 = self.update_query_values(response2.text,
                                         query_model,
                                         'name',
                                         act='LIQ_VIA_ACNI_PAG',
                                         inp_98=acni,
                                         dummy='1691429219671',
                                         unquote=True)
        data2 = unquote(data2)
        logging.info(f'{data2}&dummy=1691429219671')
        logging.info(html.unescape(data2))
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers,
                          data=f'{data2}&dummy=1691429219671')
        logging.info(response.text)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data1)
        logging.info(response.text)

        logging.info(f'{data2}&dummy=1691443213722')
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers,
                          data=f'{data2}&dummy=1691443213722')
        logging.info(response.text)
        if 'n&atilde;o est&aacute; mais pendente' in response.text:
            fatura = str(response.text).split('fatura ')[1].split()[0].strip() + '\n'
            with open('relatorios/erro_faturas_liquidacao.txt','w') as f:
                f.write(fatura)
            raise InvoiceNotPending(unquote(response.text))

        logging.info(f'{data1.replace("act=LIQ_VIA_ACNI_PAG", "act=")}')
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers,
                          data=f'{data1.replace("act=LIQ_VIA_ACNI_PAG", "act=")}')
        logging.info(response.text)

    def _op048_get_info_ctrc(self, html_t, **kwargs):
        data = ('hidd_seq_ctrc=&hidd_seq_fatura=&hidd_ctrc=&hidd_dtemiss=&hidd_valor=&hidd_cliente'
                '=&hidd_valor_aliquidar=')
        data = self.update_query_values(html_t, data, 'name')
        data = unquote(data).replace('+&+', '+@+')
        logging.info(data)
        dict_info_ctrc = self.convert_query_url_to_dict(data, False)
        self.pretty_show_query(data)
        return dict_info_ctrc

    def _op048_liquidate_ctrc(self, html_t, **kwargs):
        query_model = ("act=ENV_FORMA_PGTO&valor_aliquidar=37%2C10&vlr_juros=0%2C00&vlr_liquido=37%2C10&data_pgto"
                       "=091023&creditar=T&forma_pgto=A&hidd_seq_ctrc=22462490&hidd_seq_fatura=0&hidd_ctrc=CGB593978"
                       "%2D0&hidd_fatura=&hidd_dtemiss=05%2F10%2F23&hidd_valor=%20%20%20%20%20%20%20%20%2037%2C10"
                       "&hidd_vcto=&hidd_cliente=251%2E503%2E778%2D05%20%2D%20RODRIGO%20FERRATO%20MELO"
                       "&hidd_valor_aliquidar=%20%20%20%20%20%20%20%20%2037%2C10&hidd_vlr_credito=0&hidd_vlr_debito=0"
                       "&cod_emp_ctb=1&dummy=1696884571139")
        data = self.update_query_values(html_t,
                                        query_model,
                                        'name',
                                        act='ENV_FORMA_PGTO',
                                        dummy='1687793128084',
                                        **kwargs)
        logging.info(data)
        self.pretty_show_query(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)

        # showing results

        logging.info(unquote(response.text))
        nro_acni = kwargs.pop('nro_acni')
        query_model = ("act=ENV_ACNI&nro_acni=0080825&param1=%3Fact%3D22462490&param2=%3Fact%3D0&hidd_seq_ctrc"
                       "=22462490&hidd_seq_fatura=0&hidd_ctrc=CGB593978%2D0&hidd_fatura=&hidd_cliente=251%2E503%2E778"
                       "%2D05%20%2D%20RODRIGO%20FERRATO%20MELO&hidd_dtemiss=05%2F10%2F23&hidd_vcto=&hidd_valor=%20%20"
                       "%20%20%20%20%20%20%2037%2C10&hidd_vlr_credito=0&hidd_vlr_debito=0&hidd_valor_aliquidar=%20%20"
                       "%20%20%20%20%20%20%2037%2C10&hidd_vlr_juros=0&hidd_vlr_desconto=0&hidd_vlr_pago=37%2C10"
                       "&hidd_data_pgto=09%2F10%2F23&hidd_creditar=T&hidd_forma_pgto=A&hidd_nsu=&hidd_tp_cartao"
                       "=&hidd_cod_adm=&hidd_cod_trans=&hidd_cod_emp=24&integracao_ok=&cod_emp_ctb=1&dummy"
                       "=1696885078924")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act='ENV_ACNI',
                                        nro_acni=nro_acni,
                                        dummy='1687793128084')
        logging.info(data)
        self.pretty_show_query(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)

        # showing results

        logging.info(unquote(response.text))

        query_model = ("act=LIQ_VIA_ACNI&creditar=T&forma_pgto=A&nro_acni=0081059-2&banco=341%2001433%20000024937"
                       "&data_credito=09/10/23&vlr_credito=39%2C90&vlr_saldo=39%2C90&motivo=PIX%20TRANSF%20DA"
                       "%20DIAS07/10&usuario=taticm%20%20%20MTZ%2010/10/23%2010%3A17&param1=%3Fact%3D22488059&param2"
                       "=%3Fact%3D0&hidd_seq_ctrc=22488059&hidd_seq_fatura=0&hidd_vlr_juros=0&hidd_vlr_desconto=0"
                       "&hidd_vlr_pago=39%2C90&hidd_data_pgto=11%2F10%2F23&hidd_vlr_credito=0&hidd_vlr_debito=0"
                       "&hidd_seq_acni=81059&hidd_seq_cliente_pag=1200192&dummy=1697028178850")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act='LIQ_VIA_ACNI',
                                        nro_acni=nro_acni,
                                        dummy='1687793128084')
        logging.info(data)
        self.pretty_show_query(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)

        # showing results


        text_html = unquote(response.text)
        logging.info(text_html)
        if 'CTRC faturado' not in text_html:

            query_model = ("act=&creditar=T&forma_pgto=A&nro_acni=0081059-2&banco=341%2001433%20000024937&data_credito=09"
                           "/10/23&vlr_credito=39%2C90&vlr_saldo=39%2C90&motivo=PIX%20TRANSF%20DA%20DIAS07/10&usuario"
                           "=taticm%20%20%20MTZ%2010/10/23%2010%3A17&param1=%3Fact%3D22488059&param2=%3Fact%3D0"
                           "&hidd_seq_ctrc=22488059&hidd_seq_fatura=0&hidd_vlr_juros=0&hidd_vlr_desconto=0&hidd_vlr_pago"
                           "=39%2C90&hidd_data_pgto=11%2F10%2F23&hidd_vlr_credito=0&hidd_vlr_debito=0&hidd_seq_acni=81059"
                           "&hidd_seq_cliente_pag=1200192&msgx=&dummy=1697028199993")
            data = self.update_query_values(unquote(response.text),
                                            query_model,
                                            'name',
                                            act='',
                                            nro_acni=nro_acni,
                                            dummy='1687793128084')
            logging.info(data)
            self.pretty_show_query(data)
            response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)

            # showing results

            logging.info(unquote(response.text))
        else:
            return  text_html

    def _op048_get_pix(self,html_text,*args,**kwargs):
        query_model = ("act=ENV_FORMA_PGTO&valor_aliquidar=49%2C50&vlr_juros=0%2C00&vlr_liquido=49%2C50&data_pgto=060524&creditar=T&forma_pgto=p&hidd_seq_ctrc=25511332&hidd_seq_fatura=0&hidd_ctrc=CGB226113%2D8&hidd_fatura=&hidd_dtemiss=29%2F04%2F24&hidd_valor=%20%20%20%20%20%20%20%20%2049%2C50&hidd_vcto=&hidd_cliente=26%2E182%2E093%2F0001%2D06%20%2D%20S%20C%20DOS%20SANTOS%20SILVA%20ME%20%2D%206112&hidd_valor_aliquidar=%20%20%20%20%20%20%20%20%2049%2C50&hidd_vlr_credito=0&hidd_vlr_debito=0&cod_emp_ctb=1&dummy=1715032229262")
        data = self.update_query_values(unquote(html_text),
                                        query_model,
                                        'name',
                                        act='ENV_FORMA_PGTO',
                                        forma_pgto='p',
                                        dummy=self.get_dummy())
        logging.info(data)
        self.pretty_show_query(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)
        logging.info(response.text)
        query_model = ("act=ENV_FORMA_PGTO&hidd_seq_ctrc=25511332&hidd_seq_fatura=0&hidd_ctrc=CGB226113%2D8&hidd_fatura=&hidd_dtemiss=29%2F04%2F24&hidd_valor=%20%20%20%20%20%20%20%20%2049%2C50&hidd_vcto=&hidd_cliente=26%2E182%2E093%2F0001%2D06%20%2D%20S%20C%20DOS%20SANTOS%20SILVA%20ME%20%2D%206112&hidd_valor_aliquidar=%20%20%20%20%20%20%20%20%2049%2C50&hidd_vlr_credito=0&hidd_vlr_debito=0&cod_emp_ctb=1&btn_5001=S&valor_aliquidar=49,50&vlr_juros=0,00&vlr_liquido=49,50&data_pgto=060524&creditar=T&forma_pgto=p&hidd_seq_ctrc=25511332&hidd_seq_fatura=0&hidd_ctrc=CGB226113-8&hidd_fatura=&hidd_dtemiss=29/04/24&hidd_valor=         49,50&hidd_vcto=&hidd_cliente=26.182.093/0001-06 - S C DOS SANTOS SILVA ME - 6112&hidd_valor_aliquidar=         49,50&hidd_vlr_credito=0&hidd_vlr_debito=0&cod_emp_ctb=1&dummy=1715032229262&remember=1&useri=12345678909&permissao=&ssw_dom=OTC&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTUwODk0MzEsInB4eSI6IjE3Mi4zMS41My4yNDcifQ.ecTXg01WYQ3GNHnzy8GcIeFig5Z6OePrsCdtDYmYlo8&dummy=1715032241862")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act='ENV_FORMA_PGTO',
                                        forma_pgto='p',
                                        btn_5001='s',
                                        dummy=self.get_dummy())
        logging.info(data)
        self.pretty_show_query(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)
        logging.info(response.text)
        return response.text

    def op048(self, *args, **kwargs):
        """
            :param args:
                - 'info_cnpj'
                - 'liquidate_cnpj' -> act = 'ENV_CNPJ'
                - 'liquidate_ctrc' -> act = 'ENV_CTRC'
                - 'pix' -> act = 'ENV_CTRC'
            :param kwargs:
            Possible keys include:
                - act: 'ENV_CNPJ', 'ENV_CTRC'
                - cod_emp_ctb: CNPJdoclientepagador:
                - f4: serie ctrc
                - f5: numero ctrc
                - f20: CNPJGrupo:
                - button_env_enable:
                - button_env_disable:
                - list_seq_fatura:
                - tot_liquid:
                - acni:
                - forma_pgto: (D-dinheiro,C-cartão,H-cheque,A-ACNI) -> 'liquidate_ctrc' -> act = 'ENV_CTRC'
                - nro_acni: ->'liquidate_ctrc' -> act = 'ENV_CTRC'
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '048'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV_CNPJ'
        query_model = ("act=ENV_CNPJ&cod_emp_ctb=01&f4=bga&f5=5888867&f20=89674782001391&button_env_enable=ENV_BAR"
                       "&button_env_disable=2&dummy=1691420015506")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0126", headers=self.headers, data=data)

        # showing results

        logging.info(unquote(response.text))

        if 'info_cnpj' in args:
            return self._op048_get_table(response.text)

        if 'liquidate_cnpj' in args:
            self._op048_liquidate(kwargs['list_seq_fatura'], kwargs['tot_liquid'], kwargs['acni'])

        if 'info_ctrc' in args:
            return self._op048_get_info_ctrc(unquote(response.text), **kwargs)

        if 'liquidate_ctrc' in args:
            return self._op048_liquidate_ctrc(response.text, **kwargs)
        if 'pix' in args:
            return self._op048_get_pix(response.text, **kwargs)


if __name__ == '__main__':
    with Ssw048() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op048('info_ctrc')
