from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw434(SswRequest):
    def __init__(self):
        super().__init__()

    def op434(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f1: dominio
                - f3: cnpj

            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '434'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1486", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("act=ENV&f1=men&f3=20121850003251&dominio=MERCADO%20ENVIOS%20SERVICOS%20DE%20LOGISTICA%20LTDA"
                       "&nome_cli=MERCADO%20ENVIOS%20SERVICOS%20DE%20LOG&dummy=1693250871294")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1486", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)


if __name__ == '__main__':
    with Ssw434() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op434()
