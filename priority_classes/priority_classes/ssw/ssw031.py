from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw031(SswRequest):
    def __init__(self):
        super().__init__()

    def op031(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f1: periodo emissão do ctrc data ini
                - f2: periodo emissão do ctrc data fim
                - f3: data inicial da ocorrencia
                - f4: data final da ocorrencia
                - f6: codigo da ocorrencia:
                - f8: cnpj cliente pagador
                - f10: conferente
                - f11: situação atual do ctrc (B-baixado,P-pendente,T-todos)
                - f12: arquivo em excel (S/N)
                - programa:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '031'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0495", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = ("act=ENV&f3=020823&f4=030823&f6=67&ocor_descr=FRETE%20PAGO&f11=T&f12=s&programa=ssw0495&dummy"
                       "=1691066970659")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0495", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw031() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op031(f1='011223',f2='011223',f6='33')
