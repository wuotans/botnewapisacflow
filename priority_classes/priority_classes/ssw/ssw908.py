from priority_classes.ssw.ssw import SswRequest
from urllib.parse import unquote
import logging


class Ssw908(SswRequest):
    def __init__(self):
        super().__init__()

    def op908(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - f2:
                - occur_ssw: Dictionary with occur ssw as key and a list of ('S' or 'N') for "envia" and "finalizadora" parameters eg.{'69':['S','N']}
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '908'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0185", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'CTRC'
        query_model = "act=CTRC&f2=3007331000818&web_body=&dummy=1711459640631"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0185", headers=self.headers, data=data)

        logging.info(response.text)

        params = self.get_input_values_from_html(unquote(response.text))
        logging.info(params)
        data = params['web_body'].split('?')[1].replace(");",'')
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1949", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        df = self.get_table(response.text,18)
        df = df[ df['<f0>'].str.len()>0].reset_index(drop=True)
        df.to_excel('ssw908.xlsx')

        act = ("SRENV|1@#@#|2@#@#|3@#@#|4@#@#|5@#@#|0@#@#|0@#@#|10@#@#|11@#@#|13@#@#|14@#@#|15@#@#|16@#@#|18@#@#|19@#@#|"
             "20@#@#|0@#@#|0@#@#|0@#@#|0@#@#|26@#@#|27@#@#|0@#@#|0@#@#|31@#@#|32@#@#|33@#@#|34@#@#|35@#@#|36@#@#|37@#@#|"
             "38@#@#|39@#@#|40@#@#|45@#@#|48@#@#|49@#@#|50@#@#|51@#@#|52@#@#|53@#@#|54@#@#|0@#@#|56@#@#|57@#@#|58@#@#|"
             "59@#@#|60@#@#|61@#@#|0@#@#|63@#@#|0@#@#|0@#@#|69@#@#|70@#@#|0@#@#|0@#@#|0@#@#|0@#@#|0@#@#|0@#@#|0@#@#|"
             "78@#@#|79@#@#|80@#@#|82@#@#|83@#@#|84@#@#|85@#@#|0@#@#|0@#@#|88@#@#|0@#@#|91@#@#|92@#@#|93@#@#|94@#@#|"
             "95@#@#|99@#@#")

            # The first parameter to consider to update the values of act parameter is kwargs
        for key in kwargs['occur_ssw']:
            act_key = f'|{key}@#@#'
            act_key_u = f"|{key}@{'@'.join(kwargs['occur_ssw'][key])}"
            logging.info(act_key, act_key_u)
            act = act.replace(act_key, act_key_u)

        for i, occur in enumerate(df['<f16>']):
            occur = occur.replace('>','')
            act_key = f'|{occur}@#@#'
            act_key_u = f"|{occur}@{df.loc[i,'<f2>']}@{df.loc[i,'<f3>']}"
            logging.info(act_key,act_key_u)
            act = act.replace(act_key, act_key_u)


        logging.info(act)
        query_model = ("act=&cliente_orig=03007331000818&seq_cliente=1158768&cliente_cgc=03007331000818&"
                       "cliente_nome=EBAZAR%2ECOM%2EBR%2E%20LTDA&dummy=1711460223847")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy())
        logging.info(unquote(data))
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1949", headers=self.headers, data=unquote(data))

        logging.info(response.text)
        if 'Altera&ccedil;&otilde;es realizadas com sucesso.' in response.text:
            return True
        return False




if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
