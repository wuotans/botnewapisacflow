from priority_classes.ssw.ssw import SswRequest
from urllib.parse import unquote
import logging

class Ssw388(SswRequest):
    def __init__(self):
        super().__init__()

    def op388(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - f2: cnpj
            Possible keys include:
                    - unid_cli_como_dest: unidade destino
                    - fg_gerar_cod_barras: (S/N)
                    - qtde_cnpj: (0-14)
                    - qtde_serie_nf: (0-3)
                    - qtde_dig_nf: (6-9)
                    - qtde_dig_vol: (0-4)
                    - fg_usa_cubadora_balanca: (P-peso,C-cubagem,A-ambos,N-nenhum)
                    - fg_usa_logistica: (N-não,A-armazém,L-operadorlogístico)
                    - fg_vinc_nf_entrada: (S/N)
                    - st_icms: STISS:
                    - t_emite_rps_prov: (S/N)
                    - a_dias_adic: dianoiniciodatransferência.
                    - a_exige_recebedor: (S/N)
                    - cnpj:
                    - nome:
                    - seq_cliente:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '388'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0843", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&f2=11554424151&dummy=1692621240471"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy='1692621240471',
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0843", headers=self.headers, data=data)

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'EN2'
        query_model = ("act=EN2&unid_cli_como_dest=STG&unidest=STG%20-%20UNID%20SANTIAGO%20DO%20NORTE"
                       "&fg_gerar_cod_barras=N&qtde_cnpj=0&qtde_serie_nf=0&qtde_dig_nf=9&qtde_dig_vol=4"
                       "&fg_usa_cubadora_balanca=N&fg_usa_logistica=N&fg_vinc_nf_entrada=N&st_icms=0&t_emite_rps_prov"
                       "=N&a_dias_adic=1&a_exige_recebedor=N&cnpj=00011554424151&nome"
                       "=ARTHURLIMADATRINDADEABDHECFGBFGA%20%2E%2E&seq_cliente=2312067&dummy=1692621300439")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy='1692621300439',
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0843", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)


if __name__ == '__main__':
    with Ssw388() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op388()
