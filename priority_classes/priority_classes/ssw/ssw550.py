from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw550(SswRequest):
    def __init__(self):
        super().__init__()

    def op550(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f2: unidade
                - f3: tipo unidade (E-expedidora,R-receptora,P-unidaderesponsáveldopagador)
                - f5: cnpj:
                - f6: considerar (T-todos,X-todosmenososcancelados,C-Cancelados)
                - f7: periodo autorização inicial
                - f8: periodo autorização final
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '550'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1666", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("act=ENV&f3=P&f5=59105999002804&cliente=WHIRLPOOL%20S.A.&f6=T&f7=010823&f8=100823&web_body"
                       "=&dummy=1691697143594")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy='1687793128084',
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1666", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        if 'Nenhum registro encontrado para os par&acirc;metros informados.' not in response.text:
            self.handle_download(response.text, **kwargs)


if __name__ == '__main__':
    with Ssw550() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op550(f5='59105999002804',f7='251123',f8='011223')
