from priority_classes.ssw.ssw import SswRequest
import logging

class Ssw455(SswRequest):
    def __init__(self):
        super().__init__()

    def _op455_config_excel(self, **kwargs):
        data = "config=S&dummy=1692133004846"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0230",
                                     headers=self.headers,
                                     data=data)
        logging.info(response.text)

        data = ("act=SRENV|12|1|2|11|13|34|35|36|37|40|41|42|43|98|38|39|44|45|46|47|48|49|50|51|52|3|4|5|6|7|8|9|10"
                "|100|101|22|23|24|25|53|71|72|73|75|76|77|103|59|61|62|66|67|68|69|70|74|78|79|80|81|82|83|84|85|86"
                "|87|88|89|90|91|92|93|94|95|96|97|105|107|108|109|110|111|112|113|114|115|54|55|56|57|58|63|64|65|60"
                "|26|27|28|29|30|31|32|33|99|106|14|15|16|17|18|19|20|21|102|104&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE"
                "&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE"
                "&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE"
                "&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE"
                "&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE"
                "&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE"
                "&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE"
                "&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&=TRUE&dummy"
                "=1692133056136")
        if 'list_op_to_ignore' in kwargs:
            for op in kwargs['list_op_to_ignore']:
                data = data.replace(f'|{op}|', '|').replace('&=TRUE', '', 1)
                if op == '104':
                    # como o 104 nao possui | no final ele nao é substituido, portanto, trata ele separadamente
                    data = data.replace(f'|104&', '&').replace('&=TRUE', '', 1)
                logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0230",
                                     headers=self.headers,
                                     data=data)
        logging.info(response.text)

    def op455(self, **kwargs):
        """
        Generate record sheet 455. :param kwargs: Possible keys include: - cod_emp_ctb: Empresa - f2: (E-expedidora,
        R-recebedora,A-exped+receb,F-fiscal) - f3: (E-expedidora,R-recebedora,A-exped+receb,F-fiscal) - f4: (
        R-remetente,D-destinatário,U-unidadesdestino)(opcional) - f5: (R-remetente,D-destinatário,U-unidadesdestino)(
        opcional) - f7: (R-remetente,D-destinatário,P-pagador,T-todos)(opcional) - f8: (R-remetente,D-destinatário,
        P-pagador,T-todos)(opcional) - f9: Data inicial emissão - f10: (Data final emissão (Máximo31dias) - f11: Data
        inicial autorização - f12: Data final autorização (Máximo31dias) - f18: Tipo de documento (Todos) - f19: (
        C-CIF,F-FOB,T-todos) - f20: (S-sim,N-não) - f21: (P-pendentedefaturamento,L-liquidado,F-faturadonãoliquidado,
        C-cancelado,B-bloq.financeiro, - f22: (E-Entregues,B-baixados,P-pendentes,T-todos) - f23: (S-sim,N-não,
        A-ambos) - f25: Tipo tabela calculo (Todos) - f26: (S-sim,N-não,A-ambos) - f27: (S-sim,N-não,A-ambos) - f28:
        (S-substituição,I-isento,N-nãotributado,C-comICMS,F-comISS,T-todos) - f29: (S-sim,N-não,A-ambos) - f30: (
        S-sim,N-não,A-ambos) - f32: Vendedor (opcional) - f34: Placa coleta (opcional) - f35: (R-relatório,E-Excel,
        C-Batchgeocoleta,B-Batchgeoentrega) - list_op_to_ignore: list of columns option to ignore in the report if
        f35 == E - f37: (A-Manifesto/Romaneio, B-Ocorrências, C-Comprov Entregas, D-Parceria, E-Fatura,
        F-Notas Fiscais, G-ResultadoH-Vendedor, I-Averbação, J-Contabilidade, K-Outros, N-Sem dados complementares) -
        f38: (A-Manifesto/Romaneio, B-Ocorrências, C-Comprov Entregas, D-Parceria, E-Fatura, F-Notas Fiscais,
        G-ResultadoH-Vendedor, I-Averbação, J-Contabilidade, K-Outros, N-Sem dados complementares) - f39: (
        A-Manifesto/Romaneio, B-Ocorrências, C-Comprov Entregas, D-Parceria, E-Fatura, F-Notas Fiscais,
        G-ResultadoH-Vendedor, I-Averbação, J-Contabilidade, K-Outros, N-Sem dados complementares) :type kwargs: dict
        :return: None
        """
        self.last_opssw = '455'
        # The request to this option takes two post to reach to the page

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3=455&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01",
                          headers=self.headers,
                          data=data)

        # second query post
        data = "sequencia=455&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0230",
                                     headers=self.headers,
                                     data=data)

        # config excel
        if 'f35' in kwargs:
            self._op455_config_excel(**kwargs)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'E1'
        query_model = ("act=E1&cod_emp_ctb=00&f2=a&f3=b&f4=c&f5=d&f7=10&f8=g&f9=010623&f10=020623&f11=030623&f12"
                       "=040623&f18=5&f19=6&f20=7&f21=8&f22=9&f23=1&f25=2&f26=3&f27=4&f28=5&f29=6&f30=7&f32=8&f34=9"
                       "&f35=1&f37=2&f38=3&f39=4&basico=N&dummy=1686919951718")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act=act,
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0230",
                                     headers=self.headers,
                                     data=data)
        logging.info(response.text)
        self.handle_download(response.text)


if __name__ == '__main__':
    ssw = Ssw455()
    ssw.init_browser()
    ssw.login()
    ssw.op455()
