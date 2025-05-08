from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw454(SswRequest):
    def __init__(self):
        super().__init__()

    def op454(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f7: a
                - f8: Períododeativação:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '454'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0169", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'PER'
        query_model = "act=PER&f7=011223&f8=071223&dummy=1701958230757"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0169", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        if 'info' in args:
            return self.get_table(response.text,8)


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
