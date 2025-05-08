from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw306(SswRequest):
    def __init__(self):
        super().__init__()

    def op306(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - t_data_busca: a
                - t_data_busca2:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '306'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1379", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV_RELATORIO'
        query_model = "act=ENV_RELATORIO&t_data_busca=180823&t_data_busca2=180823&dummy=1692387366353"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1379", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw306() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op306()
