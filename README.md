# 📊 Preditor de Fluxo de Caixa para Restaurantes

Um motor de previsão financeira desenvolvido em Python para prever o fluxo de caixa diário de um restaurante sob o regime de Lucro Real. O sistema automatiza a conversão de vendas brutas em liquidez real no banco, aplicando regras complexas de adquirentes (maquininhas) e feriados/finais de semana.

## 🎯 O Problema que este projeto resolve
A gestão de tesouraria de um restaurante lida com um alto volume de transações fracionadas em diferentes meios de pagamento (Crédito, Débito, Pix e Vouchers de Benefícios como Sodexo, VR, Ticket). Cada meio possui prazos de liquidação (D+0, D+1, D+15, D+30) e taxas distintas. 

O descasamento entre a entrada física do dinheiro e o pagamento de despesas pesadas (como impostos sobre folha de pagamento) pode quebrar a operação. Este projeto automatiza a previsão, mostrando exatamente **quanto** e **quando** o dinheiro vai cair na conta.

## 🚀 Funcionalidades
* **Motor de Regras Customizável:** Aplica automaticamente taxas de desconto e desloca recebimentos que cairiam no fim de semana para o próximo dia útil.
* **Dupla Entrada de Dados:**
  * **Lançamento Manual Rápido:** Para simulações e projeções instantâneas durante a operação.
  * **Upload de Relatórios (CSV/Excel):** Processamento em lote para fechamentos semanais ou mensais.
* **Dashboard Interativo:** Visualização em gráficos de barra e tabelas dinâmicas do cronograma exato de entradas bancárias.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **Pandas:** Para manipulação de dataframes, cálculos de datas e agrupamentos matemáticos.
* **Streamlit:** Para a construção da interface web e renderização dos gráficos interativos.
* **OpenPyXL:** Para leitura e processamento de planilhas Excel nativas.

## ⚙️ Como executar o projeto localmente

1. Clone este repositório para a sua máquina:
```bash
git clone [https://github.com/SEU_USUARIO/fluxo_caixa_restaurante.git](https://github.com/SEU_USUARIO/fluxo_caixa_restaurante.git)
