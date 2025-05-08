from priority_classes.ssw.ssw_v2 import SswRequest
from urllib.parse import unquote, urlencode
from bs4 import BeautifulSoup
import logging

class Ssw437(SswRequest):
    def __init__(self, name_instance="ssw_", **kwargs):
        super().__init__(name_instance=name_instance, **kwargs)
        self.html_content = None
        self.html_text = None
        self.nro_fatura = ''

    def op437(self, *args, **kwargs):
        logging.info(f"\n\n\n -------------------------------------- INICIO 437 ")
        self.last_opssw = "437"

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy={self.get_dummy()}"

        self.session.post(
            "https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data
        )

        # second query post
        data = f"sequencia={self.last_opssw}&dummy={self.get_dummy()}"

        response = self.session.post(
            "https://sistema.ssw.inf.br/bin/ssw0114", headers=self.headers, data=data
        )

        # showing results

        logging.info(response.text)
        self.html_text = response.text
        return self

    def busca_cliente(self, *args, **kwargs):
        # consulta o cnpj
        logging.info(f"\n\n\n -------------------------------------- CONSULTA CNPJ ")
        query_model = f"get_cli=0&dummy=0"
        html = unquote(self.html_text)
        data = self.update_query_values(
            html,
            query_model,
            "name",
            dummy=self.get_dummy(),
            **kwargs,
        )
        response = self.session.post(
            "https://sistema.ssw.inf.br/bin/ssw0114", headers=self.headers, data=data
        )

        logging.info(response.text)
        self.html_text = response.text
        return self

    def escolher_cliente(self, *args, **kwargs):
        # query filters to request record
        logging.info(f"\n\n\n -------------------------------------- ENTRAR NO CLIENTE")
        act = kwargs.pop("act") if "act" in kwargs else "ENV"
        query_model = (
            "act=ENV&cod_emp_ctb=01"
            "&cgc_cliente=43854116005089"
            "&cliente=CEVA%20LOGISTICS%20LTDA"
            "&data_emissao_fat=290724"
            "&nro_banco=999"
            "&f1="
            "&dummy=1722265032042"
        )
        html = unquote(self.html_text)
        data = self.update_query_values(
            html,
            query_model,
            "name",
            act=act,
            dummy=self.get_dummy(),
            **kwargs,
        )
        logging.info(data)
        response = self.session.post(
            "https://sistema.ssw.inf.br/bin/ssw0114", headers=self.headers, data=data
        )

        logging.info(response.text)
        self.html_text = response.text
        return self

    def opcao_ctrc_origem(self, *args, **kwargs):
        ####################################
        # acessa a opcao "Ctrc Origem"
        logging.info(f"\n\n\n -------------------------------------- OPCAO CTRC ORIGEM")
        query_model = (
            "act=ORIGEM&f2=210824&f4=T&f11=N&f12=N&f13=N&f14=N&f15=N&f16=S"
            "&adi_credito=14%2C50&adi_debito=85%2C31&cod_emp_ctb=1"
            "&seq_cliente=146153&data_inclusao=29%2F07%2F2024&bco_inf=999"
            "&agc_inf=0&dig_agc=0&cta_inf=0&dig_cta=0&car_inf=0&dummy=1722279754365"
        )

        # <input type=hidden name=seq_cliente id=seq_cliente value="146153">

        act = kwargs.pop("act") if "act" in kwargs else "ORIGEM"
        html = unquote(self.html_text)
        data = self.update_query_values(
            html,
            query_model,
            "name",
            act=act,
            dummy=self.get_dummy(),
            **kwargs,
        )
        logging.info(data)
        response = self.session.post(
            "https://sistema.ssw.inf.br/bin/ssw0114", headers=self.headers, data=data
        )

        logging.info(response.text)
        self.html_text = response.text
        return self

    def lanca_ctrc_origem_na_fatura(self, *args, **kwargs):
        logging.info(
            f'\n\n\n -------------------------------------- LANCANDO CTRC ORIGEM {kwargs.get("f2", " - ")}'
        )
        ####################################
        # acessa a opcao "Ctrc Origem"
        query_model = (
            "act=INC&f1=&f2=01236197&vlr=0,00&seq_cliente=146153&data_inclusao=&data_vcto="
            "&nro_fatura=0&tipo_ctrc=T&data_emi_ini=&data_emi_fin="
            "&data_emi_nf_ini=&data_emi_nf_fin=&peso_ini=0"
            "&peso_fin=0&so_entregue=N&com_baixados=N&com_comprov=N&com_comprov_scan=N&cons_a_vista=N&cons_tde=S"
            "&cod_emp_ctb=1&dacte=N&origem=S&ccusto=&nro_cte=N&bco_inf=999&agc_inf=0&dig_agc=0"
            "&cta_inf=0&dig_cta=0&car_inf=0&dummy=1722341500349"
        )

        # <input type=hidden name=seq_cliente id=seq_cliente value="146153">

        act = kwargs.pop("act") if "act" in kwargs else "INC"
        html = unquote(self.html_text)
        data = self.update_query_values(
            html,
            query_model,
            "name",
            act=act,
            nro_fatura=self.nro_fatura,
            dummy=self.get_dummy(),
            **kwargs,
        )

        logging.info(data)
        # if self.nro_fatura:
        #     query_dict = self.convert_query_url_to_dict(data)
        #     query_dict.update({"nro_fatura": self.nro_fatura})
        #     data = urlencode(query_dict)
        # logging.info(data)
        response = self.session.post(
            "https://sistema.ssw.inf.br/bin/ssw0114", headers=self.headers, data=data
        )

        if not self.nro_fatura:
            soup = BeautifulSoup(response.text, "xml")
            # Obter o valor de nro_fatura
            if nro_fatura_value := soup.find("nro_fatura").text:
                self.nro_fatura = nro_fatura_value
                logging.info(f'\n\n N FATURA OBTIDO:  {self.nro_fatura}')

        logging.info(response.text)
        # self.html_text = response.text
        return response.text
        # return self

        # for n_ctrc in self.n_ctrcs_origem:
        #     # faz o lançamento de todas as ctrc na fatura aberta.
        #     # a ideia é lançar uma seguido da outra sem sair da tela.
        #     # no fim a tela anterior terá o numero da fatura gerado, que deverei pegar pra
        #     # usar em seguida no portal Ceva.
        #     pass

        # # showing results

        # logging.info(response1.text)
        # if "instructions" in args:
        #     self._op457_instructions(response1.text, *args, **kwargs)

        # if "occurrences" in args:
        #     return self._op457_occurrences(response1.text, *args, **kwargs)
