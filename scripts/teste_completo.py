"""
Script de teste completo - Workflow completo do sistema
Testa: Extração → Geração com data de validade → Conversão → Abertura
"""
import sys
from pathlib import Path
from datetime import datetime

# Adicionar módulos ao path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from extrator import ExtratorPDF
from gerador import GeradorOferta
from conversor import ConversorPDF

def teste_completo():
    """Executa teste completo do sistema"""
    print("="*80)
    print("TESTE COMPLETO DO SISTEMA OFERTA DO DIA")
    print("="*80)
    print(f"Data do teste: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    # Passo 1: Extração
    print("[1/3] Extraindo produtos do PDF...")
    hoje = datetime.now().strftime("%d%m%Y")
    pdf_path = f"{hoje}.PDF"
    
    extrator = ExtratorPDF(pdf_path)
    produtos = extrator.extrair_produtos(estoque_minimo=5)
    
    if not produtos:
        print("[ERRO] Nenhum produto encontrado!")
        return False
    
    print(f"[OK] {len(produtos)} produtos extraidos\n")
    
    # Passo 2: Geração DOCX com data de validade
    print("[2/3] Gerando DOCX com data de validade...")
    gerador = GeradorOferta(produtos)
    docx_path = gerador.gerar_docx()
    
    if not docx_path:
        print("[ERRO] Falha ao gerar DOCX!")
        return False
    
    print(f"[OK] DOCX gerado: {docx_path}\n")
    
    # Passo 3: Conversão para PDF
    print("[3/3] Convertendo para PDF...")
    conversor = ConversorPDF()
    pdf_path_final = conversor.converter(docx_path)
    
    if not pdf_path_final:
        print("[ERRO] Falha ao converter para PDF!")
        return False
    
    print(f"[OK] PDF gerado: {pdf_path_final}\n")
    
    # Resumo final
    print("="*80)
    print("TESTE CONCLUIDO COM SUCESSO!")
    print("="*80)
    print(f"\nArquivos gerados:")
    print(f"  - {docx_path}")
    print(f"  - {pdf_path_final}")
    print(f"\nProdutos incluidos: {len(produtos)}")
    print(f"Data de validade: {datetime.now().strftime('%d/%m/%Y')}")
    
    return True

if __name__ == "__main__":
    sucesso = teste_completo()
    sys.exit(0 if sucesso else 1)
