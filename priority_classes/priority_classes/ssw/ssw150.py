from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw150(SswRequest):
    def __init__(self):
        super().__init__()

    def op150(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f1: data inicial
                - f2: data final
                - f7: tipo unidade (E-expedidora,R-recebedora)
                - f8: excel (S/N)
                - f9: mostrar localização atual (S/N)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '150'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0861", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&f1=010101&f2=250823&f7=R&f8=s&f9=N&dummy=1692979762890"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0861", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw150() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op150()
