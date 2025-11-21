"""
Módulo Gerador - Gera documento OFERTA-DO-DIA.docx
"""
from docx import Document
from pathlib import Path
from datetime import datetime

class GeradorOferta:
    """Classe para gerar documento OFERTA-DO-DIA"""
    
    def __init__(self, produtos):
        self.produtos = produtos
    
    def gerar_docx(self, template_path="OFERTA-DO-DIA.docx", output_path="output/OFERTA-DO-DIA.docx"):
        """
        Gera documento DOCX com produtos filtrados
        
        Args:
            template_path (str): Caminho do template DOCX
            output_path (str): Caminho de saída do DOCX gerado
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            # Criar novo documento ou usar template existente
            if Path(template_path).exists():
                doc = Document(template_path)
                print(f"[OK] Template carregado: {template_path}")
                
                # Adicionar data de validade no início do documento
                self._adicionar_data_validade(doc)
            else:
                doc = Document()
                self._criar_template_basico(doc)
                print("[INFO] Criando documento novo (template nao encontrado)")
            
            # Adicionar produtos
            self._adicionar_produtos(doc)
            
            # Garantir que diretório existe
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Salvar documento
            doc.save(output_path)
            print(f"[OK] DOCX gerado: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"[ERRO] Erro ao gerar DOCX: {e}")
            return None
    
    def _adicionar_data_validade(self, doc):
        """Adiciona data de validade no início do documento existente"""
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        
        # Inserir no início do documento
        # Adiciona um parágrafo no início
        p_validade = doc.paragraphs[0].insert_paragraph_before(f"Válido para: {data_hoje}")
        p_validade.alignment = 1  # Centralizado
        
        # Formatação em negrito
        for run in p_validade.runs:
            run.bold = True
            run.font.size = 140000  # 14pt em EMU (English Metric Units)

    
    def _criar_template_basico(self, doc):
        """Cria template básico se não existir"""
        # Título
        titulo = doc.add_heading('OFERTA DO DIA', 0)
        titulo.alignment = 1  # Centralizado
        
        # Data e Validade
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        p_data = doc.add_paragraph(f"Data: {data_hoje}")
        p_data.alignment = 1
        
        p_validade = doc.add_paragraph(f"Válido para: {data_hoje}")
        p_validade.alignment = 1
        
        # Formatação em negrito para validade
        for run in p_validade.runs:
            run.bold = True
        
        doc.add_paragraph("")  # Espaço
    
    def _adicionar_produtos(self, doc):
        """Adiciona tabela com produtos ao documento"""
        # Adicionar título da seção
        doc.add_heading('Produtos Disponíveis', level=1)
        
        # Criar tabela
        # Colunas: Código, Descrição, Estoque, Preço
        tabela = doc.add_table(rows=1, cols=4)
        
        # Cabeçalho
        celulas_head = tabela.rows[0].cells
        celulas_head[0].text = 'Código'
        celulas_head[1].text = 'Descrição'
        celulas_head[2].text = 'Estoque'
        celulas_head[3].text = 'Preço'
        
        # Adicionar produtos
        for produto in self.produtos:
            celulas = tabela.add_row().cells
            celulas[0].text = produto['codigo']
            celulas[1].text = produto['descricao']
            celulas[2].text = f"{produto['estoque']} {produto['unidade']}"
            celulas[3].text = f"R$ {produto['preco']:.2f}"
        
        # Adicionar total de produtos
        doc.add_paragraph("")
        doc.add_paragraph(f"Total de produtos: {len(self.produtos)}")
        
        print(f"[OK] {len(self.produtos)} produtos adicionados ao documento")

if __name__ == "__main__":
    # Teste com dados de exemplo
    produtos_exemplo = [
        {
            'codigo': '9576',
            'descricao': 'ABS S.LIVRE ADAP C/A 48X8UN L8P7',
            'estoque': 955,
            'unidade': 'CX',
            'preco': 118.00
        },
        {
            'codigo': '1755',
            'descricao': 'ACUCAR ITAMARATY 30X1KG',
            'estoque': 449,
            'unidade': 'FD',
            'preco': 98.00
        }
    ]
    
    gerador = GeradorOferta(produtos_exemplo)
    gerador.gerar_docx()
