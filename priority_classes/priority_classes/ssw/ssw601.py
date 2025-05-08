from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw601(SswRequest):
    def __init__(self):
        super().__init__()

    def op601(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '601'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0752", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("act=ENV&col1=Codigo%20IBGE&col2=Nome%20da%20cidade&col3=UF%20da%20cidade&col4=Praca"
                       "%20Comercial&col5=Sigla%20da%20praca&col6=Sigla%20da%20unidade&cnpj=&dummy=1701376570225")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0752", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw601() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op601()
