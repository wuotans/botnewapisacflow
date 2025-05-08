from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw583(SswRequest):
    def __init__(self):
        super().__init__()

    def op583(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '583'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0662", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'IMP_EXC'
        query_model = "act=IMP_EXC&dummy=1693248197170"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0662", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw583() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op583()
