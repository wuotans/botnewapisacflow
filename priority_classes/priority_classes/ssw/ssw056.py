from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw056(SswRequest):
    def __init__(self):
        super().__init__()

    def _op056_get_table(self, html):
        return self.get_table(html, 7)

    def op056(self, *args, **kwargs):
        """
             :param kwargs:
             Possible keys include:
                 - act:
                 - f1: codigo
                 - index: posicao do relatorio para baixar, default 1
             :type kwargs: dict
             :return: None
         """
        self.last_opssw = '056'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        self.session.post("https://sistema.ssw.inf.br/bin/ssw0082", headers=self.headers, data=data)

        # showing results

        # logging.info(response.text)

        # query filters to request record
        data = "act=FIL&dummy=1694204327112"
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0082", headers=self.headers, data=data)

        # showing results

        # logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'FILCOD'
        query_model = "act=FILCOD&f1=201&dummy=1694204410776"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0082", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        index = int(kwargs.pop('index')) if 'index' in kwargs else 1
        table = self._op056_get_table(response.text)
        table.to_excel('ssw056_indexes.xlsx')
        logging.info(table)
        seq = table.loc[index, '<f6>']
        logging.info(seq)

        # query filters to request record
        data = f"act={seq}&dummy=1694204470624"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0082", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw056() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op056()
