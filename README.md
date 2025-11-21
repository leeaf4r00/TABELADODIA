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
├── app.py                      # Interface gráfica principal
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
│
├── modules/                    # Módulos do sistema
│   ├── extrator.py            # Extração de dados do PDF
│   ├── gerador.py             # Geração do DOCX
│   └── conversor.py           # Conversão DOCX → PDF
│
├── templates/                  # Templates
│   └── OFERTA-DO-DIA.docx     # Template base
│
└── output/                     # Arquivos gerados
    ├── produtos_filtrados.txt
    ├── OFERTA-DO-DIA.docx
    └── OFERTA-DO-DIA.pdf
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
