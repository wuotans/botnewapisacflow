import fitz  # PyMuPDF
import json
import csv
import logging
from itertools import zip_longest
from collections import UserList
from typing import List
#from priority_classes.tesseract.tesseract import TesseractOCR
import os
from datetime import datetime


class Bloco:
    def __init__(self, item_json: dict, index_page=0):
        """
                "column_obj": {
                    "text": "Emiss\u00e3o",
                    "1x": 37.78900146484375,
                    "1y": 267.33612060546875,
                    "2x": 68.45716857910156,
                    "2y": 278.3267517089844,
                    "name": "emissao"
                }

                text = span.get("text", "")
                bbox = span.get("bbox", "")
                {'size': 7.999000072479248, 'flags': 0, 'font': 'Helvetica', 'color': 0, 'ascender': 1.0750000476837158, 'descender': -0.29899999499320984, 'text': '0,00', 'origin': [1386.3489990234375,
        1004.93505859375], 'bbox': [1386.3489990234375, 996.3361206054688, 1401.9149169921875, 1007.3267822265625]}
                PONTO LEFT
                +------------
                |           |
                |-----------+
                            PONTO RIGHT
        """
        try:
            self.item_json: dict = item_json
            self.value = item_json.get("text", "")
            self.bbox = item_json.get("bbox", [])
            self.LX = self.bbox[0]
            self.LY = self.bbox[1]
            self.RX = self.bbox[2]
            self.RY = self.bbox[3]
            self.conteudo: list[list["Bloco"]]
            self.CURRENT_PAGE = index_page
        except:
            self.item_json = None
            self.value = ""
            self.bbox = []
            self.LX = 0
            self.LY = 0
            self.RX = 0
            self.RY = 0
            self.conteudo = []
            self.CURRENT_PAGE = 0

    def set_conteudo(self, conteudo: list[list["Bloco"]]):
        self.conteudo = conteudo

    def find_all_match_with_this_bloco(
        self, lado="left", FUNC_VALIDA=None, **kwargs
    ) -> list["Bloco"]:
        printar = kwargs.get("printar", False)
        all_associate_items: list["Bloco"] = []
        # FUNC_VALIDA é uma duncao que voce pode passar para validar se o campo encontrado deve ser adicionando ou nao
        # no caso se ele segue um padrão desejado.

        if not FUNC_VALIDA:
            # se nenhum for passado, ajusta para somente retornar True e passar pela validaçao
            def FUNC_VALIDA(_):
                return True

        # verifica tambe se as cooredenadas x e y da palavra da vez são as mesmas da palavra base (NOME DA COLUNA ENCONTRADO)
        # para não repetir e encontrar a propria palavra do titulo
        for spam in self.conteudo[self.CURRENT_PAGE]:
            # bbox de cada item e vê se comeca nesse limite (se esta entre os dois limites)

            if spam != self and FUNC_VALIDA(spam.value):
                if lado == "left":
                    lim_mim, lim_max = intervalo_margem_erro(self.LX, **kwargs)
                    if lim_mim <= spam.LX <= lim_max:
                        if printar:
                            logging.info(
                                f"{spam.value} = {self.value}       {lim_mim} <= {spam.LX} <= {lim_max}"
                            )
                        all_associate_items.append(spam)

                elif lado == "right":
                    lim_mim, lim_max = intervalo_margem_erro(self.RX, **kwargs)
                    if lim_mim <= spam.RX <= lim_max:
                        if printar:
                            logging.info(
                                f"{spam.value} = {self.value}       {lim_mim} <= {spam.RX} <= {lim_max}"
                            )
                        all_associate_items.append(spam)

                elif lado == "top":
                    lim_mim, lim_max = intervalo_margem_erro(self.LY, **kwargs)
                    if lim_mim <= spam.LY <= lim_max:
                        if printar:
                            logging.info(
                                f"{spam.value} = {self.value}       {lim_mim} <= {spam.LY} <= {lim_max}"
                            )
                        all_associate_items.append(spam)

                elif lado == "bottom":
                    lim_mim, lim_max = intervalo_margem_erro(self.RY, **kwargs)
                    if lim_mim <= spam.RY <= lim_max:
                        if printar:
                            logging.info(
                                f"{spam.value} = {self.value}       {lim_mim} <= {spam.RY} <= {lim_max}"
                            )
                        all_associate_items.append(spam)
        return all_associate_items


class ListaDeColunas(UserList):
    def __init__(self, conteudo: list[list[Bloco]]):
        super().__init__()
        self.conteudo = conteudo

    def __getitem__(self, key):
        if isinstance(key, str):
            for coluna in self.data:
                if coluna.value.strip().upper() == key.strip().upper():
                    return coluna
            raise KeyError(f"Coluna with name '{key}' not found")
        return super().__getitem__(key)

    def append(self, bloco: Bloco):
        logging.info(f"Adicionando bloco coluna: {bloco.value}")
        super().append(bloco)

    def print_columns(self):
        logging.info(f"Todas Colunas: ")
        for coluna in self.data:
            logging.info(f"    - {coluna.value}")


class ReadPdfTable:
    def __init__(
        self,
        pdf_path="",
        pdf_path_to_save_csv="./dict.csv",
        LOG=None,
        extract_with_tesseract=False,
        tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        folder_temp_images="temp",
    ):
        # extract_with_tesseract nao esta funcionando por enquanto
        if LOG:
            global print
            print = LOG.reg
        if extract_with_tesseract:
            self.TESS = TesseractOCR(tesseract_cmd=tesseract_cmd)
        self.folder_temp_images = folder_temp_images

        self.pdf_path = pdf_path
        self.json_struc_pdf_str = ""

        self.conteudo: list[list[Bloco]] = []

        self.CURRENT_PAGE = 0
        # extrai o json em texto contendo todas as informações de todos os blocos e palavras do pdf
        if not extract_with_tesseract:
            self.load_conteudo_from_all_pages()
            # self._xtract_text_with_positions()
            # # converte essas string de json em dict
            # self._get_dict_from_json_struc_pdf_str()
            # # percorre por todos os blocos e palavras obtendo seu conteudo e seu bbox
            # self.load_data_info_pdf()
        else:
            folder_pages = self.TESS.pdf_to_images(pdf_path, self.folder_temp_images)
            images = os.listdir(folder_pages)
            path_image = os.path.join(folder_pages, images[0])
            conteudo = self.TESS.extract_text_and_coordinates(path_image)
            self.load_data_info_pdf_tesseract(conteudo)

        self.add_conteudo_to_blocos()

        self.pdf_path_to_save_csv = pdf_path_to_save_csv
        self.COLUMNS: ListaDeColunas = ListaDeColunas(self.conteudo)

    def set_current_page(self, page=0):
        self.CURRENT_PAGE = page
        self.add_conteudo_to_blocos()
        self.add_conteudo_to_blocos_column()

    def print_conteudo(self):
        for pagina in self.conteudo:
            for i in pagina:
                logging.info(i.value)

    def load_conteudo_from_all_pages(self):
        # Abrir o documento PDF
        document = fitz.open(self.pdf_path)
        self.conteudo = []
        # Iterar sobre as páginas do documento
        for page_num in range(len(document)):
            page = document[page_num]
            raw_json = self.load_raw_json_from_page(page)
            dict_json = self.get_dict_from_raw_json_text(raw_json)
            conteudo_pagina = self.load_data_info_pdf(dict_json)
            self.conteudo.append(conteudo_pagina)

    def load_raw_json_from_page(self, page):
        return page.get_text("json")

    def get_dict_from_raw_json_text(self, raw_json):
        return json.loads(raw_json)

    # def _xtract_text_with_positions(self):
    #     # Abrir o documento PDF
    #     document = fitz.open(self.pdf_path)

    #     # Iterar sobre as páginas do documento
    #     for page_num in range(len(document)):
    #         page = document[page_num]

    #         # Extrair o texto e as posições
    #         self.json_struc_pdf_str = page.get_text("json")
    #         return self.json_struc_pdf_str

    # def _get_dict_from_json_struc_pdf_str(self):
    #     self.dic_struct: dict = json.loads(self.json_struc_pdf_str)

    def load_data_info_pdf(self, dict_json: dict):
        cont = []
        blocks = dict_json.get("blocks", [])
        for itens_bloco in blocks:
            if lines := itens_bloco.get("lines"):
                # row = []
                for item in lines:
                    spans = item.get("spans", [])
                    for span in spans:
                        bloco = Bloco(span)
                        cont.append(bloco)
        # self.conteudo = cont
        return cont

    def load_data_info_pdf_tesseract(self, conteudo):
        cont = []

        for item in conteudo:
            # logging.info(item)
            bloco = Bloco(item)
            cont.append(bloco)
        self.conteudo = cont
        # self.print_conteudo()
        return cont

    def add_conteudo_to_blocos(self):
        for bloco in self.conteudo[self.CURRENT_PAGE]:
            bloco.set_conteudo(self.conteudo)
            bloco.CURRENT_PAGE = self.CURRENT_PAGE

    def add_conteudo_to_blocos_column(self):
        for bloco in self.COLUMNS:
            bloco.set_conteudo(self.conteudo)
            bloco.CURRENT_PAGE = self.CURRENT_PAGE

    def find_item_in_list(self, sring: str, string_contida=False):

        for bloco in self.conteudo[self.CURRENT_PAGE]:
            # procura na lista onde aparce o primeiro item do conjunto
            if string_contida:
                if sring.strip().upper() in bloco.value.strip().upper():
                    return bloco
            else:
                if sring.strip().upper() == bloco.value.strip().upper():
                    return bloco
        # return Bloco({})
        raise ValueError(f"Nenhum item encontrado para a string: {sring}")

    def find_column(self, column_string) -> Bloco:

        bloco_column: Bloco = self.find_item_in_list(column_string)
        self.COLUMNS.append(bloco_column)
        return bloco_column


def intervalo_margem_erro(coord, **kwargs):
    printar = kwargs.get("printar", False)
    limiar_menos = kwargs.get("limiar_menos", 5)
    limiar_mais = kwargs.get("limiar_mais", 5)
    # return: tupla com limite inferior e superior
    lim_mim, lim_max = int(coord - limiar_menos), int(coord + limiar_mais)
    if printar:
        logging.info(f" -  ({lim_mim} - {coord} - {lim_max})")
    return lim_mim, lim_max


def cruza_linha_coluna(bloco_linha: Bloco, items_coluna: list[Bloco], printar=False):
    """cruza a linha do bloco atual com todas as linhas da coluna.
    compara a coordenada y do lado esquerdo para ver se estao procimos (na mesma linha)
    """
    items: list[Bloco] = []
    lim_min_base, lim_max_base = intervalo_margem_erro(bloco_linha.LY, printar=False)
    for item_coluna in items_coluna:
        if lim_min_base <= item_coluna.LY <= lim_max_base:
            if printar:
                logging.info(
                    f"o bloco ({item_coluna.value}) esta na mesma linha que ({bloco_linha.value})\n       {lim_min_base} <= {item_coluna.LY} <= {lim_max_base}"
                )
            items.append(item_coluna)

    return items if items else [Bloco({})]


def is_valid_date(item=""):
    try:
        datetime.strptime(item, "%d/%m/%Y")
        return True
    except ValueError:
        return False


################################################################################################
################################################################################################
################################################################################################
# Exemplo de implementação


def exemplo_completo():
    caminho_completo_arquivo = os.path.abspath(__file__)
    caminho_completo_diretorio = os.path.dirname(caminho_completo_arquivo)

    # os dados extraidos sao salvos no csv enquanto vao sendo extraidos.
    # isso por que, se for carregar tudo na memoria pra depois salvar, isso é muio custoso.
    with open(
        os.path.join(caminho_completo_diretorio, "extract.csv"),
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file, delimiter=";")

        # as colunas na sequencia em que voce vai procurar no pdf. ja adiciona no csv
        columns = ["emissao", "cia", "ctrc_minuta_nfst", "total"]
        writer.writerow(columns)

        # carregara o pdf e ja irá ler os blocos de todas as paginas e deixar preparados
        pdf_table = ReadPdfTable(
            pdf_path=os.path.join(caminho_completo_diretorio, "exemplo_pdf.pdf")
        )

        """adiciona as colunas que deseja encontrar
        neste caso ele vai literalmente procurar o bloco e adicionar á lista de colunas
        não é um processo necessário, só fiz pra facilitar minha vida na extração das linhas futuramente
        essa string tem que ser a mesma string do bloco que você procura
        PODE USAR O METODO ABAIXO PARA VER TODOS OS BLOCOS QUE FORAM EXTRAIDOS EM TODAS AS PAGINAS"""
        # pdf_table.print_conteudo()

        pdf_table.find_column("Emissão")
        pdf_table.find_column("CIA")
        pdf_table.find_column("MINUTA")
        pdf_table.find_column("Total")

        pdf_table.COLUMNS.print_columns()

        # itens que vou procurar em cada pagina
        pre_fatura = None
        total_fatura = None

        """as paginas sao carregadas em conteudo, composto por:
        - uma lista em que cada item é uma pagina
        - cada pagina é uma outra lista em que cada item é uma instancia de Bloco()
        - cada bloco contém itens como:
            - item_json
            - value: valor text
            - bbox
            - LX: coordenada X Left
            - LY: coordenada Y Left
            - RX: coordenada X Right
            - RY: coordenada Y Right
            - conteudo
            - CURRENT_PAGE
        """
        for index_curent_page, current_page in enumerate(pdf_table.conteudo):
            # setta essa pagina como a ser usada atualmente
            pdf_table.set_current_page(index_curent_page)

            # obtém o bloco da coluna desejada
            col_emissao = pdf_table.COLUMNS["Emissão"]
            """agora busca todos os itens na pagina atual que possuem coordenadas LEFT, ou seja X
            proximas (alinhadas) com o bloco da coluna
            - basicamente são todos os blocos que sao verticalmente compatíveis com a coluna"""
            items_emissao: list[Bloco] = col_emissao.find_all_match_with_this_bloco(
                limiar_menos=10, limiar_mais=0, FUNC_VALIDA=is_valid_date, lado="left"
            )
            """is_valid_date: é uma funcao que vai validar os blocos, só retorna aqueles que atendam ao especificado
            repare que algumas colunas indesejadas podem ser encontradas, preciso somente daquelas que cmeçam com uma data
            então valido isso."""

            items_cia: list[Bloco] = pdf_table.COLUMNS[
                "CIA"
            ].find_all_match_with_this_bloco(
                limiar_menos=20, limiar_mais=0, lado="left"
            )

            items_minuta: list[Bloco] = pdf_table.COLUMNS[
                "MINUTA"
            ].find_all_match_with_this_bloco(
                limiar_menos=0, limiar_mais=30, lado="left"
            )

            """Neste caso, a coluna Total tem numeros e eles ficam alinhados á direita
            , então se procurar pelos blocos alinhados pela esquerda alguns não vao ser encontrados, por isso uso Right"""
            items_total: list[Bloco] = pdf_table.COLUMNS[
                "Total"
            ].find_all_match_with_this_bloco(
                limiar_menos=6, limiar_mais=6, lado="right"
            )

            """é importante se atentar á
            - limiar_menos=6
            - limiar_mais=6
            Este limiar é uma margem de erro adicionada para procurar os itens pelas cooredanadas
            Isso por que alguns blocos podem estar um pouquinho desalinhados, então nem sempre serão encontrados. 
            Ajuste conforme necessario até todos os itens desejados serem encontrados.
            tenha cuidado para nao colocar muito grande, se não itens ao redor da faixa podem ser detectados. 
            """


            # cada coluna obteve uma quantidade diferente de itens, nao tem problema. vamos procurar compativeis para todos eles
            # então obtemos o tamanho da maior lista
            max_length = max(
                len(lst)
                for lst in [items_emissao, items_cia, items_minuta, items_total]
            )
            # devemos escolher uma coluna base (confiável) para cruzar com as outras colunas e definir quais são linhas validas
            # neste caso escolhi Emissão, pois a validação de data garante que as linhas pegas são sempre aquelas que me interessam
            for index in range(max_length):
                # obtem o item N dessa coluna base
                coluna_base = (
                    items_emissao[index] if index < len(items_emissao) else Bloco({})
                )
                ## caso queira escolher outra coluna como base e ver qual o resultado:
                # coluna_base = items_cia[index] if index < len(items_cia) else Bloco({})
                # coluna_base = items_minuta[index] if index < len(items_minuta) else Bloco({})
                # coluna_base = items_total[index] if index < len(items_total) else Bloco({})
                if coluna_base.item_json:
                    # procura qual item de cada coluna esta horizontalmente alinhada com o item da coluna base
                    it_emissao = " ".join(
                        bloco.value
                        for bloco in cruza_linha_coluna(
                            coluna_base, items_emissao, printar=True
                        )
                    )
                    it_cia = " ".join(
                        bloco.value
                        for bloco in cruza_linha_coluna(
                            coluna_base, items_cia, printar=True
                        )
                    )
                    it_minuta = " ".join(
                        bloco.value
                        for bloco in cruza_linha_coluna(
                            coluna_base, items_minuta, printar=True
                        )
                    )
                    it_total = " ".join(
                        bloco.value
                        for bloco in cruza_linha_coluna(
                            coluna_base, items_total, printar=True
                        )
                    )

                    logging.info(f"{it_emissao} ; {it_cia} ; {it_minuta} ; {it_total}")
                    writer.writerow([it_emissao, it_cia, it_minuta, it_total])

            # para cada pagina percorrida tenta encontrar a coluna de total
            # a ultima encontrada sera a usada (ultimas paginas)
            try:
                # encontra o bloco de label da fatura na pagina atual
                bloco_total_fatura = pdf_table.find_item_in_list("Total Fatura:")
                # sabendo a posicao horizontal do bloco do label da fatura cruza ele com a posicao vertical da coluna total
                # é onde estará a informação do total
                it_total = " ".join(
                    bloco.value
                    for bloco in cruza_linha_coluna(
                        bloco_total_fatura, items_total, printar=True
                    )
                )
                logging.info(f"Total Fatura: {it_total}")
                total_fatura = it_total
            except:
                logging.info(f"Total Fatura não foi encontrado nessa pagina. Prosseguindo...")

            try:
                # obtem o label da pre fatura
                label_pre_fatura = pdf_table.find_item_in_list("Pré-Fatura:")
                logging.info(f"Label: {label_pre_fatura.value}")
                # obtem os valores que estao na mesma linha da pre fatura
                values_pre_fatura = label_pre_fatura.find_all_match_with_this_bloco(
                    limiar_menos=5, limiar_mais=5, lado="bottom"
                )
                for i in values_pre_fatura:
                    logging.info(f"    - Retornos: {i.value}")

                logging.info(f"valor: {values_pre_fatura[0].value}")
                if values_pre_fatura:
                    pre_fatura = values_pre_fatura[0].value
            except:
                logging.info(f"Pré-Fatura nao encontrada nesta pagina. Prosseguindo...")
        logging.info(f"pre_fatura: {pre_fatura}")
        logging.info(f"total_fatura: {total_fatura}")


def exemplo_simples():
    """
    Neste exemplo vamos extrair somente uma informação do pdf.
    No caso, o nome do cliente que se encontra no cabeçalho do pdf."""

    caminho_completo_arquivo = os.path.abspath(__file__)
    caminho_completo_diretorio = os.path.dirname(caminho_completo_arquivo)

    # os dados extraidos sao salvos no csv enquanto vao sendo extraidos.
    # isso por que, se for carregar tudo na memoria pra depois salvar, isso é muio custoso.

    # carregara o pdf e ja irá ler os blocos de todas as paginas e deixar preparados
    pdf_table = ReadPdfTable(
        pdf_path=os.path.join(caminho_completo_diretorio, "exemplo_pdf.pdf")
    )

    """
    essa string tem que ser a mesma string do bloco que você procura
    PODE USAR O METODO ABAIXO PARA VER TODOS OS BLOCOS QUE FORAM EXTRAIDOS EM TODAS AS PAGINAS"""
    
    pdf_table.print_conteudo()

    """as paginas sao carregadas em conteudo, composto por:
    - uma lista em que cada item é uma pagina
    - cada pagina é uma outra lista em que cada item é uma instancia de Bloco()
    - cada bloco contém itens como:
        - item_json
        - value: valor text
        - bbox
        - LX: coordenada X Left
        - LY: coordenada Y Left
        - RX: coordenada X Right
        - RY: coordenada Y Right
        - conteudo
        - CURRENT_PAGE
    """

    # sabemos que a informacao esta sempre na primeira pagina, entao nao precisamos percorrer todas. basta settar ela como current com:
    pdf_table.set_current_page(0)

    # agora buscamos o bloco pela string do label que queremos. Sempre retorna o primeiro item encontrado
    bloco_label_cliente = pdf_table.find_item_in_list("Cliente:")

    '''tendo o label, sabemos que a informação "CEVA LOGISTICS LTDA" se encontra na mesma linha
    - vamos comparar todos com a coordenada bottom (que seria a coordenada Y do lado direito)
                  ^ (top _ Y)
    (left _ X) 🡠 +------------
                  |           |
                  |-----------+ 🡢 (Right _ X)
                            🡣 (bottom _ Y)
    '''
    items_cliente: list[Bloco] = bloco_label_cliente.find_all_match_with_this_bloco(
        limiar_menos=5, limiar_mais=5, lado="bottom"
    )

    # isso retorna os itens encontrados. ajustamos limiar limiar_menos (subtrai de Y) e limiar_mais (acrescenta á Y) 
    # faixa_de_busca = limiar_menos <= coordenada_do_bloco_referencia <= limiar_mais
    logging.info('Todos os itens encontrados na mesma linha de <Cliente:>')
    for bloco_da_linha in items_cliente:
        logging.info(f'    - {bloco_da_linha.value}')
    ''' note que esta busca retorna os unicos 3 itens encontrados nessa linha, exceto o próprio bloco "Cliente:" que é ignorado
    CEVA LOGISTICS LTDA
    BU:
    4009301

    Como sabemos que o nome do cliente é o primeiro encontrado na pagina, da esquerda para a direita, depois do prório label do cliente
    então basta pegar o primeiro item retornado.
    '''
    razao_social_cliente = items_cliente[0]

    logging.info(f'Clente encontrado: {razao_social_cliente.value}')


if __name__ == "__main__":
    exemplo_simples()

    # exemplo_completo()
    # observe "extract.csv extraido comas infomrações"
