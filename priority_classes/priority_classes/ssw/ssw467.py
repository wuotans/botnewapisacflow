from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw467(SswRequest):
    def __init__(self):
        super().__init__()

    def op467(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - data_ult_ini: a
                - data_ult_fin: (opcional)
                - classificacao: (E-especial,C-comum,T-todos)
                - credito: (V-àvista,B-banco,C-carteira,T-todos)
                - transportar: (S-sim,V-sim,àvista,N-não,T-todos)
                - protesta: (S-sim,N-não,T-todos)
                - ent_dificil: (S-sim,N-não,T-todos)
                - faturamento: (A-automático,M-manual,T-todos)
                - servico: ICMSnatabela:
                - icms: (S-sim,N-não,T-todos)
                - rcfdc: (S-sim,N-não,T-todos)
                - desconto: (S/N)
                - canhoto: (S-sim,N-não,T-todos)
                - tab_frete: (C-com,S-sem,T-todos)
                - tipo: (J-pessoajurídica,F-pessoafísica,T-todos)
                - excel: (S/N)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '467'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0176", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'GER'
        query_model = ("act=GER&data_ult_ini=010119&data_ult_fin=180823&classificacao=T&credito=T&transportar=T"
                       "&protesta=T&ent_dificil=T&faturamento=T&servico=T&icms=T&rcfdc=T&desconto=N&canhoto=T"
                       "&tab_frete=T&tipo=T&excel=s&dummy=1692385970840")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0176", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw467() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op467(data_ult_ini='301123',data_ult_fin='011223', excel='s')
