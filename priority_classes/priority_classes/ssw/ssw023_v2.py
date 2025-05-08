from priority_classes.ssw.ssw_v2 import SswRequest
import pandas as pd
import logging

class Ssw023(SswRequest):
    def __init__(self,name_instance='ssw023', **kwargs):
        super().__init__(name_instance=name_instance,**kwargs)
        self.html_content = None
        self.html_text = None
        self.name_instance = name_instance


    def _op023_get_table_mdfes_from_manifest(self, sequencia)->pd.DataFrame:
        data = f"act=MDFES_MAN&seq_manifesto={sequencia}&dummy=1690551210921"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0125", headers=self.headers, data=data)
        logging.info(response.text)
        return self.get_table(response.text,11)

    def get_info(self, **kwargs)->tuple:
        df_manifests = self._op023_get_table(self.html_text, 16)
        sequencia = kwargs['t_cod_barras_mdfe'][-8:-1]
        logging.info(sequencia)
        data = f"act={sequencia}&dummy=1690547565641"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0125", headers=self.headers, data=data)
        logging.info(response.text)
        df_list_mdfes = self._op023_get_table_mdfes_from_manifest(sequencia)
        return response, df_list_mdfes, df_manifests

    def get_ctrcs_from_manif(self,*args,**kwargs)->pd.DataFrame:
        query_model = ("act=CTRCS_MAN&seq_manifesto=2203613&dummy=1721915794679")
        data = self.update_query_values(self.html_text,
                                        query_model,
                                        'name',
                                        act='CTRCS_MAN',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0125", headers=self.headers, data=data)
        self.html_text = response.text
        logging.info(self.html_text)
        return self.get_table(self.html_text,15)

    def op023(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:'BAR_MDF'->t_cod_barras_mdfe,'IMP'->(t_ser_manifesto,t_nro_manifesto)
                - t_ser_manifesto: CódbarrasManifestoOperac:
                - t_nro_manifesto: CódbarrasManifestoOperac:
                - t_cod_barras_mdfe: ManifestosOperacdoperíodo:
                - t_sigla_origem: Placadocavalo(opc):
                - t_data_saida_ini: a
                - t_data_saida_fin:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '023'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0125", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'BAR_MDF'
        query_model = ("act=BAR_MDF&t_ser_manifesto=cgb&t_nro_manifesto=630033&t_cod_barras_mdfe=&t_sigla_origem=MTZ&t_data_saida_ini=280623&t_data_saida_fin"
                       "=280723&dummy=1690546780542")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0125", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        return self



if __name__ == '__main__':
    with Ssw023() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op023()
