"""
Script para extrair e filtrar produtos do PDF do ERGON
Filtra apenas produtos com estoque > 5 caixas
"""
import pdfplumber
import re
from datetime import datetime

def extrair_produtos_pdf(pdf_path):
    """
    Extrai produtos do PDF do ERGON e filtra os com estoque > 5
    
    Retorna:
        lista de dicionários com: codigo, numero, descricao, estoque, unidade, local, marca, preco
    """
    produtos_filtrados = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processando {len(pdf.pages)} paginas...\n")
            
            for num_pagina, pagina in enumerate(pdf.pages, 1):
                texto = pagina.extract_text()
                
                # Dividir em linhas
                linhas = texto.split('\n')
                
                # Processar cada linha
                for linha in linhas:
                    # Ignorar cabeçalhos e linhas de separação
                    if ('-----' in linha or 
                        'Código' in linha or 
                        'TARUMA' in linha or 
                        'Emitido' in linha or
                        'Pagina' in linha or
                        linha.strip() == ''):
                        continue
                    
                    # Tentar extrair dados da linha usando regex
                    # Padrão: Código Número Descrição Estoque Unid Local Marca Preço
                    # Exemplo: 9576 577508 ABS S.LIVRE ADAP C/A 48X8UN L8P7 955 CX SEMPRELIVRE 118,00
                    
                    # Regex para capturar os campos
                    padrao = r'^(\d+)\s+(\S+)\s+(.+?)\s+(-?\d+)\s+(CX|FD|UN)\s+(\S+)?\s+(.+?)\s+([\d,]+)$'
                    match = re.match(padrao, linha.strip())
                    
                    if match:
                        codigo = match.group(1)
                        numero = match.group(2)
                        descricao = match.group(3).strip()
                        estoque = int(match.group(4))
                        unidade = match.group(5)
                        local = match.group(6) if match.group(6) else ""
                        marca = match.group(7).strip()
                        preco_str = match.group(8)
                        preco = float(preco_str.replace(',', '.'))
                        
                        # Filtrar apenas produtos com estoque > 5
                        if estoque > 5:
                            produto = {
                                'codigo': codigo,
                                'numero': numero,
                                'descricao': descricao,
                                'estoque': estoque,
                                'unidade': unidade,
                                'local': local,
                                'marca': marca,
                                'preco': preco
                            }
                            produtos_filtrados.append(produto)
                
                print(f"[OK] Pagina {num_pagina} processada")
            
            print(f"\nTotal de produtos filtrados (estoque > 5): {len(produtos_filtrados)}")
            return produtos_filtrados
            
    except FileNotFoundError:
        print(f"[ERRO] Arquivo {pdf_path} nao encontrado!")
        return []
    except Exception as e:
        print(f"[ERRO] Erro ao processar PDF: {e}")
        return []

def salvar_produtos_texto(produtos, arquivo_saida="produtos_filtrados.txt"):
    """Salva produtos em arquivo de texto para conferência"""
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write("PRODUTOS COM ESTOQUE > 5 CAIXAS\n")
        f.write("="*80 + "\n\n")
        
        for i, p in enumerate(produtos, 1):
            f.write(f"{i}. {p['descricao']}\n")
            f.write(f"   Código: {p['codigo']} | Estoque: {p['estoque']} {p['unidade']} | Preço: R$ {p['preco']:.2f}\n")
            f.write(f"   Marca: {p['marca']}\n\n")
    
    print(f"[OK] Produtos salvos em: {arquivo_saida}")

if __name__ == "__main__":
    # Pegar PDF do dia atual
    hoje = datetime.now().strftime("%d%m%Y")
    pdf_path = f"{hoje}.PDF"
    
    print(f"Buscando arquivo: {pdf_path}\n")
    
    produtos = extrair_produtos_pdf(pdf_path)
    
    if produtos:
        salvar_produtos_texto(produtos)
        
        # Mostrar alguns exemplos
        print("\nPrimeiros 5 produtos filtrados:")
        print("="*80)
        for i, p in enumerate(produtos[:5], 1):
            print(f"{i}. {p['descricao']}")
            print(f"   Estoque: {p['estoque']} {p['unidade']} | Preço: R$ {p['preco']:.2f}")
            print()
