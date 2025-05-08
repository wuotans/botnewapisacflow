from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw104(SswRequest):
    def __init__(self):
        super().__init__()

    def _op104_download_invoice(self, invoice, name_file, **kwargs):
        # query filters to request record
        data = f"act=IMP&ler_morto=N&chamador=ssw0183&nro_fat_ini={invoice}&dummy=1695990910673"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw2701", headers=self.headers, data=data)
        logging.info(response.text)
        self.handle_download(response.text, name_file=name_file)

    def op104(self, *args, **kwargs):
        """
            :param args:
                - 'download_invoice'
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
                - sequencia:
                - name_file: nome do arquivo (Opcional)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '104'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'NRO'
        query_model = ("act=NRO&t_nro_fatura=2047387&t_data_pes_ini=010723&t_data_pes_fin=290923&t_nao_liqui1=X"
                       "&t_liqui1=X&t_nao_liqui2=X&t_liqui2=X&t_nao_liqui3=X&t_liqui3=X&sequencia=104&dummy"
                       "=1695990869916")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        self.session.post("https://sistema.ssw.inf.br/bin/ssw0183", headers=self.headers, data=data)

        if 'download_invoice' in args:
            name_file = kwargs.pop('name_file') if 'name_file' in kwargs else str(kwargs['t_nro_fatura']) + '.pdf'
            self._op104_download_invoice(kwargs['t_nro_fatura'], name_file)


if __name__ == '__main__':
    with Ssw104() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op104()
