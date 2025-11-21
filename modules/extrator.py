"""
Módulo Extrator - Extrai dados do PDF do ERGON
Filtra produtos com estoque > 5 caixas
"""
import pdfplumber
import re
from pathlib import Path

class ExtratorPDF:
    """Classe para extrair e filtrar produtos do PDF do ERGON"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.produtos = []
    
    def extrair_produtos(self, estoque_minimo=5):
        """
        Extrai produtos do PDF e filtra por estoque mínimo
        
        Args:
            estoque_minimo (int): Estoque mínimo para filtrar (padrão: 5)
            
        Returns:
            list: Lista de dicionários com dados dos produtos
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                print(f"Processando {len(pdf.pages)} paginas...")
                
                for num_pagina, pagina in enumerate(pdf.pages, 1):
                    texto = pagina.extract_text()
                    self._processar_pagina(texto, estoque_minimo)
                    print(f"[OK] Pagina {num_pagina} processada")
                
                print(f"\nTotal de produtos filtrados (estoque > {estoque_minimo}): {len(self.produtos)}")
                return self.produtos
                
        except FileNotFoundError:
            print(f"[ERRO] Arquivo {self.pdf_path} nao encontrado!")
            return []
        except Exception as e:
            print(f"[ERRO] Erro ao processar PDF: {e}")
            return []
    
    def _processar_pagina(self, texto, estoque_minimo):
        """Processa uma página do PDF e extrai produtos"""
        linhas = texto.split('\n')
        
        for linha in linhas:
            # Ignorar cabeçalhos e linhas de separação
            if self._ignorar_linha(linha):
                continue
            
            produto = self._extrair_produto(linha)
            if produto and produto['estoque'] > estoque_minimo:
                self.produtos.append(produto)
    
    def _ignorar_linha(self, linha):
        """Verifica se a linha deve ser ignorada"""
        return ('-----' in linha or 
                'Código' in linha or 
                'TARUMA' in linha or 
                'Emitido' in linha or
                'Pagina' in linha or
                linha.strip() == '')
    
    def _extrair_produto(self, linha):
        """Extrai dados do produto de uma linha usando regex"""
        # Padrão: Código Número Descrição Estoque Unid Local Marca Preço
        padrao = r'^(\d+)\s+(\S+)\s+(.+?)\s+(-?\d+)\s+(CX|FD|UN)\s+(\S+)?\s+(.+?)\s+([\d,]+)$'
        match = re.match(padrao, linha.strip())
        
        if match:
            try:
                return {
                    'codigo': match.group(1),
                    'numero': match.group(2),
                    'descricao': match.group(3).strip(),
                    'estoque': int(match.group(4)),
                    'unidade': match.group(5),
                    'local': match.group(6) if match.group(6) else "",
                    'marca': match.group(7).strip(),
                    'preco': float(match.group(8).replace(',', '.'))
                }
            except (ValueError, IndexError):
                return None
        return None
    
    def salvar_resumo(self, caminho_saida="output/produtos_filtrados.txt"):
        """Salva resumo dos produtos filtrados em arquivo de texto"""
        Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write("PRODUTOS COM ESTOQUE > 5 CAIXAS\n")
            f.write("="*80 + "\n\n")
            
            for i, p in enumerate(self.produtos, 1):
                f.write(f"{i}. {p['descricao']}\n")
                f.write(f"   Codigo: {p['codigo']} | Estoque: {p['estoque']} {p['unidade']} | Preco: R$ {p['preco']:.2f}\n")
                f.write(f"   Marca: {p['marca']}\n\n")
        
        print(f"[OK] Produtos salvos em: {caminho_saida}")
        return caminho_saida

if __name__ == "__main__":
    from datetime import datetime
    
    # Pegar PDF do dia atual
    hoje = datetime.now().strftime("%d%m%Y")
    pdf_path = f"{hoje}.PDF"
    
    print(f"Buscando arquivo: {pdf_path}\n")
    
    extrator = ExtratorPDF(pdf_path)
    produtos = extrator.extrair_produtos(estoque_minimo=5)
    
    if produtos:
        extrator.salvar_resumo()
        
        # Mostrar alguns exemplos
        print("\nPrimeiros 5 produtos filtrados:")
        print("="*80)
        for i, p in enumerate(produtos[:5], 1):
            print(f"{i}. {p['descricao']}")
            print(f"   Estoque: {p['estoque']} {p['unidade']} | Preco: R$ {p['preco']:.2f}\n")
