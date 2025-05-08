from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw536(SswRequest):
    def __init__(self):
        super().__init__()

    def op536(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f2: (opcional)
                - f4: (opcional)
                - f6: (opcional)
                - f7: (S/N)
                - f8: a
                - f9: (Máximo31dias)
                - f10: a
                - f11: (Máximo31dias)
                - f14: (S/N)
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = 'op'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0324", headers=self.headers, data=data)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else '@E'
        query_model = "act=@E&f2=1&f4=2&f6=3&f7=S&f8=010623&f9=020623&f10=010623&f11=020623&f14=N&dummy=1687985695134"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0324", headers=self.headers, data=data)

        self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw536() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op536()
