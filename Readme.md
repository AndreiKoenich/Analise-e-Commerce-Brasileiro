Este projeto foi desenvolvido na disciplina de Projeto de Bancos de Dados. O objetivo deste projeto é a construção de uma interface
gráfica que permita, por meio da utilização de Python e Streamlit, observar informações relacionadas com o e-commerce brasileiro, utilizando
PostgreSQL para armazenar e recuperar os dados referentes a uma base de dados (obtida no Kaggle) que revela informações de compras
realizadas entre os anos de 2016 e 2018.

Link da base de dados no Kaggle:

```
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data
```

Todos os imports utilizados:

```
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
```

Consultas implementadas:

```
CONSULTAS SOBRE PEDIDOS:

Consulta 4: estado com maior poder aquisitivo por ano/mês (maior valor de compra por número de pedidos).
Consulta 5: meses do ano com maior volume de compras.
Consulta 8: total de pedidos realizados por cidade.
Consulta 9: total de pedidos realizados por estado.
Consulta 12: número de pedidos por faixa de preço (baixo, médio, alto).
Consulta 14: vendas totais por tipo de pagamento (cartão de crédito, boleto, etc.).
Consulta 17: vendas totais por estado.
Consulta 20: número de pedidos por tipo de pagamento.
Consulta 25: número de pedidos por status (pendente, aprovado, cancelado, etc.).
Consulta 26: vendas totais por cada valor de frete.
Consulta 29: top 10 cidades com maiores valores em vendas.
Consulta 32: comparação entre número de pedidos aprovados e pedidos cancelados por cidade.
Consulta 36: número de pedidos entregues dentro do prazo, para uma cidade específica.
Consulta 42: número de pedidos por intervalo de datas (diário, semanal, mensal).
Consulta 46: total de vendas por tipo de produto (eletrônicos, roupas, etc.).

CONSULTAS SOBRE CLIENTES:

Consulta 6: valor médio de compras efetuadas por clientes de todas as cidades.
Consulta 7: valor médio das compras realizadas por estado.
Consulta 18: total de produtos comprados por cliente.
Consulta 37: top 10 clientes com maior volume de compras.
Consulta 47: média de avaliações dos clientes por cidade.
Consulta 51: média de avaliações dos clientes por estado.
Consulta 53: número de clientes por cidade.
Consulta 56: top 10 cidades com maior quantidade de clientes.
Consulta 57: número total de clientes em cada estado.

CONSULTAS SOBRE VENDEDORES:

Consulta 16: valor total em vendas por vendedor.
Consulta 21: média de avaliação dos vendedores por estado.
Consulta 31: número de itens vendidos por vendedor.
Consulta 52: quantidade total de vendedores por estado.
Consulta 58: quantidade total de vendedores por cidade.
Consulta 59: top 10 cidades com maior quantidade de vendedores.
Consulta 60: quantidade de vendedores por categoria de produto.

CONSULTAS SOBRE PRODUTOS:

Consulta 1: top 10 categorias de produtos melhor avaliadas.
Consulta 3: categorias mais compradas em um ano/mês.
Consulta 10: total de vendas por categoria de produto.
Consulta 11: média de avaliação dos produtos por categoria.
Consulta 54: top 10 categorias com maior valor gasto com frete.
Consulta 55: valor total gasto com frete, para cada categoria de produto.
Consulta 61: top 10 categorias mais adquiridas em um determinado estado.
Consulta 62: quantidade de vezes que produtos de uma categoria foram adquiridos em cada estado.
Consulta 63: as dez categorias mais adquiridas.

CONSULTAS NÃO UTILIZADAS:

Consulta 2: produtos mais bem avaliados em uma região (all-time).
Consulta 13: número de produtos vendidos por cidade.
Consulta 15: número de pedidos entregues com atraso (data de entrega estimada vs. data real) em um determinado ano.
Consulta 19: média de parcelas dos pagamentos.
Consulta 22: produtos mais comprados por faixa de preço.
Consulta 23: total de vendas por estado e cidade.
Consulta 24: média de tempo de entrega por estado.
Consulta 27: produtos com mais comentários e avaliações.
Consulta 28: número de produtos vendidos por vendedor e estado.
Consulta 30: vendas por categoria de produto, ordenadas por maior faturamento.
Consulta 33: top 10 produtos mais vendidos em termos de unidades.
Consulta 34: produtos com maior valor de frete.
Consulta 35: média de preço dos produtos por categoria.
Consulta 38: média de tempo de entrega por cidade.
Consulta 39: média de avaliação por produto e categoria.
Consulta 40: total de vendas por tipo de pagamento (dividido por cidade).
Consulta 41: comparação entre vendas de produtos físicos e digitais.
Consulta 43: vendas totais por período do ano (por exemplo, verão, inverno, datas promocionais).
Consulta 44: top 5 categorias de produto mais compradas no último mês.
Consulta 45: número de pedidos por estado e cidade, dividido por status do pedido.
Consulta 48: total de vendas por categoria de produto e vendedor.
Consulta 49: número de pedidos por status de pagamento.
Consulta 50: categorias mais vendidas em um intervalo de datas.
```
