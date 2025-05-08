from priority_classes.ssw.ssw import SswRequest
from bs4 import BeautifulSoup
import logging


class Ssw403(SswRequest):
    def __init__(self):
        super().__init__()

    def _op403_post_route(self,html_content,**kwargs):
        query_model = "act=ENV&f2=cgb&f4=mdt&dummy=1704894555890"
        data = self.update_query_values(html_content,
                                        query_model,
                                        'name',
                                        act='ENV',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0241", headers=self.headers, data=data)
        logging.info(response.text)
        return response.text

    def _op403_extract_seq(self,html_content):
        df = self.get_table(html_content,12)
        logging.info(df)
        logging.info(df.loc[1,'<f11>'])
        return df.loc[1,'<f11>'].replace('>','')

    def _op403_select_route(self,html_content,**kwargs):
        act = self._op403_extract_seq(html_content)
        query_model = "act=PES|44|15&sigla_emit=CGB&sigla_dest=MDT&dummy=1704894784988"
        data = self.update_query_values(html_content,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0241", headers=self.headers, data=data)
        logging.info(response.text)
        return response.text

    def _op403_select_smp(self,html_content,**kwargs):
        act = kwargs.pop('act') if 'act' in kwargs else 'ENV'
        query_model = "act=R_SMP&sigla_central=CGB&distancia=298&prazo_transf=0&horas_transferencia=6&qtde_pedagio=0&vlr_transf_com=44%2C70&sigla_emit=CGB&sigla_dest=MDT&cod_fil_emit=44&cod_fil_dest=15&dummy=1704894942839"
        data = self.update_query_values(html_content,
                                        query_model,
                                        'name',
                                        act='R_SMP',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0241", headers=self.headers, data=data)
        logging.info(response.text)
        return response.text

    def _op403_insert_info_route_smp(self,html_content,**kwargs):
        query_model = "act=ENV_SMP&f2=05&f3=21205&f4=CBA%20X%20CPV%20-%20CARVALIMA%20HOJE&cod_fil_emit=44&cod_fil_dest=81&sigla_emit=CGB&sigla_dest=CPV&dummy=1704895302158"
        data = self.update_query_values(html_content,
                                        query_model,
                                        'name',
                                        act='ENV_SMP',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0241", headers=self.headers, data=data)
        logging.info(response.text)

    def _op403_insert_info_route_smp_confirm(self,html_content,**kwargs):
        query_model = "act=&f2=05&f3=21205&f4=CBA%20X%20CPV%20-%20CARVALIMA%20HOJE&cod_fil_emit=44&cod_fil_dest=81&sigla_emit=CGB&sigla_dest=CPV&act=R_SMP&msgx=&dummy=1704895302256"
        data = self.update_query_values(html_content,
                                        query_model,
                                        'name',
                                        act='',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0241", headers=self.headers, data=data)
        logging.info(response.text)

    def op403(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - origem:
                - destino:
                - sigla_central: DistânciaemKm:
                - distancia: Diasdetransferência:
                - prazo_transf: Quanthorasp/previsãochegada:
                - horas_transferencia: Quantidadedepedágios:
                - qtde_pedagio: Customédiodetransferência:
                - vlr_transf_com: (R$/ton)
                - sigla_emit:
                - sigla_dest:
                - cod_fil_emit:
                - cod_fil_dest:
                - cod_gen:
                - cod_route:
                - descri_route:
                - cod_fil_emit:
                - cod_fil_dest:
                - sigla_emit:
                - sigla_dest:
            :type kwargs: dict
        """
        self.last_opssw = '403'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0241", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        params = {
            "f2" : kwargs.pop('origem'),
            "f4" : kwargs.pop('destino'),
        }
        kwargs.update(params)
        html_content = self._op403_post_route(response.text,**kwargs)
        html_content = self._op403_select_route(html_content,**kwargs)
        #input()
        html_content = self._op403_select_smp(html_content, **kwargs)
        #input()
        params = {
            "f2" : kwargs.pop('cod_gen'),
            "f3" : kwargs.pop('cod_route'),
            "f4" : kwargs.pop('descri_route')
        }
        kwargs.update(params)

        self._op403_insert_info_route_smp(html_content, **kwargs)
        self._op403_insert_info_route_smp_confirm(html_content,**kwargs)
        #input()




if __name__ == '__main__':
    with Ssw_() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op_()
