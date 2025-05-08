from urllib.parse import unquote
from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw149(SswRequest):
    def __init__(self):
        super().__init__()

    def op149(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '149'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1503", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        data = f"act=CONF&f7=T&apenas_descarregados=S&dummy={self.get_dummy()}"
        response2 = self.session.post("https://sistema.ssw.inf.br/bin/ssw1503", headers=self.headers, data=data)

        act = kwargs.pop('act') if 'act' in kwargs else 'ENT'
        query_model = ("act=ENT&f7=T&apenas_descarregados=S&inicio_conf=botcvl%2023%2F11%2F23%2017%3A08&dummy"
                       "=1700770114872")
        data = self.update_query_values(response2.text, query_model, 'name', act=act, dummy=self.get_dummy(),
                                        **kwargs)
        response3 = self.session.post("https://sistema.ssw.inf.br/bin/ssw1503", headers=self.headers, data=data)



        act = kwargs.pop('act') if 'act' in kwargs else 'FIN'
        query_model = ("act=FIN&f7=T&apenas_descarregados=S&inicio_conf=botcvl%2023%2F11%2F23%2017%3A08&web_body"
                       "=&dummy=1700770123287")
        data = self.update_query_values(response2.text, query_model, 'name', act=act, dummy=self.get_dummy(),
                                        **kwargs)
        response4 = self.session.post("https://sistema.ssw.inf.br/bin/ssw1503", headers=self.headers, data=data)

        act = kwargs.pop('act') if 'act' in kwargs else 'FIN'
        query_model = ("act=FIN&inicio_conf=botcvl%2023%2F11%2F23%2017%3A08&btn_61=S&f7=T&apenas_descarregados=S"
                       "&inicio_conf=botcvl 23/11/23 "
                       "17:08&dummy=1700770123287&remember=1&ssw4importa=S&useri=12345678909&lastcnpj_cotacao"
                       "=&sacflow-connect-version=3.9.25&permissao=&zera=false&lista_ctrc=&listacnpj=&extensao=23/11"
                       "/2023&ssw_dom=OTC&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                       ".eyJleHAiOjE3MDA4NDkyNTgsInB4eSI6IjE3Mi4zMS41My4yNDcifQ.xcI77hUG8rXTgfOQdRCsM54RUJgx"
                       "--v4x2954bo3clg&unidade_ssw=CGB&dummy=1700770124880")
        data = self.update_query_values(response4.text,
                                        query_model, 'name',
                                        act=act,
                                        btn_61='S',
                                        dummy=self.get_dummy(),
                                        unquote=True,
                                        **kwargs)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1503", headers=self.headers,
                                     data=f'{unquote(data)}&dummy={self.get_dummy()}')

        # showing results
        logging.info(response.text)

        self.handle_download(response3.text)


if __name__ == '__main__':
    with Ssw149() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.credentials[4]='cgb'
        ssw.op149()
