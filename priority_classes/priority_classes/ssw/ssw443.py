from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw443(SswRequest):
    def __init__(self):
        super().__init__()

    def op443(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '443'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0076", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&f2=237&f3=02647&f4=6&f5=2460&f6=0%20&f7=009&nomebanco=BRADESCO%20S.A.&f8=160424&f16=R&dummy=1713295892857"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0076", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        if 'N&atilde;o ha instrucoes' not in response.text and 'N&atilde;o existem faturas e instru&ccedil;' not in response.text:
            self.handle_download(response.text)
            return True
        return False


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
