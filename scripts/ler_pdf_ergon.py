"""
Script para ler e analisar o PDF do ERGON
"""
import pdfplumber

pdf_path = "21112025.PDF"

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total de páginas: {len(pdf.pages)}\n")
        
        # Ler primeira página para entender estrutura
        primeira_pagina = pdf.pages[0]
        texto = primeira_pagina.extract_text()
        
        print("=" * 80)
        print("CONTEÚDO DA PRIMEIRA PÁGINA:")
        print("=" * 80)
        print(texto)
        print("\n")
        
        # Tentar extrair tabelas
        print("=" * 80)
        print("TENTANDO EXTRAIR TABELAS:")
        print("=" * 80)
        tabelas = primeira_pagina.extract_tables()
        if tabelas:
            for i, tabela in enumerate(tabelas):
                print(f"\nTabela {i+1}:")
                for linha in tabela[:5]:  # Mostrar primeiras 5 linhas
                    print(linha)
        else:
            print("Nenhuma tabela detectada automaticamente")
            
except FileNotFoundError:
    print(f"Arquivo {pdf_path} não encontrado!")
except ImportError:
    print("Biblioteca pdfplumber não instalada. Execute: pip install pdfplumber")
