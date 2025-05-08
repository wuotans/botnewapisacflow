import pandas as pd
from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw018(SswRequest):
    def __init__(self):
        super().__init__()

    def _op018_get_table(self, html):
        """
        Retrieves the user table from the 156 system.

        :param html: The HTML content.
        :type html: str
        :return: The user table.
        :rtype: pandas.DataFrame
        """
        tags_inicio = [f'<f{i}>' for i in range(12)]
        tags_fim = [f'</f{i}>' for i in range(12)]
        fila = {}
        for tag_inicio, tag_fim in zip(tags_inicio, tags_fim):
            fila[tag_inicio] = self.scrap_tags_from_xml(html, tag_inicio, tag_fim)

        # converting to Dataframe to better manipulation
        df_fila = pd.DataFrame(fila)
        self._create_folder('relatorios')
        df_fila.to_csv(f'relatorios/{self.credentials[4]}_ssw018_report.csv', sep=';')
        return df_fila

    def op018(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '018'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1273", headers=self.headers, data=data)
        logging.info(response.text)

        return self._op018_get_table(response.text)


if __name__ == '__main__':
    with Ssw018() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.credentials[4]='cgb'
        logging.info(ssw.op018())
