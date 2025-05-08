from priority_classes.ssw.ssw import SswRequest
import pandas as pd
import logging

class Ssw023(SswRequest):
    def __init__(self):
        super().__init__()

    def _op023_get_table(self, html, range_):
        """
        Retrieves the user table from the 156 system.

        :param html: The HTML content.
        :type html: str
        :return: The user table.
        :rtype: pandas.DataFrame
        """
        tags_inicio = [f'<f{i}>' for i in range(range_)]
        tags_fim = [f'</f{i}>' for i in range(range_)]
        fila = {}
        for tag_inicio, tag_fim in zip(tags_inicio, tags_fim):
            fila[tag_inicio] = self.scrap_tags_from_xml(html, tag_inicio, tag_fim)

        # converting to Dataframe to better manipulation
        df_list = pd.DataFrame(fila)
        return df_list

    def _op023_get_table_mdfes_from_manifest(self, sequencia):
        data = f"act=MDFES_MAN&seq_manifesto={sequencia}&dummy=1690551210921"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0125", headers=self.headers, data=data)
        logging.info(response.text)
        return self._op023_get_table(response.text, 11)

    def _op023_get_info(self, html, **kwargs):
        df_manifests = self._op023_get_table(html, 16)
        sequencia = kwargs['t_cod_barras_mdfe'][-8:-1]
        logging.info(sequencia)
        data = f"act={sequencia}&dummy=1690547565641"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0125", headers=self.headers, data=data)
        logging.info(response.text)
        df_list_mdfes = self._op023_get_table_mdfes_from_manifest(sequencia)
        return response, df_list_mdfes, df_manifests

    def op023(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act:
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
        query_model = ("act=BAR_MDF&t_cod_barras_mdfe=&t_sigla_origem=MTZ&t_data_saida_ini=280623&t_data_saida_fin"
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

        return self._op023_get_info(response.text, **kwargs)


if __name__ == '__main__':
    with Ssw023() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op023()
