from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw103(SswRequest):
    def __init__(self):
        super().__init__()

    def op103(self, *args, **kwargs):
        """
        :param kwargs:
        Possible keys include:
            - act:
            - f2: Unidadedecoleta(opc):
            - f14: a
            - f15: Pordatade:
            - f16: (C-coleta,I-inclusão,L-limite)
            - f17: (V-vídeo,R-relatório,E-excel)
            - f34: a
            - f35: Pordatade:
            - f36: (C-coleta,I-inclusão,L-limite)
            - f37: (V-vídeo,R-relatório,E-excel)
        :type kwargs: dict
        :return: None
        """
        self.last_opssw = '103'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0166", headers=self.headers, data=data)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'FIL_COL'
        query_model = ("act=FIL_COL&f2=OTC&f14=050723&f15=050723&f16=i&f17=e&f34=050723&f35=050723&f36=L&f37=V&dummy"
                       "=1688584613002")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0166",
                                     headers=self.headers,
                                     data=data)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw103() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op103(f14='301123',f15='301123',f17='E')
