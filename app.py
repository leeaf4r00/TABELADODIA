"""
OFERTA DO DIA - Aplicação com Interface Gráfica
Automatiza geração de OFERTA-DO-DIA.PDF a partir do PDF do ERGON
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path
import sys
import os
import subprocess

# Adicionar diretório modules ao path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from extrator import ExtratorPDF
from gerador import GeradorOferta
from conversor import ConversorPDF

class AplicacaoOfertaDia:
    """Interface gráfica principal"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OFERTA DO DIA - Automação TARUMA")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Variáveis
        self.pdf_path = tk.StringVar()
        self.estoque_minimo = tk.IntVar(value=5)
        self.produtos = []
        self.ultimo_docx = None
        self.ultimo_pdf = None
        
        self._criar_interface()
        self._detectar_pdf_dia()
    
    def _criar_interface(self):
        """Cria elementos da interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="OFERTA DO DIA", font=('Arial', 24, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=20)
        
        subtitulo = ttk.Label(main_frame, text="Automação de Geração de PDF", font=('Arial', 12))
        subtitulo.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Seção 1: Seleção de arquivo
        ttk.Label(main_frame, text="1. Arquivo PDF do ERGON:", font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        ttk.Entry(main_frame, textvariable=self.pdf_path, width=50).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Procurar...", command=self._selecionar_pdf).grid(row=3, column=2, padx=5)
        
        # Seção 2: Configurações
        ttk.Label(main_frame, text="2. Configurações:", font=('Arial', 11, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        
        config_frame = ttk.Frame(main_frame)
        config_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        ttk.Label(config_frame, text="Estoque mínimo (caixas):").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(config_frame, from_=1, to=100, textvariable=self.estoque_minimo, width=10).grid(row=0, column=1, padx=10)
        
        # Seção 3: Ações
        ttk.Label(main_frame, text="3. Processar:", font=('Arial', 11, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        ttk.Button(btn_frame, text="▶ GERAR OFERTA DO DIA", command=self._processar_completo, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📄 Apenas Extrair Dados", command=self._apenas_extrair).pack(side=tk.LEFT, padx=5)
        
        # Seção 4: Abrir Arquivos
        ttk.Label(main_frame, text="4. Abrir Arquivos:", font=('Arial', 11, 'bold')).grid(row=7, column=0, sticky=tk.W, pady=(20, 5))
        
        open_frame = ttk.Frame(main_frame)
        open_frame.grid(row=8, column=0, columnspan=3, pady=10)
        
        ttk.Button(open_frame, text="📄 Abrir DOCX", command=self._abrir_docx).pack(side=tk.LEFT, padx=5)
        ttk.Button(open_frame, text="📕 Abrir PDF", command=self._abrir_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(open_frame, text="📂 Abrir Pasta Output", command=self._abrir_pasta).pack(side=tk.LEFT, padx=5)
        
        # Área de log
        ttk.Label(main_frame, text="Log de Execução:", font=('Arial', 11, 'bold')).grid(row=9, column=0, sticky=tk.W, pady=(20, 5))
        
        # Frame com scrollbar para log
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=15, width=90, yscrollcommand=scrollbar.set, 
                                state='disabled', bg='#f0f0f0')
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Rodapé
        rodape = ttk.Label(main_frame, text="© 2025 TARUMA Comercial - Sistema de Automação", 
                          font=('Arial', 9), foreground='gray')
        rodape.grid(row=11, column=0, columnspan=3, pady=20)
    
    def _detectar_pdf_dia(self):
        """Detecta automaticamente o PDF do dia atual"""
        hoje = datetime.now().strftime("%d%m%Y")
        pdf_hoje = f"{hoje}.PDF"
        
        if Path(pdf_hoje).exists():
            self.pdf_path.set(pdf_hoje)
            self._log(f"[OK] PDF do dia detectado automaticamente: {pdf_hoje}")
        else:
            self._log(f"[INFO] PDF do dia ({pdf_hoje}) não encontrado. Selecione manualmente.")
    
    def _selecionar_pdf(self):
        """Abre diálogo para selecionar PDF"""
        filename = filedialog.askopenfilename(
            title="Selecione o PDF do ERGON",
            filetypes=[("PDF files", "*.PDF *.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
            self._log(f"[OK] Arquivo selecionado: {filename}")
    
    def _log(self, mensagem):
        """Adiciona mensagem ao log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
    
    def _abrir_arquivo(self, caminho):
        """Abre arquivo com aplicação padrão do sistema"""
        if not caminho or not Path(caminho).exists():
            messagebox.showwarning("Aviso", f"Arquivo não encontrado:\n{caminho}")
            return
        
        try:
            os.startfile(caminho)  # Windows
            self._log(f"[OK] Abrindo arquivo: {caminho}")
        except AttributeError:
            # Linux/Mac
            try:
                subprocess.run(['xdg-open', caminho], check=True)
                self._log(f"[OK] Abrindo arquivo: {caminho}")
            except:
                subprocess.run(['open', caminho], check=True)
                self._log(f"[OK] Abrindo arquivo: {caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir arquivo:\n{e}")
            self._log(f"[ERRO] Falha ao abrir arquivo: {e}")
    
    def _abrir_docx(self):
        """Abre o DOCX gerado"""
        if self.ultimo_docx:
            self._abrir_arquivo(self.ultimo_docx)
        else:
            # Tentar abrir o padrão
            caminho_padrao = "output/OFERTA-DO-DIA.docx"
            if Path(caminho_padrao).exists():
                self._abrir_arquivo(caminho_padrao)
            else:
                messagebox.showinfo("Info", "Nenhum DOCX foi gerado ainda.\nGere a OFERTA DO DIA primeiro!")
    
    def _abrir_pdf(self):
        """Abre o PDF gerado"""
        if self.ultimo_pdf:
            self._abrir_arquivo(self.ultimo_pdf)
        else:
            # Tentar abrir o padrão
            caminho_padrao = "output/OFERTA-DO-DIA.pdf"
            if Path(caminho_padrao).exists():
                self._abrir_arquivo(caminho_padrao)
            else:
                messagebox.showinfo("Info", "Nenhum PDF foi gerado ainda.\nGere a OFERTA DO DIA primeiro!")
    
    def _abrir_pasta(self):
        """Abre a pasta output"""
        pasta_output = Path("output").absolute()
        pasta_output.mkdir(parents=True, exist_ok=True)
        self._abrir_arquivo(str(pasta_output))
    
    def _apenas_extrair(self):
        """Apenas extrai e mostra produtos filtrados"""
        if not self.pdf_path.get():
            messagebox.showerror("Erro", "Selecione um arquivo PDF primeiro!")
            return
        
        self._log("\n" + "="*80)
        self._log("INICIANDO EXTRAÇÃO DE DADOS...")
        self._log("="*80)
        
        try:
            extrator = ExtratorPDF(self.pdf_path.get())
            self.produtos = extrator.extrair_produtos(estoque_minimo=self.estoque_minimo.get())
            
            if self.produtos:
                caminho_txt = extrator.salvar_resumo()
                self._log(f"\n[OK] {len(self.produtos)} produtos extraídos com sucesso!")
                self._log(f"[OK] Resumo salvo em: {caminho_txt}")
                
                messagebox.showinfo("Sucesso", 
                    f"Extração concluída!\n\n{len(self.produtos)} produtos encontrados com estoque > {self.estoque_minimo.get()}\n\nResumo salvo em:\n{caminho_txt}")
            else:
                self._log("[AVISO] Nenhum produto encontrado com os critérios especificados")
                messagebox.showwarning("Aviso", "Nenhum produto encontrado!")
                
        except Exception as e:
            self._log(f"[ERRO] {str(e)}")
            messagebox.showerror("Erro", f"Erro ao extrair dados:\n{str(e)}")
    
    def _processar_completo(self):
        """Executa processo completo: extrair → gerar DOCX → converter PDF"""
        if not self.pdf_path.get():
            messagebox.showerror("Erro", "Selecione um arquivo PDF primeiro!")
            return
        
        self._log("\n" + "="*80)
        self._log("PROCESSAMENTO COMPLETO INICIADO")
        self._log("="*80)
        
        try:
            # Passo 1: Extrair produtos
            self._log("\n[1/3] Extraindo produtos do PDF...")
            extrator = ExtratorPDF(self.pdf_path.get())
            self.produtos = extrator.extrair_produtos(estoque_minimo=self.estoque_minimo.get())
            
            if not self.produtos:
                self._log("[ERRO] Nenhum produto encontrado!")
                messagebox.showwarning("Aviso", "Nenhum produto encontrado com os critérios especificados!")
                return
            
            self._log(f"[OK] {len(self.produtos)} produtos extraídos")
            
            # Passo 2: Gerar DOCX
            self._log("\n[2/3] Gerando documento OFERTA-DO-DIA.docx...")
            gerador = GeradorOferta(self.produtos)
            docx_path = gerador.gerar_docx()
            
            if not docx_path:
                self._log("[ERRO] Falha ao gerar DOCX!")
                return
            
            self._log(f"[OK] DOCX gerado: {docx_path}")
            
            # Passo 3: Converter para PDF
            self._log("\n[3/3] Convertendo para PDF...")
            conversor = ConversorPDF()
            pdf_path = conversor.converter(docx_path)
            
            if pdf_path:
                self._log(f"[OK] PDF gerado: {pdf_path}")
                self._log("\n" + "="*80)
                self._log("PROCESSO CONCLUÍDO COM SUCESSO!")
                self._log("="*80)
                
                # Armazenar caminhos
                self.ultimo_docx = docx_path
                self.ultimo_pdf = pdf_path
                
                # Abrir PDF automaticamente
                self._log("\n[INFO] Abrindo PDF automaticamente...")
                self._abrir_arquivo(pdf_path)
                
                messagebox.showinfo("Sucesso!", 
                    f"OFERTA DO DIA gerada com sucesso!\n\n"
                    f"Produtos incluídos: {len(self.produtos)}\n\n"
                    f"Arquivos gerados:\n"
                    f"• {docx_path}\n"
                    f"• {pdf_path}\n\n"
                    f"PDF aberto automaticamente!")
            else:
                self._log("[ERRO] Falha ao converter para PDF!")
                
        except Exception as e:
            self._log(f"\n[ERRO] {str(e)}")
            messagebox.showerror("Erro", f"Erro durante processamento:\n{str(e)}")

def main():
    """Função principal"""
    root = tk.Tk()
    app = AplicacaoOfertaDia(root)
    root.mainloop()

if __name__ == "__main__":
    main()
