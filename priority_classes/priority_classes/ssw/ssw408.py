from bs4 import BeautifulSoup
from urllib.parse import unquote
from priority_classes.ssw.ssw import SswRequest
import html
from datetime import datetime
import logging

class Ssw408(SswRequest):
    def __init__(self):
        super().__init__()

    def _op408_get_filial(self, unidade):
        response = self.session.get(f"https://sistema.ssw.inf.br/bin/ssw0507?get_filial={unidade}&dummy=1691768360612",
                                    headers=self.headers)
        html_text = html.unescape(response.text)
        logging.info(html_text)
        tag_ini = '<filial>'
        tag_fim = '</filial>'
        index_ini = html_text.find(tag_ini)
        index_fim = html_text.find(tag_fim)
        if -1 not in (index_ini, index_fim):
            result = html_text[index_ini + len(tag_ini):index_fim]
            filial = result.split('_0>')[1].replace('</', '')
            cidade = result.split('_1>')[1].replace('</', '')
            uf = result.split('_2>')[1].replace('</', '')
            filial_t = f"{filial} - {cidade}/{uf}"
            return filial_t
        else:
            return None

    def _op408_get_cgc(self, html):
        """
        Builds the URL to download a file from the 156 system.

        :param html: The HTML content containing the required values.
        :type html: str
        :return: The URL to download the file.
        :rtype: str
        """
        # Parse the HTML input
        soup = BeautifulSoup(html, "html.parser")
        web_body_value = soup.find("input", id="web_body")["value"]

        # Extract the required values from the web_body value
        decoded_text = unquote(web_body_value)
        logging.info(decoded_text)
        return decoded_text

    def _op408_link_cli(self, data, **kwargs):
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0508", headers=self.headers, data=data)
        logging.info(response.text)
        # query filters to request record
        query_model = ("act=ENV&f2=CGB&f3=a&f5=1024607000174&f6=p&f8=1&sigla_emit=2&sigla_dest=3&f9=a&comi_unid=S"
                       "&dummy=1691773684222")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act='ENV',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0508", headers=self.headers, data=data)
        logging.info(response.text)

        _ = kwargs.pop('unidade') if 'unidade' in kwargs else None
        _ = kwargs.pop('f3') if 'f3' in kwargs else None
        _ = kwargs.pop('f5') if 'f5' in kwargs else None
        _ = kwargs.pop('f6') if 'f6' in kwargs else None
        _ = kwargs.pop('f8') if 'f8' in kwargs else None
        _ = kwargs.pop('f9') if 'f9' in kwargs else None

        # query filters to request record
        query_model = ("act=ENV2&subcontratado=51450375000194%20-%20R%20M%20TRANSPORTES%20E%20LOGISTICA&cod_nro_tabela"
                       "=CC40041&cliente=01024607000174%20-%20SUPER%20LIGAS%20IND.%20E%20COM.%20DE%20MET"
                       "&desc_fg_cliente=Pagador&filial=BOA%20-%20BOA-UNIDADE%20AGUA%20BOA&desc_fg_filial=Expedidora"
                       "&mercadoria=Todos%20os%20codigos&desc_tp_frete=CIF/FOB&exp_cli_emit_pol=5%2C00"
                       "&exp_cli_emit_reg=5%2C00&exp_cli_emit_int=5%2C00&exp_cli_emit_perc_seguro=0%2C00"
                       "&exp_cli_emit_fg_cofins=S&exp_cli_emit_fg_desc_tda=N&exp_cli_emit_fg_desc_despacho=N"
                       "&exp_cli_emit_fg_icms=S&exp_cli_emit_fg_desc_tde=S&exp_cli_emit_fg_desc_pedagio=S"
                       "&exp_cli_emit_fg_desc_outros=S&exp_cli_emit_fg_desc_trt=N&exp_cli_emit_fg_desc_recepcao=N"
                       "&exp_cli_emit_fg_desc_tar=N&exp_cli_emit_fg_desc_tdc=N&exp_cli_emit_vlr_min_merc=0%2C00"
                       "&exp_cli_emit_ad_valor_pol=0%2C000&exp_cli_emit_ad_valor_reg=0%2C000"
                       "&exp_cli_emit_ad_valor_int=0%2C000&exp_cli_emit_despacho_pol=0%2C00&exp_cli_emit_despacho_reg"
                       "=0%2C00&exp_cli_emit_despacho_int=0%2C00&exp_cli_emit_cubagem=0%2C00&exp_cli_emit_fx0_limite"
                       "=0%2C000&exp_cli_emit_fx0_peso_pol=0%2C00&exp_cli_emit_fx0_peso_reg=0%2C00"
                       "&exp_cli_emit_fx0_peso_int=0%2C00&exp_cli_emit_fx1_limite=0%2C000&exp_cli_emit_fx1_peso_pol=0"
                       "%2C00&exp_cli_emit_fx1_peso_reg=0%2C00&exp_cli_emit_fx1_peso_int=0%2C00"
                       "&exp_cli_emit_fx2_limite=0%2C000&exp_cli_emit_fx2_peso_pol=0%2C00&exp_cli_emit_fx2_peso_reg=0"
                       "%2C00&exp_cli_emit_fx2_peso_int=0%2C00&exp_cli_emit_fx3_limite=0%2C000"
                       "&exp_cli_emit_fx3_peso_pol=0%2C00&exp_cli_emit_fx3_peso_reg=0%2C00&exp_cli_emit_fx3_peso_int"
                       "=0%2C00&exp_cli_emit_fx4_limite=0%2C000&exp_cli_emit_fx4_peso_pol=0%2C00"
                       "&exp_cli_emit_fx4_peso_reg=0%2C00&exp_cli_emit_fx4_peso_int=0%2C00&exp_cli_emit_fx5_limite=0"
                       "%2C000&exp_cli_emit_fx5_peso_pol=0%2C00&exp_cli_emit_fx5_peso_reg=0%2C00"
                       "&exp_cli_emit_fx5_peso_int=0%2C00&exp_cli_emit_fx6_limite=0%2C000&exp_cli_emit_fx6_peso_pol=0"
                       "%2C00&exp_cli_emit_fx6_peso_reg=0%2C00&exp_cli_emit_fx6_peso_int=0%2C00"
                       "&exp_cli_emit_fx7_limite=0%2C000&exp_cli_emit_fx7_peso_pol=0%2C00&exp_cli_emit_fx7_peso_reg=0"
                       "%2C00&exp_cli_emit_fx7_peso_int=0%2C00&exp_cli_emit_fx8_limite=0%2C000"
                       "&exp_cli_emit_fx8_peso_pol=0%2C00&exp_cli_emit_fx8_peso_reg=0%2C00&exp_cli_emit_fx8_peso_int"
                       "=0%2C00&exp_cli_emit_fx9_limite=0%2C000&exp_cli_emit_fx9_peso_pol=0%2C00"
                       "&exp_cli_emit_fx9_peso_reg=0%2C00&exp_cli_emit_fx9_peso_int=0%2C00&exp_cli_emit_fx10_limite=0"
                       "%2C000&exp_cli_emit_fx10_peso_pol=0%2C00&exp_cli_emit_fx10_peso_reg=0%2C00"
                       "&exp_cli_emit_fx10_peso_int=0%2C00&exp_cli_emit_fx11_limite=0%2C000"
                       "&exp_cli_emit_fx11_peso_pol=0%2C00&exp_cli_emit_fx11_peso_reg=0%2C00"
                       "&exp_cli_emit_fx11_peso_int=0%2C00&exp_cli_emit_fx12_limite=0%2C000"
                       "&exp_cli_emit_fx12_peso_pol=0%2C00&exp_cli_emit_fx12_peso_reg=0%2C00"
                       "&exp_cli_emit_fx12_peso_int=0%2C00&exp_cli_emit_fx13_limite=0%2C000"
                       "&exp_cli_emit_fx13_peso_pol=0%2C00&exp_cli_emit_fx13_peso_reg=0%2C00"
                       "&exp_cli_emit_fx13_peso_int=0%2C00&exp_cli_emit_ult_fx_peso_pol=0%2C00"
                       "&exp_cli_emit_ult_fx_peso_reg=0%2C00&exp_cli_emit_ult_fx_peso_int=0%2C00"
                       "&exp_cli_emit_apos_ult_fx=E&exp_cli_emit_pol_min_ton=0%2C00&exp_cli_emit_reg_min_ton=0%2C00"
                       "&exp_cli_emit_int_min_ton=0%2C00&exp_cli_emit_pol_min=0%2C00&exp_cli_emit_reg_min=0%2C00"
                       "&exp_cli_emit_int_min=0%2C00&exp_cli_emit_pol_min_perc_frt=0%2C00"
                       "&exp_cli_emit_reg_min_perc_frt=0%2C00&exp_cli_emit_int_min_perc_frt=0%2C00"
                       "&exp_cli_emit_tar_perc=0%2C00&exp_cli_emit_tar_sobre_frete=0%2C00&exp_cli_emit_min_tar=0%2C00"
                       "&exp_cli_emit_tdc_perc=0%2C00&exp_cli_emit_tdc_sobre_frete=0%2C00&exp_cli_emit_min_tdc=0%2C00"
                       "&exp_cli_emit_vlr_pedagio=0%2C00&exp_cli_emit_fec=10%2C00&rec_cli_dest_pol=0%2C00"
                       "&rec_cli_dest_reg=0%2C00&rec_cli_dest_int=0%2C00&rec_cli_dest_perc_seguro=0%2C00"
                       "&rec_cli_dest_fg_cofins=N&rec_cli_dest_fg_desc_tda=N&rec_cli_dest_fg_desc_despacho=N"
                       "&rec_cli_dest_fg_icms=N&rec_cli_dest_fg_desc_tde=N&rec_cli_dest_fg_desc_pedagio=N"
                       "&rec_cli_dest_fg_desc_outros=N&rec_cli_dest_fg_desc_trt=N&rec_cli_dest_fg_desc_col=N"
                       "&rec_cli_dest_fg_desc_tar=N&rec_cli_dest_fg_desc_tdc=N&rec_cli_dest_vlr_min_merc=0%2C00"
                       "&rec_cli_dest_ad_valor_pol=0%2C000&rec_cli_dest_ad_valor_reg=0%2C000"
                       "&rec_cli_dest_ad_valor_int=0%2C000&rec_cli_dest_despacho_pol=0%2C00&rec_cli_dest_despacho_reg"
                       "=0%2C00&rec_cli_dest_despacho_int=0%2C00&rec_cli_dest_cubagem=0%2C00&rec_cli_dest_fx0_limite"
                       "=0%2C000&rec_cli_dest_fx0_peso_pol=0%2C00&rec_cli_dest_fx0_peso_reg=0%2C00"
                       "&rec_cli_dest_fx0_peso_int=0%2C00&rec_cli_dest_fx1_limite=0%2C000&rec_cli_dest_fx1_peso_pol=0"
                       "%2C00&rec_cli_dest_fx1_peso_reg=0%2C00&rec_cli_dest_fx1_peso_int=0%2C00"
                       "&rec_cli_dest_fx2_limite=0%2C000&rec_cli_dest_fx2_peso_pol=0%2C00&rec_cli_dest_fx2_peso_reg=0"
                       "%2C00&rec_cli_dest_fx2_peso_int=0%2C00&rec_cli_dest_fx3_limite=0%2C000"
                       "&rec_cli_dest_fx3_peso_pol=0%2C00&rec_cli_dest_fx3_peso_reg=0%2C00&rec_cli_dest_fx3_peso_int"
                       "=0%2C00&rec_cli_dest_fx4_limite=0%2C000&rec_cli_dest_fx4_peso_pol=0%2C00"
                       "&rec_cli_dest_fx4_peso_reg=0%2C00&rec_cli_dest_fx4_peso_int=0%2C00&rec_cli_dest_fx5_limite=0"
                       "%2C000&rec_cli_dest_fx5_peso_pol=0%2C00&rec_cli_dest_fx5_peso_reg=0%2C00"
                       "&rec_cli_dest_fx5_peso_int=0%2C00&rec_cli_dest_fx6_limite=0%2C000&rec_cli_dest_fx6_peso_pol=0"
                       "%2C00&rec_cli_dest_fx6_peso_reg=0%2C00&rec_cli_dest_fx6_peso_int=0%2C00"
                       "&rec_cli_dest_fx7_limite=0%2C000&rec_cli_dest_fx7_peso_pol=0%2C00&rec_cli_dest_fx7_peso_reg=0"
                       "%2C00&rec_cli_dest_fx7_peso_int=0%2C00&rec_cli_dest_fx8_limite=0%2C000"
                       "&rec_cli_dest_fx8_peso_pol=0%2C00&rec_cli_dest_fx8_peso_reg=0%2C00&rec_cli_dest_fx8_peso_int"
                       "=0%2C00&rec_cli_dest_fx9_limite=0%2C000&rec_cli_dest_fx9_peso_pol=0%2C00"
                       "&rec_cli_dest_fx9_peso_reg=0%2C00&rec_cli_dest_fx9_peso_int=0%2C00&rec_cli_dest_fx10_limite=0"
                       "%2C000&rec_cli_dest_fx10_peso_pol=0%2C00&rec_cli_dest_fx10_peso_reg=0%2C00"
                       "&rec_cli_dest_fx10_peso_int=0%2C00&rec_cli_dest_fx11_limite=0%2C000"
                       "&rec_cli_dest_fx11_peso_pol=0%2C00&rec_cli_dest_fx11_peso_reg=0%2C00"
                       "&rec_cli_dest_fx11_peso_int=0%2C00&rec_cli_dest_fx12_limite=0%2C000"
                       "&rec_cli_dest_fx12_peso_pol=0%2C00&rec_cli_dest_fx12_peso_reg=0%2C00"
                       "&rec_cli_dest_fx12_peso_int=0%2C00&rec_cli_dest_fx13_limite=0%2C000"
                       "&rec_cli_dest_fx13_peso_pol=0%2C00&rec_cli_dest_fx13_peso_reg=0%2C00"
                       "&rec_cli_dest_fx13_peso_int=0%2C00&rec_cli_dest_ult_fx_peso_pol=0%2C00"
                       "&rec_cli_dest_ult_fx_peso_reg=0%2C00&rec_cli_dest_ult_fx_peso_int=0%2C00"
                       "&rec_cli_dest_apos_ult_fx=E&rec_cli_dest_pol_min_ton=0%2C00&rec_cli_dest_reg_min_ton=0%2C00"
                       "&rec_cli_dest_int_min_ton=0%2C00&rec_cli_dest_pol_min=0%2C00&rec_cli_dest_reg_min=0%2C00"
                       "&rec_cli_dest_int_min=0%2C00&rec_cli_dest_pol_min_perc_frt=0%2C00"
                       "&rec_cli_dest_reg_min_perc_frt=0%2C00&rec_cli_dest_int_min_perc_frt=0%2C00"
                       "&rec_cli_dest_tdc_perc=0%2C00&rec_cli_dest_tdc_sobre_frete=0%2C00&rec_cli_dest_min_tdc=0%2C00"
                       "&rec_cli_dest_tde_perc=0%2C00&rec_cli_dest_tde_sobre_frete=0%2C00&rec_cli_dest_min_tde=0%2C00"
                       "&rec_cli_dest_trt_perc=0%2C00&rec_cli_dest_trt_sobre_frete=0%2C00&rec_cli_dest_min_trt=0%2C00"
                       "&rec_cli_dest_tda_perc=0%2C00&rec_cli_dest_tda_sobre_frete=0%2C00&rec_cli_dest_min_tda=0%2C00"
                       "&rec_cli_dest_tar_perc=0%2C00&rec_cli_dest_tar_sobre_frete=0%2C00&rec_cli_dest_min_tar=0%2C00"
                       "&rec_cli_dest_vlr_pedagio=0%2C00&rec_cli_dest_comi_fec=0%2C00&acao=A&cgc=51450375000194"
                       "&seq_cliente=30566&cod_fil=74&seq_mercadoria=0&fg_cliente=P&fg_filial=E&tp_frete=A"
                       "&data_ini_ativ=11%2F08%2F23&cod_fil_emit=0&cod_fil_dest=0&dummy=1691787245867")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act='ENV2',
                                        dummy=self.get_dummy(),
                                        #data_ini_ativ=datetime.now().strftime("%d/%m/%y"),
                                        **kwargs)

        data = data.replace('+', ' ')
        logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0508", headers=self.headers, data=data)
        logging.info(response.text)
        if 'Erro lendo tabela.' in response.text:
            return False
        else:
            return True

    def _op408_link_merc(self, data, **kwargs):
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1940", headers=self.headers, data=data)
        logging.info(response.text)

        query_model = ("act=ENV&f2=ABV&f3=e&f5=439&comi_unid=S&dummy=1723152804674")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act='ENV',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1940", headers=self.headers, data=data)
        logging.info(response.text)

        query_model = ("act=ENV2&subcontratado=36086069000127%20-%20DANTES%20UMBERTO%20LASSE&filial=ABV%20-%20ABV%20"
                       "-%20UND.%20ALTO%20BOA%20VISTA%20-%20MT&desc_fg_filial=Expedidora&mercadoria=439%20-%20MK%20"
                       "-%20DAFITI&exp_emit_pol=20%2C00&exp_emit_reg=35%2C00&exp_emit_int=35%2C00&exp_emit_fg_cofins"
                       "=s&exp_emit_fg_desc_tda=s&exp_emit_fg_desc_despacho=s&exp_emit_fg_icms=s&exp_emit_fg_desc_tde"
                       "=s&exp_emit_fg_desc_pedagio=s&exp_emit_fg_desc_outros=N&exp_emit_fg_desc_trt=s"
                       "&exp_emit_fg_desc_recepcao=N&exp_emit_fg_desc_tar=N&exp_emit_fg_desc_tdc=s"
                       "&exp_emit_vlr_min_merc=0%2C00&exp_emit_apos_ult_fx=E&exp_emit_pol_min=6%2C00&exp_emit_reg_min"
                       "=6%2C00&exp_emit_int_min=6%2C00&rec_dest_fg_cofins=N&rec_dest_fg_desc_tda=N"
                       "&rec_dest_fg_desc_despacho=N&rec_dest_fg_icms=N&rec_dest_fg_desc_tde=N"
                       "&rec_dest_fg_desc_pedagio=N&rec_dest_fg_desc_outros=N&rec_dest_fg_desc_trt=N"
                       "&rec_dest_fg_desc_col=N&rec_dest_fg_desc_tar=N&rec_dest_fg_desc_tdc=N&rec_dest_apos_ult_fx=E"
                       "&acao=I&cgc=36086069000127&cod_fil=120&seq_mercadoria=1116&fg_filial=E&data_ini_ativ=08%2F08"
                       "%2F24&dummy=1723154324224")
        query_model = ("act=ENV2&subcontratado=36086069000127%20-%20DANTES%20UMBERTO%20LASSE&filial=ABV%20-%20ABV%20"
                       "-%20UND.%20ALTO%20BOA%20VISTA%20-%20MT&desc_fg_filial=Expedidora&mercadoria=439%20-%20MK%20"
                       "-%20DAFITI&exp_emit_pol=25%2C00&exp_emit_reg=25"
                       "%2C00&exp_emit_int=25%2C00&exp_emit_perc_seguro=0%2C00&exp_emit_fg_cofins=N"
                       "&exp_emit_fg_desc_tda=N&exp_emit_fg_desc_despacho=N&exp_emit_fg_icms=S&exp_emit_fg_desc_tde=S"
                       "&exp_emit_fg_desc_pedagio=S&exp_emit_fg_desc_outros=N&exp_emit_fg_desc_trt=N"
                       "&exp_emit_fg_desc_recepcao=N&exp_emit_fg_desc_tar=N&exp_emit_fg_desc_tdc=N"
                       "&exp_emit_vlr_min_merc=0%2C00&exp_emit_ad_valor_pol=0%2C050&exp_emit_ad_valor_reg=0%2C500"
                       "&exp_emit_ad_valor_int=0%2C500&exp_emit_despacho_pol=3%2C00&exp_emit_despacho_reg=3%2C00"
                       "&exp_emit_despacho_int=3%2C00&exp_emit_cubagem=0%2C00&exp_emit_fx0_limite=0%2C000"
                       "&exp_emit_fx0_peso_pol=0%2C00&exp_emit_fx0_peso_reg=0%2C00&exp_emit_fx0_peso_int=0%2C00"
                       "&exp_emit_fx1_limite=0%2C000&exp_emit_fx1_peso_pol=0%2C00&exp_emit_fx1_peso_reg=0%2C00"
                       "&exp_emit_fx1_peso_int=0%2C00&exp_emit_fx2_limite=0%2C000&exp_emit_fx2_peso_pol=0%2C00"
                       "&exp_emit_fx2_peso_reg=0%2C00&exp_emit_fx2_peso_int=0%2C00&exp_emit_fx3_limite=0%2C000"
                       "&exp_emit_fx3_peso_pol=0%2C00&exp_emit_fx3_peso_reg=0%2C00&exp_emit_fx3_peso_int=0%2C00"
                       "&exp_emit_fx4_limite=0%2C000&exp_emit_fx4_peso_pol=0%2C00&exp_emit_fx4_peso_reg=0%2C00"
                       "&exp_emit_fx4_peso_int=0%2C00&exp_emit_fx5_limite=0%2C000&exp_emit_fx5_peso_pol=0%2C00"
                       "&exp_emit_fx5_peso_reg=0%2C00&exp_emit_fx5_peso_int=0%2C00&exp_emit_fx6_limite=0%2C000"
                       "&exp_emit_fx6_peso_pol=0%2C00&exp_emit_fx6_peso_reg=0%2C00&exp_emit_fx6_peso_int=0%2C00"
                       "&exp_emit_fx7_limite=0%2C000&exp_emit_fx7_peso_pol=0%2C00&exp_emit_fx7_peso_reg=0%2C00"
                       "&exp_emit_fx7_peso_int=0%2C00&exp_emit_fx8_limite=0%2C000&exp_emit_fx8_peso_pol=0%2C00"
                       "&exp_emit_fx8_peso_reg=0%2C00&exp_emit_fx8_peso_int=0%2C00&exp_emit_fx9_limite=0%2C000"
                       "&exp_emit_fx9_peso_pol=0%2C00&exp_emit_fx9_peso_reg=0%2C00&exp_emit_fx9_peso_int=0%2C00"
                       "&exp_emit_fx10_limite=0%2C000&exp_emit_fx10_peso_pol=0%2C00&exp_emit_fx10_peso_reg=0%2C00"
                       "&exp_emit_fx10_peso_int=0%2C00&exp_emit_fx11_limite=0%2C000&exp_emit_fx11_peso_pol=0%2C00"
                       "&exp_emit_fx11_peso_reg=0%2C00&exp_emit_fx11_peso_int=0%2C00&exp_emit_fx12_limite=0%2C000"
                       "&exp_emit_fx12_peso_pol=0%2C00&exp_emit_fx12_peso_reg=0%2C00&exp_emit_fx12_peso_int=0%2C00"
                       "&exp_emit_fx13_limite=0%2C000&exp_emit_fx13_peso_pol=0%2C00&exp_emit_fx13_peso_reg=0%2C00"
                       "&exp_emit_fx13_peso_int=0%2C00&exp_emit_ult_fx_peso_pol=0%2C00&exp_emit_ult_fx_peso_reg=0%2C00"
                       "&exp_emit_ult_fx_peso_int=0%2C00&exp_emit_apos_ult_fx=E&exp_emit_pol_min_ton=280%2C00"
                       "&exp_emit_reg_min_ton=280%2C00&exp_emit_int_min_ton=280%2C00&exp_emit_pol_min=28%2C00"
                       "&exp_emit_reg_min=28%2C00&exp_emit_int_min=28%2C00&exp_emit_pol_min_perc_frt=0%2C00"
                       "&exp_emit_reg_min_perc_frt=0%2C00&exp_emit_int_min_perc_frt=0%2C00&exp_emit_tdc_perc=0%2C00"
                       "&exp_emit_tdc_sobre_frete=0%2C00&exp_emit_min_tdc=0%2C00&exp_emit_trt_perc=0%2C00"
                       "&exp_emit_trt_sobre_frete=0%2C00&exp_emit_min_trt=0%2C00&exp_emit_tda_perc=0%2C00"
                       "&exp_emit_tda_sobre_frete=0%2C00&exp_emit_min_tda=0%2C00&exp_emit_tar_perc=0%2C00"
                       "&exp_emit_tar_sobre_frete=0%2C00&exp_emit_min_tar=0%2C00&exp_emit_vlr_pedagio=1%2C20"
                       "&exp_emit_fec=0%2C00&rec_dest_pol=0%2C00&rec_dest_reg=0%2C00&rec_dest_int=0%2C00"
                       "&rec_dest_perc_seguro=0%2C00&rec_dest_fg_cofins=N&rec_dest_fg_desc_tda=N"
                       "&rec_dest_fg_desc_despacho=N&rec_dest_fg_icms=N&rec_dest_fg_desc_tde=N&rec_dest_fg_desc_pedagio"
                       "=N&rec_dest_fg_desc_outros=N&rec_dest_fg_desc_trt=N&rec_dest_fg_desc_col=N&rec_dest_fg_desc_tar"
                       "=N&rec_dest_fg_desc_tdc=N&rec_dest_vlr_min_merc=0%2C00&rec_dest_ad_valor_pol=0%2C000"
                       "&rec_dest_ad_valor_reg=0%2C000&rec_dest_ad_valor_int=0%2C000&rec_dest_despacho_pol=0%2C00"
                       "&rec_dest_despacho_reg=0%2C00&rec_dest_despacho_int=0%2C00&rec_dest_cubagem=0%2C00"
                       "&rec_dest_fx0_limite=0%2C000&rec_dest_fx0_peso_pol=0%2C00&rec_dest_fx0_peso_reg=0%2C00"
                       "&rec_dest_fx0_peso_int=0%2C00&rec_dest_fx1_limite=0%2C000&rec_dest_fx1_peso_pol=0%2C00"
                       "&rec_dest_fx1_peso_reg=0%2C00&rec_dest_fx1_peso_int=0%2C00&rec_dest_fx2_limite=0%2C000"
                       "&rec_dest_fx2_peso_pol=0%2C00&rec_dest_fx2_peso_reg=0%2C00&rec_dest_fx2_peso_int=0%2C00"
                       "&rec_dest_fx3_limite=0%2C000&rec_dest_fx3_peso_pol=0%2C00&rec_dest_fx3_peso_reg=0%2C00"
                       "&rec_dest_fx3_peso_int=0%2C00&rec_dest_fx4_limite=0%2C000&rec_dest_fx4_peso_pol=0%2C00"
                       "&rec_dest_fx4_peso_reg=0%2C00&rec_dest_fx4_peso_int=0%2C00&rec_dest_fx5_limite=0%2C000"
                       "&rec_dest_fx5_peso_pol=0%2C00&rec_dest_fx5_peso_reg=0%2C00&rec_dest_fx5_peso_int=0%2C00"
                       "&rec_dest_fx6_limite=0%2C000&rec_dest_fx6_peso_pol=0%2C00&rec_dest_fx6_peso_reg=0%2C00"
                       "&rec_dest_fx6_peso_int=0%2C00&rec_dest_fx7_limite=0%2C000&rec_dest_fx7_peso_pol=0%2C00"
                       "&rec_dest_fx7_peso_reg=0%2C00&rec_dest_fx7_peso_int=0%2C00&rec_dest_fx8_limite=0%2C000"
                       "&rec_dest_fx8_peso_pol=0%2C00&rec_dest_fx8_peso_reg=0%2C00&rec_dest_fx8_peso_int=0%2C00"
                       "&rec_dest_fx9_limite=0%2C000&rec_dest_fx9_peso_pol=0%2C00&rec_dest_fx9_peso_reg=0%2C00"
                       "&rec_dest_fx9_peso_int=0%2C00&rec_dest_fx10_limite=0%2C000&rec_dest_fx10_peso_pol=0%2C00"
                       "&rec_dest_fx10_peso_reg=0%2C00&rec_dest_fx10_peso_int=0%2C00&rec_dest_fx11_limite=0%2C000"
                       "&rec_dest_fx11_peso_pol=0%2C00&rec_dest_fx11_peso_reg=0%2C00&rec_dest_fx11_peso_int=0%2C00"
                       "&rec_dest_fx12_limite=0%2C000&rec_dest_fx12_peso_pol=0%2C00&rec_dest_fx12_peso_reg=0%2C00"
                       "&rec_dest_fx12_peso_int=0%2C00&rec_dest_fx13_limite=0%2C000&rec_dest_fx13_peso_pol=0%2C00"
                       "&rec_dest_fx13_peso_reg=0%2C00&rec_dest_fx13_peso_int=0%2C00&rec_dest_ult_fx_peso_pol=0%2C00"
                       "&rec_dest_ult_fx_peso_reg=0%2C00&rec_dest_ult_fx_peso_int=0%2C00&rec_dest_apos_ult_fx=E"
                       "&rec_dest_pol_min_ton=0%2C00&rec_dest_reg_min_ton=0%2C00&rec_dest_int_min_ton=0%2C00"
                       "&rec_dest_pol_min=0%2C00&rec_dest_reg_min=0%2C00&rec_dest_int_min=0%2C00"
                       "&rec_dest_pol_min_perc_frt=0%2C00&rec_dest_reg_min_perc_frt=0%2C00&rec_dest_int_min_perc_frt=0"
                       "%2C00&rec_dest_tdc_perc=0%2C00&rec_dest_tdc_sobre_frete=0%2C00&rec_dest_min_tdc=0%2C00"
                       "&rec_dest_tde_perc=0%2C00&rec_dest_tde_sobre_frete=0%2C00&rec_dest_min_tde=0%2C00"
                       "&rec_dest_trt_perc=0%2C00&rec_dest_trt_sobre_frete=0%2C00&rec_dest_min_trt=0%2C00"
                       "&rec_dest_tda_perc=0%2C00&rec_dest_tda_sobre_frete=0%2C00&rec_dest_min_tda=0%2C00"
                       "&rec_dest_tar_perc=0%2C00&rec_dest_tar_sobre_frete=0%2C00&rec_dest_min_tar=0%2C00"
                       "&rec_dest_vlr_pedagio=0%2C00&rec_dest_comi_fec=0%2C00&acao=A&cgc=38475768000194&seq_cidade=901"
                       "&cod_fil=72&seq_mercadoria=0&fg_filial=E&data_ini_ativ=10%2F06%2F24&dummy=1718136404789")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act='ENV2',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        data = data.replace('+', ' ')
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1940", headers=self.headers, data=data)
        logging.info(response.text)
        if 'Erro lendo tabela.' in response.text:
            return False
        else:
            return True

    def _op408_link_city(self, data, **kwargs):
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1269", headers=self.headers, data=data)
        logging.info(response.text)
        query_model = ("act=ENV&f2=GYN&f3=E&f4=ANAPOLIS/GO&comi_unid=S&dummy=1718126884488")
        data = self.update_query_values(response.text,
                                        query_model,
                                        'name',
                                        act='ENV',
                                        dummy=self.get_dummy(),
                                        **kwargs)
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1269", headers=self.headers, data=data)
        logging.info(response.text)
        query_model = ("act=ENV2&subcontratado=38475768000194%20-%20EXPRESSO%20GOIAS%20E%20LOGISTICA%20LTDA%20%28SIM"
                       "%20GOIAS%29&cod_nro_tabela=CI574&cidade=ANAPOLIS%20GO&filial=GYN%20-%20GYN-REDESPACHO"
                       "&desc_fg_filial=Expedidora&mercadoria=Todos%20os%20codigos&exp_emit_pol=25%2C00&exp_emit_reg=25"
                       "%2C00&exp_emit_int=25%2C00&exp_emit_perc_seguro=0%2C00&exp_emit_fg_cofins=N"
                       "&exp_emit_fg_desc_tda=N&exp_emit_fg_desc_despacho=N&exp_emit_fg_icms=S&exp_emit_fg_desc_tde=S"
                       "&exp_emit_fg_desc_pedagio=S&exp_emit_fg_desc_outros=N&exp_emit_fg_desc_trt=N"
                       "&exp_emit_fg_desc_recepcao=N&exp_emit_fg_desc_tar=N&exp_emit_fg_desc_tdc=N"
                       "&exp_emit_vlr_min_merc=0%2C00&exp_emit_ad_valor_pol=0%2C050&exp_emit_ad_valor_reg=0%2C500"
                       "&exp_emit_ad_valor_int=0%2C500&exp_emit_despacho_pol=3%2C00&exp_emit_despacho_reg=3%2C00"
                       "&exp_emit_despacho_int=3%2C00&exp_emit_cubagem=0%2C00&exp_emit_fx0_limite=0%2C000"
                       "&exp_emit_fx0_peso_pol=0%2C00&exp_emit_fx0_peso_reg=0%2C00&exp_emit_fx0_peso_int=0%2C00"
                       "&exp_emit_fx1_limite=0%2C000&exp_emit_fx1_peso_pol=0%2C00&exp_emit_fx1_peso_reg=0%2C00"
                       "&exp_emit_fx1_peso_int=0%2C00&exp_emit_fx2_limite=0%2C000&exp_emit_fx2_peso_pol=0%2C00"
                       "&exp_emit_fx2_peso_reg=0%2C00&exp_emit_fx2_peso_int=0%2C00&exp_emit_fx3_limite=0%2C000"
                       "&exp_emit_fx3_peso_pol=0%2C00&exp_emit_fx3_peso_reg=0%2C00&exp_emit_fx3_peso_int=0%2C00"
                       "&exp_emit_fx4_limite=0%2C000&exp_emit_fx4_peso_pol=0%2C00&exp_emit_fx4_peso_reg=0%2C00"
                       "&exp_emit_fx4_peso_int=0%2C00&exp_emit_fx5_limite=0%2C000&exp_emit_fx5_peso_pol=0%2C00"
                       "&exp_emit_fx5_peso_reg=0%2C00&exp_emit_fx5_peso_int=0%2C00&exp_emit_fx6_limite=0%2C000"
                       "&exp_emit_fx6_peso_pol=0%2C00&exp_emit_fx6_peso_reg=0%2C00&exp_emit_fx6_peso_int=0%2C00"
                       "&exp_emit_fx7_limite=0%2C000&exp_emit_fx7_peso_pol=0%2C00&exp_emit_fx7_peso_reg=0%2C00"
                       "&exp_emit_fx7_peso_int=0%2C00&exp_emit_fx8_limite=0%2C000&exp_emit_fx8_peso_pol=0%2C00"
                       "&exp_emit_fx8_peso_reg=0%2C00&exp_emit_fx8_peso_int=0%2C00&exp_emit_fx9_limite=0%2C000"
                       "&exp_emit_fx9_peso_pol=0%2C00&exp_emit_fx9_peso_reg=0%2C00&exp_emit_fx9_peso_int=0%2C00"
                       "&exp_emit_fx10_limite=0%2C000&exp_emit_fx10_peso_pol=0%2C00&exp_emit_fx10_peso_reg=0%2C00"
                       "&exp_emit_fx10_peso_int=0%2C00&exp_emit_fx11_limite=0%2C000&exp_emit_fx11_peso_pol=0%2C00"
                       "&exp_emit_fx11_peso_reg=0%2C00&exp_emit_fx11_peso_int=0%2C00&exp_emit_fx12_limite=0%2C000"
                       "&exp_emit_fx12_peso_pol=0%2C00&exp_emit_fx12_peso_reg=0%2C00&exp_emit_fx12_peso_int=0%2C00"
                       "&exp_emit_fx13_limite=0%2C000&exp_emit_fx13_peso_pol=0%2C00&exp_emit_fx13_peso_reg=0%2C00"
                       "&exp_emit_fx13_peso_int=0%2C00&exp_emit_ult_fx_peso_pol=0%2C00&exp_emit_ult_fx_peso_reg=0%2C00"
                       "&exp_emit_ult_fx_peso_int=0%2C00&exp_emit_apos_ult_fx=E&exp_emit_pol_min_ton=280%2C00"
                       "&exp_emit_reg_min_ton=280%2C00&exp_emit_int_min_ton=280%2C00&exp_emit_pol_min=28%2C00"
                       "&exp_emit_reg_min=28%2C00&exp_emit_int_min=28%2C00&exp_emit_pol_min_perc_frt=0%2C00"
                       "&exp_emit_reg_min_perc_frt=0%2C00&exp_emit_int_min_perc_frt=0%2C00&exp_emit_tdc_perc=0%2C00"
                       "&exp_emit_tdc_sobre_frete=0%2C00&exp_emit_min_tdc=0%2C00&exp_emit_trt_perc=0%2C00"
                       "&exp_emit_trt_sobre_frete=0%2C00&exp_emit_min_trt=0%2C00&exp_emit_tda_perc=0%2C00"
                       "&exp_emit_tda_sobre_frete=0%2C00&exp_emit_min_tda=0%2C00&exp_emit_tar_perc=0%2C00"
                       "&exp_emit_tar_sobre_frete=0%2C00&exp_emit_min_tar=0%2C00&exp_emit_vlr_pedagio=1%2C20"
                       "&exp_emit_fec=0%2C00&rec_dest_pol=0%2C00&rec_dest_reg=0%2C00&rec_dest_int=0%2C00"
                       "&rec_dest_perc_seguro=0%2C00&rec_dest_fg_cofins=N&rec_dest_fg_desc_tda=N"
                       "&rec_dest_fg_desc_despacho=N&rec_dest_fg_icms=N&rec_dest_fg_desc_tde=N&rec_dest_fg_desc_pedagio"
                       "=N&rec_dest_fg_desc_outros=N&rec_dest_fg_desc_trt=N&rec_dest_fg_desc_col=N&rec_dest_fg_desc_tar"
                       "=N&rec_dest_fg_desc_tdc=N&rec_dest_vlr_min_merc=0%2C00&rec_dest_ad_valor_pol=0%2C000"
                       "&rec_dest_ad_valor_reg=0%2C000&rec_dest_ad_valor_int=0%2C000&rec_dest_despacho_pol=0%2C00"
                       "&rec_dest_despacho_reg=0%2C00&rec_dest_despacho_int=0%2C00&rec_dest_cubagem=0%2C00"
                       "&rec_dest_fx0_limite=0%2C000&rec_dest_fx0_peso_pol=0%2C00&rec_dest_fx0_peso_reg=0%2C00"
                       "&rec_dest_fx0_peso_int=0%2C00&rec_dest_fx1_limite=0%2C000&rec_dest_fx1_peso_pol=0%2C00"
                       "&rec_dest_fx1_peso_reg=0%2C00&rec_dest_fx1_peso_int=0%2C00&rec_dest_fx2_limite=0%2C000"
                       "&rec_dest_fx2_peso_pol=0%2C00&rec_dest_fx2_peso_reg=0%2C00&rec_dest_fx2_peso_int=0%2C00"
                       "&rec_dest_fx3_limite=0%2C000&rec_dest_fx3_peso_pol=0%2C00&rec_dest_fx3_peso_reg=0%2C00"
                       "&rec_dest_fx3_peso_int=0%2C00&rec_dest_fx4_limite=0%2C000&rec_dest_fx4_peso_pol=0%2C00"
                       "&rec_dest_fx4_peso_reg=0%2C00&rec_dest_fx4_peso_int=0%2C00&rec_dest_fx5_limite=0%2C000"
                       "&rec_dest_fx5_peso_pol=0%2C00&rec_dest_fx5_peso_reg=0%2C00&rec_dest_fx5_peso_int=0%2C00"
                       "&rec_dest_fx6_limite=0%2C000&rec_dest_fx6_peso_pol=0%2C00&rec_dest_fx6_peso_reg=0%2C00"
                       "&rec_dest_fx6_peso_int=0%2C00&rec_dest_fx7_limite=0%2C000&rec_dest_fx7_peso_pol=0%2C00"
                       "&rec_dest_fx7_peso_reg=0%2C00&rec_dest_fx7_peso_int=0%2C00&rec_dest_fx8_limite=0%2C000"
                       "&rec_dest_fx8_peso_pol=0%2C00&rec_dest_fx8_peso_reg=0%2C00&rec_dest_fx8_peso_int=0%2C00"
                       "&rec_dest_fx9_limite=0%2C000&rec_dest_fx9_peso_pol=0%2C00&rec_dest_fx9_peso_reg=0%2C00"
                       "&rec_dest_fx9_peso_int=0%2C00&rec_dest_fx10_limite=0%2C000&rec_dest_fx10_peso_pol=0%2C00"
                       "&rec_dest_fx10_peso_reg=0%2C00&rec_dest_fx10_peso_int=0%2C00&rec_dest_fx11_limite=0%2C000"
                       "&rec_dest_fx11_peso_pol=0%2C00&rec_dest_fx11_peso_reg=0%2C00&rec_dest_fx11_peso_int=0%2C00"
                       "&rec_dest_fx12_limite=0%2C000&rec_dest_fx12_peso_pol=0%2C00&rec_dest_fx12_peso_reg=0%2C00"
                       "&rec_dest_fx12_peso_int=0%2C00&rec_dest_fx13_limite=0%2C000&rec_dest_fx13_peso_pol=0%2C00"
                       "&rec_dest_fx13_peso_reg=0%2C00&rec_dest_fx13_peso_int=0%2C00&rec_dest_ult_fx_peso_pol=0%2C00"
                       "&rec_dest_ult_fx_peso_reg=0%2C00&rec_dest_ult_fx_peso_int=0%2C00&rec_dest_apos_ult_fx=E"
                       "&rec_dest_pol_min_ton=0%2C00&rec_dest_reg_min_ton=0%2C00&rec_dest_int_min_ton=0%2C00"
                       "&rec_dest_pol_min=0%2C00&rec_dest_reg_min=0%2C00&rec_dest_int_min=0%2C00"
                       "&rec_dest_pol_min_perc_frt=0%2C00&rec_dest_reg_min_perc_frt=0%2C00&rec_dest_int_min_perc_frt=0"
                       "%2C00&rec_dest_tdc_perc=0%2C00&rec_dest_tdc_sobre_frete=0%2C00&rec_dest_min_tdc=0%2C00"
                       "&rec_dest_tde_perc=0%2C00&rec_dest_tde_sobre_frete=0%2C00&rec_dest_min_tde=0%2C00"
                       "&rec_dest_trt_perc=0%2C00&rec_dest_trt_sobre_frete=0%2C00&rec_dest_min_trt=0%2C00"
                       "&rec_dest_tda_perc=0%2C00&rec_dest_tda_sobre_frete=0%2C00&rec_dest_min_tda=0%2C00"
                       "&rec_dest_tar_perc=0%2C00&rec_dest_tar_sobre_frete=0%2C00&rec_dest_min_tar=0%2C00"
                       "&rec_dest_vlr_pedagio=0%2C00&rec_dest_comi_fec=0%2C00&acao=A&cgc=38475768000194&seq_cidade=901"
                       "&cod_fil=72&seq_mercadoria=0&fg_filial=E&data_ini_ativ=10%2F06%2F24&dummy=1718136404789")
        data = self.update_query_values(unquote(response.text),
                                        query_model,
                                        'name',
                                        act='ENV2',
                                        dummy=self.get_dummy(),
                                        #data_ini_ativ=datetime.now().strftime("%d/%m/%y"),
                                        **kwargs)

        data = data.replace('+', ' ')
        logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1269", headers=self.headers, data=data)
        logging.info(response.text)
        if 'Erro lendo tabela.' in response.text:
            return False
        else:
            return True

    def op408(self, *args, **kwargs):
        """
            :param kwargs:
            Possible keys include:
                - act: 'LINK_CLI','LINK_MERC','LINK_CID'
                - unidade: sigla
                - f2: unidade
                - f3: tipo unidade (E-expedidora,R-recebedora,A-ambas)
                - f5: cnpj cliente
                - f6: tipo cliente (R-remetente,D-destinatário,P-pagador)
                - f8: codigo mercadoria
                - sigla_emit: rota
                - sigla_dest: rota
                - f9: tipo de frete (C-CIF,F-FOB,A-ambas)
                - comi_unid:

            :type kwargs: dict
            :return: None

            Possible key include if act='LINK_CLI':
                - subcontratado: Códigodatabela:
                - cod_nro_tabela: Cliente:
                - cliente: Como:
                - desc_fg_cliente: Unidade:
                - filial: Como:
                - desc_fg_filial: Mercadoria:
                - mercadoria: Tipodefrete:
                - desc_tp_frete: Rota:
                - exp_cli_emit_pol: Região(%):
                - exp_cli_emit_reg: Interior(%):
                - exp_cli_emit_int: Descontardofrete(basedecálculo):
                - exp_cli_emit_perc_seguro: PIS/COFINS(S/N):
                - exp_cli_emit_fg_cofins: TDA(S/N):
                - exp_cli_emit_fg_desc_tda: Despacho(S/N):
                - exp_cli_emit_fg_desc_despacho: ICMS/ISS(S/N):
                - exp_cli_emit_fg_icms: TDE(S/N):
                - exp_cli_emit_fg_desc_tde: Pedágio(S/N):
                - exp_cli_emit_fg_desc_pedagio: Outros(S/N):
                - exp_cli_emit_fg_desc_outros: TRT(S/N):
                - exp_cli_emit_fg_desc_trt: ComRecParceiro(S/N):
                - exp_cli_emit_fg_desc_recepcao: TAR(S/N):
                - exp_cli_emit_fg_desc_tar: TDC(S/N):
                - exp_cli_emit_fg_desc_tdc: 2.Sobrevalordemercadoria(%):
                - exp_cli_emit_vlr_min_merc: OrigemPólo(%):
                - exp_cli_emit_ad_valor_pol: Região(%):
                - exp_cli_emit_ad_valor_reg: Interior(%):
                - exp_cli_emit_ad_valor_int: 3.Sobrepeso(R$):
                - exp_cli_emit_despacho_pol: Região(R$):
                - exp_cli_emit_despacho_reg: Interior(R$):
                - exp_cli_emit_despacho_int: Cubagem(kg/m3):
                - exp_cli_emit_cubagem: Faixa(AtéKg):
                - exp_cli_emit_fx0_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx0_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx0_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx0_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx1_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx1_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx1_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx1_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx2_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx2_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx2_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx2_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx3_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx3_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx3_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx3_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx4_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx4_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx4_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx4_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx5_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx5_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx5_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx5_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx6_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx6_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx6_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx6_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx7_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx7_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx7_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx7_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx8_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx8_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx8_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx8_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx9_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx9_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx9_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx9_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx10_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx10_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx10_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx10_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx11_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx11_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx11_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx11_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx12_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx12_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx12_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx12_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx13_limite: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx13_peso_pol: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx13_peso_reg: Apósultfaixa(R$/ton):
                - exp_cli_emit_fx13_peso_int: Apósultfaixa(R$/ton):
                - exp_cli_emit_ult_fx_peso_pol: (E-excedente,T-total)
                - exp_cli_emit_ult_fx_peso_reg: (E-excedente,T-total)
                - exp_cli_emit_ult_fx_peso_int: (E-excedente,T-total)
                - exp_cli_emit_apos_ult_fx: (E-excedente,T-total)
                - exp_cli_emit_pol_min_ton: Região(R$/ton):
                - exp_cli_emit_reg_min_ton: Interior(R$/ton):
                - exp_cli_emit_int_min_ton: OrigemPólo(R$):
                - exp_cli_emit_pol_min: Região(R$):
                - exp_cli_emit_reg_min: Interior(R$):
                - exp_cli_emit_int_min: OrigemPólo(%frete):
                - exp_cli_emit_pol_min_perc_frt: Região(%frete):
                - exp_cli_emit_reg_min_perc_frt: Interior(%frete):
                - exp_cli_emit_int_min_perc_frt: 5.AdicionarTAR,TDCepedágio:
                - exp_cli_emit_tar_perc: TARsobrefrete(%):
                - exp_cli_emit_tar_sobre_frete: ComTARmin(R$):
                - exp_cli_emit_min_tar: SobreTDC(%):
                - exp_cli_emit_tdc_perc: TDCsobrefrete(%):
                - exp_cli_emit_tdc_sobre_frete: ComTDCmin(R$):
                - exp_cli_emit_min_tdc: Pedágio(R$/fraç100Kg):
                - exp_cli_emit_vlr_pedagio: 6.ComissãosobreCargaFechada(%):
                - exp_cli_emit_fec: ComoReceptora:
                - rec_cli_dest_pol: Região(%):
                - rec_cli_dest_reg: Interior(%):
                - rec_cli_dest_int: Descontardofrete(basedecálculo):
                - rec_cli_dest_perc_seguro: PIS/COFINS(S/N):
                - rec_cli_dest_fg_cofins: TDA(S/N):
                - rec_cli_dest_fg_desc_tda: Despacho(S/N):
                - rec_cli_dest_fg_desc_despacho: ICMS/ISS(S/N):
                - rec_cli_dest_fg_icms: TDE(S/N):
                - rec_cli_dest_fg_desc_tde: Pedágio(S/N):
                - rec_cli_dest_fg_desc_pedagio: Outros(S/N):
                - rec_cli_dest_fg_desc_outros: TRT(S/N):
                - rec_cli_dest_fg_desc_trt: Coleta(S/N):
                - rec_cli_dest_fg_desc_col: TAR(S/N):
                - rec_cli_dest_fg_desc_tar: TDC(S/N):
                - rec_cli_dest_fg_desc_tdc: 2.Sobrevalordemercadoria(%):
                - rec_cli_dest_vlr_min_merc: DestinoPólo(%):
                - rec_cli_dest_ad_valor_pol: Região(%):
                - rec_cli_dest_ad_valor_reg: Interior(%):
                - rec_cli_dest_ad_valor_int: 3.Sobrepeso(R$):
                - rec_cli_dest_despacho_pol: Região(R$):
                - rec_cli_dest_despacho_reg: Interior(R$):
                - rec_cli_dest_despacho_int: Cubagem(kg/m3):
                - rec_cli_dest_cubagem: Faixa(AtéKg):
                - rec_cli_dest_fx0_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx0_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx0_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx0_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx1_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx1_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx1_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx1_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx2_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx2_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx2_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx2_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx3_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx3_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx3_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx3_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx4_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx4_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx4_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx4_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx5_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx5_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx5_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx5_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx6_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx6_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx6_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx6_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx7_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx7_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx7_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx7_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx8_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx8_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx8_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx8_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx9_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx9_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx9_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx9_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx10_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx10_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx10_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx10_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx11_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx11_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx11_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx11_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx12_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx12_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx12_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx12_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx13_limite: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx13_peso_pol: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx13_peso_reg: Apósultfaixa(R$/ton):
                - rec_cli_dest_fx13_peso_int: Apósultfaixa(R$/ton):
                - rec_cli_dest_ult_fx_peso_pol: (E-excedente,T-total)
                - rec_cli_dest_ult_fx_peso_reg: (E-excedente,T-total)
                - rec_cli_dest_ult_fx_peso_int: (E-excedente,T-total)
                - rec_cli_dest_apos_ult_fx: (E-excedente,T-total)
                - rec_cli_dest_pol_min_ton: Região(R$/ton):
                - rec_cli_dest_reg_min_ton: Interior(R$/ton):
                - rec_cli_dest_int_min_ton: DestinoPólo(R$):
                - rec_cli_dest_pol_min: Região(R$):
                - rec_cli_dest_reg_min: Interior(R$):
                - rec_cli_dest_int_min: DestinoPólo(%frete):
                - rec_cli_dest_pol_min_perc_frt: Região(%frete):
                - rec_cli_dest_reg_min_perc_frt: Interior(%frete):
                - rec_cli_dest_int_min_perc_frt: 5.AdicionarTDC,TDE,TRT,TDA,TARepedágio:
                - rec_cli_dest_tdc_perc: TDCsobrefrete(%):
                - rec_cli_dest_tdc_sobre_frete: ComTDCmin(R$):
                - rec_cli_dest_min_tdc: SobreTDE(%):
                - rec_cli_dest_tde_perc: TDEsobrefrete(%):
                - rec_cli_dest_tde_sobre_frete: ComTDEmin(R$):
                - rec_cli_dest_min_tde: SobreTRT(%):
                - rec_cli_dest_trt_perc: TRTsobrefrete(%):
                - rec_cli_dest_trt_sobre_frete: ComTRTmin(R$):
                - rec_cli_dest_min_trt: SobreTDA(%):
                - rec_cli_dest_tda_perc: TDAsobrefrete(%):
                - rec_cli_dest_tda_sobre_frete: ComTDAmin(R$):
                - rec_cli_dest_min_tda: SobreTAR(%):
                - rec_cli_dest_tar_perc: TARsobrefrete(%):
                - rec_cli_dest_tar_sobre_frete: ComTARmin(R$):
                - rec_cli_dest_min_tar: Pedágio(R$/fraç100Kg):
                - rec_cli_dest_vlr_pedagio: 6.Sobrecargafechada(%):
                - rec_cli_dest_comi_fec: Inclusão:
                - acao:
                - cgc:
                - seq_cliente:
                - cod_fil:
                - seq_mercadoria:
                - fg_cliente:
                - fg_filial:
                - tp_frete:
                - data_ini_ativ:
                - cod_fil_emit:
                - cod_fil_dest:
            :type kwargs: dict
            :return: None
        """
        self.last_opssw = '408'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        # second query post
        data = f"sequencia={self.last_opssw}&dummy=1686918186137"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0507", headers=self.headers, data=data)

        # showing results

        logging.info(response.text)

        filial = self._op408_get_filial(kwargs['unidade'])
        logging.info(filial)

        # query filters to request record
        act = kwargs.pop('act') if 'act' in kwargs else 'LINK_CLI'
        data = f"act={act}&f2={kwargs['unidade']}&filial={filial}&dummy=1691768377282"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0507", headers=self.headers, data=data)

        logging.info(response.text)

        cgc = self._op408_get_cgc(response.text)

        data = f"act=&f2={kwargs['unidade']}&filial={filial}&web_body={cgc}&msgx=&dummy=1691768377417"
        logging.info(data)
        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw0507", headers=self.headers, data=data)
        logging.info(response.text)

        params = cgc.split("'")[3].split('?')[1]
        data = f'{params}&dummy=1691768377851'
        logging.info(data)

        if 'cliente' in args:
            return self._op408_link_cli(data, **kwargs)

        if 'mercadoria' in args:
            self._op408_link_merc(data, **kwargs)

        if 'cidade' in args:
            self._op408_link_city(data, **kwargs)


if __name__ == '__main__':
    with Ssw408() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.op408()
