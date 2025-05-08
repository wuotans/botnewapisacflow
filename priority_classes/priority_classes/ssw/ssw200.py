from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw200(SswRequest):
    def __init__(self):
        super().__init__()

    def op200(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - f1: data ini
                - f2: data fim
                - f4: unidade origem
                - f6: unidade destino
                - f11: (T-texto,E-excel)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '200'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0644", headers=self.headers, data=data)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&f1=010723&f2=060723&f4=cgb&f6=sao&f11=e&dummy=1688644085169"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0644",
                                     headers=self.headers,
                                     data=data)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw200() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op200(f1='011223',f2='011223')
