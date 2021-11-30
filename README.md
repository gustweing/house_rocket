# House Rocket Data Analysis

# 1.0 - Business Problem
1.1 - Descrição:

House Rocket é uma companhia fictícia interessada em análises para venda e compra de imóveis.
O modelo de negócios da empresa ocorre com a compra de casas e a venda delas por preços maiores. A diferença entre o preço de venda e o preço de compra é o lucro obtido pela empresa.
O principal objetivo desse projeto é ter insights de negócio baseados em análise de dados para ajudar nas decisões do CEO e encontrar as melhores oportunidades de negócios. Com base nas análises, serão definidas as casas que estão com valores abaixo de mercado em boas condições de compra e as casas que possuem uma possibilidade de compra/reforma para uma maior valorização. 


1.2 - Data Overview:

Foi utilizado um dataset público do Kaggle. O dataset possui 21613 linhas e originalmente 21 features. Posteriormente será adicionado novas features para uma análise dos dados. 
Abaixo está a descrição das features.

| Attribute | Description |
| :----- | :----- |
| id | Unique ID for each home sold |
| date | Date of the home sale |
| price | Price of each home sold |
| bedrooms | Number of bedrooms |
| bathrooms | Number of bathrooms, where .5 accounts for a room with a toilet but no shower |
| sqft_living | Square footage of the home interior living space |
| sqft_lot | Square footage of the land space |
| floors | Number of floors |
| waterfront | A dummy variable for whether the home was overlooking the waterfront or not |
| view | An index from 0 to 4 of how good the view of the property was |
| condition | An index from 1 to 5 on the condition of the home |
| grade | An index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 have a high quality level of construction and design |
| sqft_above | The square footage of the interior housing space that is above ground level |
| sqft_basement | The square footage of the interior housing space that is below ground level |
| yr_built | The year the home was initially built |
| yr_renovated | The year of the home’s last renovation |
| zipcode | What zip code area the home is in |
| lat | Latitude |
| long | Longitude |
| sqft_living15 | The square footage of interior housing living space for the nearest 15 neighbors |
| sqft_lot15 | The square footage of the land lots of the nearest 15 neighbors |

[Dataset](https://www.kaggle.com/harlfoxem/housesalesprediction)  

A resolução de todas informações abaixo podem ser encontradas no notebook do projeto.

[NOTEBOOK](https://github.com/gustweing/house_rocket/blob/main/notebook%20house_rocket.ipynb)

# 2.0 - Business Assumptions
Foi considerado que todas as casas do dataset estão disponíveis para compra e venda. 

As estações do ano foram consideradas como um fator para as alterações de preços.

As casas necessitam ter no mínimo condição 3 ('regular') para serem adicionadas ao dataset para comprar.

Para esse dataset não será considerado a verificação e retirada de Outliers.

# 3.0 - Solution Strategy
As seguintes ações foram usadas para as análises:

* Passo 01 - Análise Descritiva

Foi utilizada para analisar as colunas e seus valores estatísticos. 

* Passo 02 - Geocode

Utilizamos uma API para buscar dados baseados na Latitude e Longitude de cada imóvel. Com isso retiramos os seguintes dados:
'Road', 'House_number', 'neighbourhood', 'city', 'county', 'state', 'place_id', 'osm_type', 'country', 'country_code'.
Nesse passo, buscando uma melhor otimização utilizamos um processo de Multi-Thread para a captura dos dados do API.

* Passo 03 - Visualização dos dados

Foi criado gráficos e mapas para melhor entendimento dos dados.
Os mapas criados foram de Densidade de Portfólio e Densidade de Preços.
Os gráficos criados foram de Preço por ano de construção, preço por dia, distribuição de preços, casas por quartos, casas por banheiros, casas por andares e casas com vista para a água.
        
* Passo 04 - Deploy em núvem

Foi realizado um deploy em uma aplicação em núvem, de modo que o CEO consiga realizar as próprias análises dos dados. 
O aplicativo conta com a análise descritiva dos dados e análises por 'zipcode', além de contar com os gráficos e mapas a disposição. 
O deploy ocorreu pelo Heroku e o framework utilizado foi o streamlit. 

[Código para deploy](https://github.com/gustweing/house_rocket/blob/main/house_rocket_app_final.py)

[House Rocket App](https://analytics-house-rocket-gw.herokuapp.com) - O aplicativo pode demorar para carregar devido ao grande número de requisições para rodar o mapa. 

* Passo 05 - Análises buscando Insights

Aqui foi analizado o Dataset buscando insights para o time de negócios. 

* Passo 06 - Recomendação de negócios

Com a análise dos dados, foi criado um arquivo de recomendação de negócios para a compra.
As recomendações foram feitas utilizando a mediana por 'zipcode' de cada um dos locais. 
Um dos fatores importantes para ser considerado ou não uma recomendação de negócio é condição ser igual ou superior a 3 ('regular'). 

[Recomendações de Negócio](https://github.com/gustweing/house_rocket/blob/main/datasets/recomendacoes_compras.csv)

* Passo 07 - Recomendação de vendas

Com a análise dos dados, foi criado um arquivo de recomendação das melhores épocas para vender o imóvel e o melhor preço sugerido.
As recomendações foram feitas utilizando a mediana por 'zipcode' e por estação de cada imóvel.

[Recomendação de venda](https://github.com/gustweing/house_rocket/blob/main/datasets/recomendacoes_venda.csv)


# 4.0 - Top 5 Data Insights
Os insights acionáveis que vieram através da exploração dos dados:

* Imóveis que possuem vista para a água são 30% mais caros na média.  - 
VERDADEIRO: As casas que possuem "waterfront" são aproximadamente 213% acima da média comparada com as casas sem "waterfront"

* Imóveis com data de construção menores que 1955 são 50% mais baratos na média. - 
FALSO: As casas com menor ano de construção são apenas 0.78% mais baratas

* Imóveis sem porão possuem área total 40% maiores do que imóveis sem porão. - 
FALSO: As casas sem porão possuem em média área de 18.41% maiores

* O crescimento dos imóveis YoY (year over year) é de 10%. - 
FALSO: O crescimento dos imóveis YoY é de 0.52%.

# 5.0 - Business Results
O cálculo do melhor preços de venda dos imóveis deu-se com as seguintes situações:

I - Se o preço de compra for maior que a mediana da região naquela sazonalidade, então o valor de venda será: O valor de compra + adicional de 10%.

II - Se o preço de compra for menor que a mediana da região naquela sazonalidade, então o valor de venda será: O valor de compra + adicional de 30$.

Na tabela abaixo, é possível fazer uma comparação dos resultados obtidos e do lucro esperado. 

| Situação de Venda | N° de casas | Valor total (US$) | Valor de revenda (US$) | Lucro (US$) |
| :-----: | :-----: | :-----: | :-----: | :-----: |
| 1 | 10.678 | 7.427.092.990,00 | 8.169.802.289,00 | 742.709.299,00 |
| 2 | 10.935 | 4.245.832.018,00 | 5.519.581.623,40 | 1.273.749.605,40 |
| Grand Total | 21.613 | 11.672.925.008,00 | 13.689.383.912,40 | 2.016.458.904,40 |


# 6.0 - Conclusions
O objetivo de análisar os valores com base nas regiões foi concluído.
É possível notar que seguindo o modelo há uma obtenção de lucro de maneira calculada e objetiva. 

# 7.0 - Next steps
Para as próximas etapas, é crucial que alguns pontos sejam alterados e adicionados.

I - Deve-se fazer uma limpeza dos dados, retirando possíveis outliers que influenciem nas análises finais.

II - Deve-se preparar os códigos para que sejam manipulados por modelos de ML, modelos esses que podem fazer uma melhor predição do melhor preço de venda e da melhor época do ano para vender esses imóveis. 

Utilizando essas duas alterações, é possível ter uma acertividade muito maior e segura do negócio.

# 8.0 - Technologies
As seguintes tecnologias foram utilizadas ao longo do processo.

![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)

![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)

![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
