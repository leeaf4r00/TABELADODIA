# OFERTA DO DIA - Automação

Sistema de automação para geração de OFERTA-DO-DIA.PDF a partir do PDF gerado pelo sistema ERGON.

## 📋 Descrição

Automatiza o processo de:
1. Leitura do PDF do ERGON (formato DDMMYYYY.PDF)
2. Filtragem de produtos com estoque > 5 caixas
3. Geração do documento OFERTA-DO-DIA.docx **com data de validade do dia**
4. Conversão automática para PDF
5. **Abertura automática** do PDF gerado

## 🚀 Instalação

### Pré-requisitos
- Python 3.11 ou superior

### Instalar dependências

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Interface Gráfica (Recomendado)

```bash
python app.py
```

### Linha de Comando

```bash
# Extrair produtos do PDF do dia
python modules/extrator.py

# Gerar OFERTA-DO-DIA completo
python modules/gerador.py
```

## 📁 Estrutura do Projeto

```
TABELADODIA/
│
├── app.py                      # 🖥️ Interface Gráfica Principal
├── requirements.txt            # 📦 Dependências do Projeto
├── README.md                   # 📖 Documentação
│
├── modules/                    # 📂 Módulos (Arquitetura Modular)
│   ├── extrator.py            # Extração de dados do PDF
│   ├── gerador.py             # Geração do DOCX
│   └── conversor.py           # Conversão DOCX → PDF
│
├── scripts/                    # 🛠️ Scripts de Desenvolvimento/Teste
│   ├── extrair_produtos.py    # Script standalone de extração
│   ├── ler_pdf_ergon.py       # Análise do PDF do ERGON
│   └── teste_completo.py      # Teste completo do sistema
│
├── output/                     # 📄 Arquivos Gerados
│   ├── produtos_filtrados.txt # Lista de produtos extraídos
│   ├── OFERTA-DO-DIA.docx    # Documento Word gerado
│   └── OFERTA-DO-DIA.pdf     # PDF final
│
├── OFERTA-DO-DIA.docx         # 📝 Template do usuário
└── [DDMMYYYY].PDF              # PDF do ERGON (automático)
```


## ⚙️ Configuração

O sistema detecta automaticamente o PDF do dia atual no formato `DDMMYYYY.PDF`.

## 🔧 Desenvolvimento

### Módulos

- **extrator.py**: Responsável pela leitura e filtragem do PDF do ERGON
- **gerador.py**: Gera o documento DOCX com os produtos filtrados
- **conversor.py**: Converte o DOCX final para PDF
- **app.py**: Interface gráfica do sistema

## 📝 Licença

Uso interno - TARUMA Comercial
