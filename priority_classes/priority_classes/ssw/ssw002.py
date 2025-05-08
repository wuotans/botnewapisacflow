from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw002(SswRequest):
    def __init__(self):
        super().__init__()

    def _op002_get_report(self,html_text, *args, **kwargs):
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'PES'
        query_model = "act=PES&f6=e&f7=T&f8=T&f9=N&f17=070623&f18=070723&dummy=1688732484473"
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1601",
                                     headers=self.headers,
                                     data=data)

        self.handle_download(response.text)

    def _op002_get_cotation_info(self, html_text, *args, **kwargs):
        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'NUM'
        query_model = "act=NUM&f3=2659023&f6=V&f7=T&f8=T&f9=N&f17=280224&f18=280324&dummy=1711634275379"
        data = self.update_query_values(html_text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1601",
                                     headers=self.headers,
                                     data=data)
        logging.info(response.text)
        return  response.text

    def op002(self, *args, **kwargs):
        """
            :param args:
                - 'report'
                - 'info'
            :param kwargs:
            Possible keys include:
                - act:
                - f3: Num cotação
                - f6: (V-vídeo,R-relatório,E-excel)
                - f7: (C-CIF,F-FOB,T-todos)
                - f8: (C-cotada,D-cancelada,F-contratada,E-CTRCemitido,K-cotadacliente,T-todos)
                - f9: (S/N)
                - f17: a
                - f18:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '002'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1601", headers=self.headers, data=data)

        if 'report' in args:
            self._op002_get_report(response.text, *args, **kwargs)

        if 'info' in args:
            return self._op002_get_cotation_info(response.text, *args, **kwargs)


if __name__ == '__main__':
    with Ssw002() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op002(f6='e')
