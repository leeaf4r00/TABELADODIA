"""
Módulo Conversor - Converte DOCX para PDF
"""
from docx2pdf import convert
from pathlib import Path

class ConversorPDF:
    """Classe para converter DOCX para PDF"""
    
    @staticmethod
    def converter(docx_path, pdf_path=None):
        """
        Converte arquivo DOCX para PDF
        
        Args:
            docx_path (str): Caminho do arquivo DOCX
            pdf_path (str): Caminho de saída do PDF (opcional)
            
        Returns:
            str: Caminho do arquivo PDF gerado
        """
        try:
            if not Path(docx_path).exists():
                print(f"[ERRO] Arquivo DOCX nao encontrado: {docx_path}")
                return None
            
            # Se não especificar PDF, usa mesmo nome do DOCX
            if pdf_path is None:
                pdf_path = str(Path(docx_path).with_suffix('.pdf'))
            
            print(f"Convertendo {docx_path} para PDF...")
            
            # Garantir que diretório existe
            Path(pdf_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Converter
            convert(docx_path, pdf_path)
            
            print(f"[OK] PDF gerado: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"[ERRO] Erro ao converter para PDF: {e}")
            return None

if __name__ == "__main__":
    # Teste
    conversor = ConversorPDF()
    conversor.converter("output/OFERTA-DO-DIA.docx", "output/OFERTA-DO-DIA.pdf")
