from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw206(SswRequest):
    def __init__(self):
        super().__init__()

    def op206(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - t_sigla: unidade
                - t_dia: data
                - t_hora: hora
                - t_xml: (S-sim,N-não,A-ambos)
                - t_ctrc: (S-sim,N-não,A-ambos)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '206'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1988", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&t_sigla=MTZ&t_dia=180823&t_hora=0001&t_xml=A&t_ctrc=N&dummy=1692386996200"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1988", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw206() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op206()
