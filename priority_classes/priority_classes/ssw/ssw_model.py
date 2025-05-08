from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw_(SswRequest):
    def __init__(self):
        super().__init__()

    def model(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = 'op'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw...", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ATALHO_IMP&seq_ctrc=21263102&FAMILIA=&dummy=1688659540624"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw....", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
