from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw915(SswRequest):
    def __init__(self):
        super().__init__()

    def op915(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f1: (C-CTRC,F-fatura)
                - f4: periodo inicial autorização
                - f5: periodo final autorização
                - f8: (R-remetende,D-destinatário,P-pagador,T-todos)
                - f11: (E-expedidora,R-recebedora,A-ambas)
                - f12: (S/N)
                - f13: (L-liquidado,P-pendente,A-ambos)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '915'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0261", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&f1=C&f4=130823&f5=130823&f8=T&f11=A&f12=S&f13=A&dummy=1692037311088"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0261", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw915() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op915()
