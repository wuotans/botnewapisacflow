from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw457(SswRequest):
    def __init__(self):
        super().__init__()

    def _op457_I90(self,html_text,cod_instrucao,*args,**kwargs):
        query_model = "act=I90&f1=90&sequencia=457&seq_fatura=2461743&ler_arq_morto=S&dummy=1701259424276"
        act = f'I{cod_instrucao}'
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        f1=cod_instrucao,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response3 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response3.text)

        query_model = ("act=I90&sequencia=457&seq_fatura=2461743&ler_arq_morto=S&sequencia=457&btn_50=S&f1=90"
                       "&seq_fatura=2461743&ler_arq_morto=S&dummy=1701259424276&remember=1&ssw4importa=S&useri"
                       "=12345678909&lastcnpj_cotacao=&sacflow-connect-version=3.10.0&permissao=&zera=false"
                       "&lista_ctrc=&listacnpj=&unidade_ssw=MTZ&extensao=29/11/2023&ssw_dom=OTC&token"
                       "=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDEzNDE4MTYsInB4eSI6IjE3Mi4zMS41My4yNDcifQ"
                       ".wfCkkSVpg3wUNdqdTZJJVId-pvaSEp0f-ND_ovMOcFA&dummy=1701259497755")

        data = self.update_query_values(response3.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        f1=cod_instrucao,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response3 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response3.text)

    def _op457_A88(self,html_text,cod_instrucao,*args,**kwargs):
        query_model = "act=I88&f1=88&sequencia=457&seq_fatura=2461743&ler_arq_morto=S&dummy=1701259424276"
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=f'I{cod_instrucao}',
                                        f1=cod_instrucao,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response3 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response3.text)
        # query_model = "act=A88&vlr_saldo=50%2C00&f4=50%2C00&f5=170424&f12=341&f13=01433&f14=1&f15=000024937&f16=0&sequencia=457&seq_fatura=2637499&ler_arq_morto=S&dummy=1713371052488"
        #
        # data = self.update_query_values(response3.text,
        #                                 query_model,
        #                                 'name',
        #                                 act=act,
        #                                 dummy=self.get_dummy(),
        #                                 **kwargs)
        # logging.info(data)
        # response3 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)
        #
        # # showing results
        #
        # logging.info(response3.text)
        query_model = "act=A88&sequencia=457&seq_fatura=2644094&ler_arq_morto=S&sequencia=457&inp_98=1234&vlr_saldo=520,75&f4=520,75&f5=160424&f12=341&f13=01433&f14=1&f15=000024937&f16=0&seq_fatura=2644094&ler_arq_morto=S&dummy=1713291733156&remember=1&ssw4importa=S&lastcnpj_cotacao=&useri=12345678909&permissao=&ssw_dom=OTC&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTMzNTQ2NTIsInB4eSI6IjE3Mi4zMS41My4yNDcifQ.IuFfnvlPssaMfDy_1tlPGa7BkgTtynf9f2prht6MSYU&dummy=1713291745165"

        data = self.update_query_values(html_text + response3.text,
                                        query_model,
                                        'name',
                                        act=f'A{cod_instrucao}',
                                        f1=cod_instrucao,
                                        inp_98=kwargs['nro_acni'],
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response3 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response3.text)

    def _op457_instructions(self,html_text,*args,**kwargs):
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'INS'
        query_model = ("act=INS&sequencia=457&ler_arq_morto=S&data0_ini=01012000&data0_fin=31122090&parcelada"
                       "=&seq_fatura=2461743&local=Q&dummy=1701259345588")
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response2 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response2.text)

        # query filters to request record
        cod_instrucao = kwargs.pop('cod_instrucao') if 'cod_instrucao' in kwargs else None

        if cod_instrucao == '90':
            self._op457_I90(response2.text,cod_instrucao,*args,**kwargs)

        if cod_instrucao =='88':
            self._op457_A88(response2.text, cod_instrucao, *args, **kwargs)


    def _op457_occurrences(self,html_text,*args,**kwargs):
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'OCO'
        query_model = ("act=OCO&sequencia=457&ler_arq_morto=S&data0_ini=01012000&data0_fin=31122090&parcelada=&seq_fatura=2618706&local=Q&dummy=1712582493803")
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response2 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        logging.info(response2.text)
        table = self.get_table(response2.text,6)
        logging.info(table)
        #table.to_excel('ssw457_indexes.xlsx')
        return table

    def op457(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - t_nro_fatura: Fatura(codbar):
                - t_data_pes_ini: a
                - t_data_pes_fin: CNPJdopagador:
                - t_nao_liqui1: (nãoliquidado)
                - t_liqui1: (liquidado)
                - t_nao_liqui2: (nãoliquidado)
                - t_liqui2: (liquidado)
                - t_nao_liqui3: (nãoliquidado)
                - t_liqui3: (liquidado)
                - cod_instrucao: code of general instructions option if 'instructions' in args
                - nro_acni: number of acni
                - sequencia:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '457'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'NRO'
        query_model = ("act=NRO&t_nro_fatura=2201338&t_data_pes_ini=310823&t_data_pes_fin=291123&t_nao_liqui1=X"
                       "&t_liqui1=X&t_nao_liqui2=X&t_liqui2=X&t_nao_liqui3=X&t_liqui3=X&sequencia=457&dummy"
                       "=1701259227781")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response1 = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response1.text)
        if 'instructions' in args:
            self._op457_instructions(response1.text,*args,**kwargs)

        if 'occurrences' in args:
            return self._op457_occurrences(response1.text,*args,**kwargs)





if __name__ == '__main__':
    with Ssw457() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op457()
