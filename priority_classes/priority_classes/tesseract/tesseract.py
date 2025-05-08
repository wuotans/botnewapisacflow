import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO
import os
import cv2
from PIL import Image
import shutil
import os
import logging


class TesseractOCR:
    def __init__(self, tesseract_cmd=None, lang="eng"):
        """
        Inicializa a classe TesseractOCR.

        :param tesseract_cmd: Caminho para o executável do Tesseract (se necessário).
        :param lang: Idioma a ser usado pelo Tesseract (padrão: inglês).
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.lang = lang

    def extract_text_and_coordinates(self, image_path):
        # Abrir a imagem
        img = Image.open(image_path)
        """
        config

        -------------------------- Parâmetro --oem
        0 = Legacy engine only:
        Utiliza apenas o motor OCR legado, que é baseado em um motor de reconhecimento de caracteres mais antigo.
        Este modo pode ser útil para documentos que o motor legado processa melhor, mas geralmente é menos preciso do que os motores mais modernos.

        1 = Neural nets LSTM engine only:
        Utiliza apenas o motor baseado em redes neurais LSTM (Long Short-Term Memory).
        Este motor é mais avançado e geralmente oferece melhor precisão, especialmente para textos complexos e escritos à mão.

        2 = Legacy + LSTM engines:
        Utiliza uma combinação dos motores legado e LSTM.
        Pode fornecer uma boa combinação de velocidade e precisão, usando ambos os motores para tentar obter os melhores resultados.

        3 = Default, based on what is available:
        Este é o valor padrão e seleciona automaticamente o melhor motor disponível com base no contexto e nas configurações do Tesseract instaladas.
        Geralmente usa o motor LSTM se estiver disponível, mas pode usar o motor legado se necessário.
        
        
        
        -------------------------- Parâmetro --psm
        --psm (Page Segmentation Mode) define como o Tesseract deve segmentar a página antes de executar o OCR. Existem vários modos disponíveis, cada um adequado para diferentes tipos de documentos e estruturas de texto:

        0 = Orientação e detecção de script apenas:
        Apenas detecta a orientação da página e o script do texto, sem realizar o OCR real.
        Útil para identificar a direção do texto antes de aplicar o OCR.

        1 = Segmentação automática da página com OCR:
        Segmenta a página automaticamente e executa o OCR em todo o conteúdo detectado.
        Este é o modo padrão e geralmente funciona bem para a maioria dos documentos.

        3 = Segmentação total da linha de texto:
        Segmenta a página em linhas de texto completas.
        Útil para documentos que têm texto organizado em linhas distintas, como listas ou tabelas.

        6 = Supõe um único bloco de texto uniforme:
        Supõe que a página inteira é um único bloco de texto uniforme.
        Útil para documentos simples com uma única área de texto contínua.

        11 = Supõe uma linha de texto no valor de entrada:
        Supõe que o documento contém apenas uma única linha de texto.
        Útil para processar entradas de texto simples, como frases curtas ou legendas.
        """
        # Usar pytesseract para extrair dados de OCR com coordenadas
        data = pytesseract.image_to_data(
            img, config=r"--oem 3 --psm 1", output_type=pytesseract.Output.DICT
        )
        # data = pytesseract.image_to_pdf_or_hocr(img)
        # data = pytesseract.image_to_boxes(img)
        # data = pytesseract.image_to_osd(img)
        # data = pytesseract.image_to_alto_xml(img)
        # data = pytesseract.image_to_string(img)
        # return data
        # Lista para armazenar os blocos de texto e suas coordenadas
        blocks = []

        # Iterar sobre os dados extraídos
        n_boxes = len(data["level"])
        for i in range(n_boxes):
            text = data["text"][i]
            if text.strip():
                item = {
                    "text": text.strip(),
                    "bbox": [
                        data["left"][i],
                        data["top"][i],
                        data["left"][i] + data["width"][i],
                        data["top"][i] + data["height"][i],
                    ],
                }
                blocks.append(item)

        return blocks

    def extract_text_from_pdf_fitz(self, pdf_path):
        try:
            extracted_text = ""
            # Abre o arquivo PDF
            with fitz.open(pdf_path) as pdf_document:
                num_pages = pdf_document.page_count
                for page_num in range(num_pages):
                    page = pdf_document.load_page(page_num)
                    page_text = page.get_text()
                    extracted_text += page_text
            return extracted_text
        except Exception as e:
            return str(e)

    def mark_region(self, image_path):
        im = cv2.imread(image_path)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30
        )

        # Dilate to combine adjacent text contours
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        dilate = cv2.dilate(thresh, kernel, iterations=4)

        # Find contours, highlight text areas, and extract ROIs
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        line_items_coordinates = []
        for c in cnts:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)

            if y >= 600 and x <= 1000:
                if area > 10000:
                    image = cv2.rectangle(
                        im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3
                    )
                    line_items_coordinates.append([(x, y), (2200, y + h)])

            if y >= 2400 and x <= 2000:
                image = cv2.rectangle(
                    im, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3
                )
                line_items_coordinates.append([(x, y), (2200, y + h)])

        return im, line_items_coordinates

    def show_images_with_boxes(self, image_paths):
        for image_path in image_paths:
            image, boxes = self.mark_region(image_path)
            logging.info(boxes)
            cv2.imshow("Image with Boxes", image)
            cv2.waitKey(0)  # Pressione qualquer tecla para fechar a janela
        cv2.destroyAllWindows()

    def set_language(self, lang):
        """
        Define o idioma a ser usado pelo Tesseract.

        :param lang: Idioma a ser usado pelo Tesseract.
        """
        self.lang = lang

    def read_text_from_image(self, image_path, **kwargs):
        """
        Lê o texto de uma imagem usando Tesseract OCR.

        :param image_path: Caminho para a imagem.
        :param kwargs: Configurações adicionais do Tesseract.
        :return: Texto extraído da imagem.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"A imagem '{image_path}' não foi encontrada.")

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=self.lang, **kwargs)
        return text

    def read_text_from_image_object(self, image_object, **kwargs):
        """
        Lê o texto de um objeto de imagem usando Tesseract OCR.

        :param image_object: Objeto de imagem (PIL.Image).
        :param kwargs: Configurações adicionais do Tesseract.
        :return: Texto extraído da imagem.
        """
        text = pytesseract.image_to_string(image_object, lang=self.lang, **kwargs)
        return text

    def extract_text_from_pdf(self, pdf_path):
        """
        Lê o texto de um arquivo PDF convertendo-o em imagens e usando Tesseract OCR.

        :param pdf_path: Caminho para o arquivo PDF.
        :return: Texto extraído do PDF.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"O PDF '{pdf_path}' não foi encontrado.")

        # Abre o arquivo PDF
        document = fitz.open(pdf_path)
        text = ""

        # Itera sobre cada página do PDF
        for page_number in range(len(document)):
            page = document.load_page(page_number)
            pix = page.get_pixmap()  # Converte a página em uma imagem

            # Converte a imagem para bytes e usa PIL para abrir a imagem
            img_bytes = pix.tobytes(output="png")  # Especifica o formato como 'png'
            img = Image.open(BytesIO(img_bytes))

            # Extrai o texto da imagem usando Tesseract
            text += pytesseract.image_to_string(img)

        return text

    def get_tesseract_version(self):
        """
        Obtém a versão do Tesseract OCR instalada.

        :return: Versão do Tesseract OCR.
        """
        return pytesseract.get_tesseract_version()

    def image_to_boxes(self, image_path, **kwargs):
        """
        Obtém as caixas delimitadoras de caracteres de uma imagem.

        :param image_path: Caminho para a imagem.
        :param kwargs: Configurações adicionais do Tesseract.
        :return: Caixas delimitadoras dos caracteres na imagem.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"A imagem '{image_path}' não foi encontrada.")

        image = Image.open(image_path)
        boxes = pytesseract.image_to_boxes(image, lang=self.lang, **kwargs)
        return boxes

    def image_to_data(self, image_path, **kwargs):
        """
        Obtém os dados detalhados de OCR de uma imagem.

        :param image_path: Caminho para a imagem.
        :param kwargs: Configurações adicionais do Tesseract.
        :return: Dados detalhados do OCR.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"A imagem '{image_path}' não foi encontrada.")

        image = Image.open(image_path)
        data = pytesseract.image_to_data(image, lang=self.lang, **kwargs)
        return data

    def pdf_to_images(self, pdf_path, output_folder, image_format="png", dpi=300):
        """
        Converte um arquivo PDF em imagens, salvando cada página como uma imagem separada com a resolução especificada.

        :param pdf_path: Caminho para o arquivo PDF.
        :param output_folder: Pasta onde as imagens serão salvas.
        :param image_format: Formato das imagens a serem salvas (padrão: "png").
        :param dpi: Resolução da imagem em DPI (padrão: 300).
        """

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"O PDF '{pdf_path}' não foi encontrado.")

        # Cria a pasta de saída se não existir
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Abre o arquivo PDF
        document = fitz.open(pdf_path)

        # Extrai o nome base do PDF (sem extensão)
        base_name = os.path.basename(pdf_path).rsplit(".", 1)[0]

        # Diretório onde ficarão as imagens das páginas
        folder_pages = os.path.join(output_folder, base_name)

        if os.path.exists(folder_pages):
            self.remove_folder(folder_pages)

        os.makedirs(folder_pages, exist_ok=True)

        # Calcula o fator de escala baseado no DPI
        zoom_x = dpi / 72.0
        zoom_y = dpi / 72.0
        matrix = fitz.Matrix(zoom_x, zoom_y)

        # Itera sobre cada página do PDF
        for page_number in range(len(document)):
            page = document.load_page(page_number)
            pix = page.get_pixmap(matrix=matrix)

            # Cria o caminho completo para a imagem
            image_path = os.path.join(
                folder_pages, f"{base_name}_{page_number + 1}.{image_format}"
            )

            # Salva a imagem no formato especificado
            pix.save(image_path)

            logging.info(f"Página {page_number + 1} salva como {image_path}")

        return folder_pages

    def remove_folder(self, folder_path):
        """
        Remove uma pasta junto com todos os seus arquivos e subpastas.

        :param folder_path: Caminho para a pasta a ser removida.
        """
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            logging.info(f"A pasta '{folder_path}' foi removida com sucesso.")
        else:
            logging.info(f"A pasta '{folder_path}' não existe ou não é um diretório.")


# Exemplo de uso da classe TesseractOCR
if __name__ == "__main__":
    # Inicialize a classe com o caminho do executável do Tesseract, se necessário.
    ocr = TesseractOCR(tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe")

    # Defina o idioma, se necessário.
    ocr.set_language("eng")

    # Caminho para a imagem.
    image_path = "path/to/your/image.png"
    pdf_path = "path/to/your/document.pdf"

    # Leia o texto da imagem.
    try:
        text = ocr.read_text_from_image(image_path)
        logging.info(f"Texto extraído da imagem: {text}")

        text_pdf = ocr.read_text_from_pdf(pdf_path)
        logging.info(f"Texto extraído do PDF: {text_pdf}")
    except FileNotFoundError as e:
        logging.info(e)
