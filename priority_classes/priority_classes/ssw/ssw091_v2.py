from priority_classes.ssw.ssw_v2 import SswRequest
import logging

class Ssw091(SswRequest):
    def __init__(self,name_instance='ssw091', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance

    def op091(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f1:
                - f2:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '091'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0783", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=ENV&f1=ca1&f2=4951280&dummy=1721917209601"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0783", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        return self


if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
