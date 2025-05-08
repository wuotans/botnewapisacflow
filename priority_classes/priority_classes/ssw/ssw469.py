from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw469(SswRequest):
    def __init__(self):
        super().__init__()

    def op469(self, *args, **kwargs):
        """
            :param args:
                - 'get_table','update_table'
            :param kwargs:
            Possible keys include:
                - act:
                - unid: unidade
                - uf: UF
                - col1: Desc max NTC
                - col2: Result comerc minimo
                - col3: Desc max cotac inicial
                - col4: Frete valor minimo
                - col5: Frete peso minimo
                - col6: Frete minimo
                - list_seq_to_update: list of sequences in the html table
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '469'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        self.session.post("https://sistema.ssw.inf.br/bin/ssw0188", headers=self.headers, data=data)

        # showing results

        # logging.info(response.text)

        # query filters to request record
        data = f"act=CON&unid={kwargs['unid']}&uf={kwargs['uf']}&dummy={self.get_dummy()}"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0188", headers=self.headers, data=data)

        html_base = response.text


        logging.info(response.text)
        if 'get_table' in args:
            return self.get_table(html_base, 10)

        if 'update_table' in args:
            query_seq = 'act=SRENV'
            for seq in kwargs['list_seq_to_update']:
                query_seq = query_seq + f"|{seq}@{kwargs['col1']}@{kwargs['col2']}@{kwargs['col3']}@{kwargs['col4']}@{kwargs['col5']}@{kwargs['col6']}"

            logging.info(query_seq)

            # query filters to request record
            data = ("=0%2C00&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01"
                    "&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01"
                    "&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01&=0%2C01")
            query_model = "BSIQ=CGB&BEST=PA&BTAM=25&msgx=&dummy=1698675896839"
            query = self.update_query_values(html_base,
                                             query_model,
                                             'name',
                                             dummy=self.get_dummy())
            data = query_seq + '&' + data + '&' + query
            logging.info(data)
            self.session.post("https://sistema.ssw.inf.br/bin/ssw0188",
                              headers=self.headers,
                              data=data)

            # query filters to request record
            data = ("act=&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0"
                    "%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00"
                    "&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0"
                    "%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00"
                    "&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0"
                    "%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00"
                    "&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20"
                    "%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00"
                    "&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0"
                    "%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00&=0%2C00&=0%2C00&=0%2C00&=20%2C00"
                    "&=20%2C00&=0%2C00&=20%2C00&=20%2C00&=20%2C00&=20%2C00")
            query_model = "BSIQ=CGB&BEST=PA&BTAM=25&msgx=&dummy=1698675896839"
            query = self.update_query_values(html_base,
                                             query_model,
                                             'name',
                                             dummy=self.get_dummy())
            data = data + '&' + query
            logging.info(data)
            self.session.post("https://sistema.ssw.inf.br/bin/ssw0188",
                              headers=self.headers,
                              data=data)

        # self.handle_download(response.text)


if __name__ == '__main__':
    with Ssw469() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op469()
