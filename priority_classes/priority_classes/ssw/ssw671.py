from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw671(SswRequest):
    def __init__(self):
        super().__init__()

    def op671(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
                - t_ser_ctrc:
                - t_nro_ctrc:
                - if_many_filter_ctrc_by_value:dict {'col':'value'}
                - t_comissao_expedicao:
                - t_comissao_recepcao:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '671'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw3003", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'CTRC'
        query_model = "act=CTRC&t_ser_ctrc=nat&t_nro_ctrc=5930570&dummy=1698679298779"
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw3003", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        if 'CTRC n&atilde;o encontrado.' in response.text:
            return 'CTRC não encontrado'
        else:
            # Verifica quando tem multiplos ctrcs e seleciona aquele conforme o parametro if_many_filter_ctrc_by_value
            ctrcs_available = self.get_table(response.text,9)
            ctrcs_available = ctrcs_available[ctrcs_available['<f0>'].str.strip().str.len()>6].reset_index(drop=True)
            value_fil = kwargs.pop('if_many_filter_ctrc_by_value','')
            ctrcs_available = self.filter_df_by_values(ctrcs_available,value_fil)
            logging.info(ctrcs_available)
            if not ctrcs_available.empty:
                logging.info('Existem multiplos ctrcs selecionando conforme filtro!')
                query_model = ("act=CTRC&btn_1=27405589&t_ser_ctrc=mlv&t_nro_ctrc=0023981&dummy=1728481119821&remember=1&ssw4importa=S&lastcnpj_cotacao=&useri=12345678909&sacflow-connect-login=%7B%22vers%C3%A3o%22%3A%223%2E13%2E54%22%2C%22data%22%3A%2209%2F10%2F2024%2009%3A10%3A35%22%7D&permissao=&ssw_dom=OTC&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9%2EeyJleHAiOjE3Mjg1NjIyMzYsInB4eSI6IjE3Mi4zMS41My4yNDcifQ%2EpcLOI6yRvrDE_wjT_8l_YQSZyyxuw60bvMAfispc9Xc&dummy=1728481472263")
                data = self.update_query_values(response.text,
                                                query_model,
                                                'name',
                                                act='CTRC',
                                                btn_1=ctrcs_available.loc[0,'<f8>'],
                                                dummy=self.get_dummy(),
                                                **kwargs)
                logging.info(data)
                response = self.session.post("https://sistema.ssw.inf.br/bin/ssw3003", headers=self.headers, data=data)
                logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'ALT'
        query_model = ("act=ALT&t_comissao_expedicao=0%2C00&t_comissao_recepcao=6%2C00&seq_ctrc=22601077&dummy"
                       "=1698679495034")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw3003", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        return response.text


if __name__ == '__main__':
    with Ssw671() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op671()
