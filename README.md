# FUNDO DE INVESTIMENTO CVM - ENGENHERIA E ANALISE DE DADOS
- O Portal Brasileiro de Dados Abertos é a ferramenta disponibilizada pelo governo para que todos possam encontrar e utilizar os dados e as informações públicas, prezando pela simplicidade e organização, a fim de disponibilizar, facilmente, os dados e informações que o usuário necessita. Ele foi idealizado no contexto da Lei de Acesso à Informação (LAI), funcionando como um grande catálogo que facilita a busca e uso de dados publicados pelos órgãos do governo. Isso proporciona ao cidadão um melhor entendimento do governo, no acesso aos serviços públicos, no controle das contas públicas e na participação no planejamento e desenvolvimento das políticas públicas.
Fonte: Portal Dados Abertos CVM (Aba 'Sobre')

- OBS.: ESSE PROJETO NÃO É UMA RECOMENDAÇÃO DE INVESTIMENTO, MAS UMA INICIATIVA DE FORNECER ALGUMAS INFORMAÇÕES, DADOS ÚTEIS - E PÚBLICOS - AOS INVESTIDORES/INTERESSADOS E INSIGHTS.

---------------------------------------------------------------------------------------------
# PROJETO
- Levando em conta a riqueza de dados que a Comissão de Valores Mobiliários (CVM) nos concede (como: Valor total da carteira do fundo, Patrimônio líquido, Valor da cota, Captações realizadas no dia, Resgates pagos no dia, Número de cotistas - informações públicas) com foco prioritário em Fundos de Investimentos, fiz a extração desses dados disponíveis e listados pela autarquia. A partir desses dados - coletados e organizados, os investidores, de diferentes perfis e objetivos financeiros, poderão usá-los como auxiliadores em tomadas de decisões, escolhendo o fundo que lhe atender melhor. Além disso, para melhores resultados e decisões mais acertivas: 
- listarei os melhores fundos de investimentos (podendo escolher a quantidade para o range) usando, como referência, os maiores patrimônios líquidos;
- graficamente, demonstarei a evolução do patrimônio líquido desses melhores fundos, separados e particionados através da data;
- informarei como esses melhores fundos são distribuídos, isto é, quais tipos de fundos mais aparecem nesse ranking;
- seguindo esse terceiro passo, demonstrarei, usando todos os fundos listados, como eles estão tipificados, só que agora de maneira geral.
Para conclusão desse projeto - abordando obtenção dos dados, tratamento, armazenamento deles e geração de gráficos -, foram necessárias algumas etapas, sendo elas:

---------------------------------------------------------------------------------------------
# ETAPAS

# 1) Configuração de Acessos
- Visando uma melhor organização das informações de configurações, inseri as informações necessárias, e de acessos, em um arquivo json, de nome 'data' - localizado dentro da pasta utils -, nesse arquivo há informações pertinentes a fonte extraída, o tipo do arquivo a ser gerado, parâmetros, credenciais da conta cloud AWS - usuário IAM, links necessários, informações essas pré-selecionadas pelo usuário;

# 2) Criei um processo ETL:
- E: Extração dos dados respectivos oriundos das fontes "https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/" e 'https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv' e já inseridos no S3 Bucket, da AWS, visando garantir integridade dos dados;

- T: No primeiro link são os dados de valor dos fundos, já no segundo link, são os dados considerados cadastrais. Dessa forma, mesclei ambos usando a coluna 'CNPJ_FUNDO' como referência e obtive a DENOM_SOCIAL dos fundos. Posterior esse processo, fiz os tratamentos necessários para deixar os dados limpos e, por consequência, tê-los de maneira apropriada para obtenção/geração de gráficos/insights.

- L: Logo após os tratamentos, e tendo um dataframe preparado, carreguei os dados em um arquivo csv - nomeado com a estrutura padrão: 'Fundo_Investimento_[%Y%m%d]', para o histórico geral, e 'Fundo_Investimento_[XX]_[%Y%m%d]' - sendo XX o número relacionado ao toprange, isto é, quantidade dos melhores fundos desejados, para o histórico dos 'toprange'. um arquivo já tratado, limpo e em conformidade, disponível para ser utilizado como ferramenta para obtenção de insights.

# 3) Desenvolvimento e Análise de Gráficos:
- Agora, inserindo um pouco sobre a função do Analista, farei algumas análises quanto aos dados coletados da CVM, levantando hipóteses e cenários.

# A) Análise dos 'toprange' (inserido no data.json) fundos com maiores Patrimônios Líquidos
- Para ponto de partida, classifiquei e listei os melhores fundos usando como métrica referencial o Patrimônio Líquido, isto é, considerando os maiores Patrimônios como 'melhores' fundos, para a partir desses dados usar nas outras projeções.

# B) Análise da Evolução do Valor Patrimonial Líquido dos 'toprange' ao Longo do Tempo
- Tendo ciência de que usar somente uma variável para ordenação seja perigoso, plotei, usando como base esses melhores fundos, um gráfico relacionado a evolução patrimonial líquida desses fundos, tendo como faixa/divisão/separação as datas referenciais disponibilizadas pelos próprios fundos. Com isso, sanarei o possível 'imbróglio' do tópico A - ou que poderia surgir, que é: será que aquele dado do patrimônio líquido é ilusório? Foi uma movimentação 'anormal', isto é, o valor foi inserido dia x, e no dia posterior retirado do fundo, trazendo uma falsa percepção?

# C) Análise da Distribuição dos Tipos de Fundos ocupados no 'toprange'
- Sabendo que existe tipos de fundos, e querendo entender quais são os predominantes, sinalizei os tipos de fundos encontradas nessa ordenação e sua respectiva quantidade, para estudo de motivação e causa.

# D) Análise da Distribuição Geral dos Tipos de Fundos (TP_FUNDO)
- Ainda nesse segmento de tipos de fundos, usarei o histórico dos dados para levantar os tipos e quantidade de fundos listados. Esse levantamento é justamente para entender quais são os que não aparecem nos melhores ordenados, e possíveis causas para tal.

# 4)

# 5)

# 6)

---------------------------------------------------------------------------------------------
# OBSERVAÇÕES:
- Conforme mencionado, há arquivos ausentes nesse repositório - exemplo do data.json, justamente para manter integridade dos dados pessoais. Dessa forma, para obtenção do resultado esperado, criei um arquivo base (de nome data_exemplo.json, dentro da pasta utils), para vocês terem uma noção da estrutura que foi necessária para obtenção do resultado esperado.

- Passo 2 foi realizado usando, prioritariamente e somente, Linguagem de Programação Python e suas principais bibliotecas, sendo algumas delas: pandas, requests, bs4, zipFile.

- Passo 3 foi realizado usando, prioritariamente e somente, Linguagem de Programação Python e suas principais bibliotecas - tanto para manipular os dados quanto para gerar gráficos, sendo algumas delas: pandas, matplotlib e seaborn.

- 

---------------------------------------------------------------------------------------------
# CONCLUSÃO (PESSOAL):
- Levando em conta a cultura data-driven e a minha maneira de analisar o cenário a partir dos dados encontrados - sabendo que não uma via de regra o meu ponto de vista, concluo que ...

------------------------------------------------------------------------------------------------
# REFERÊNCIAS:
- Sites que podem contribuir à realização das etapas acima, e que me ajudaram para obtenção do resultado final e esperado:

- https://acervolima.com/use-diferentes-eixos-y-a-esquerda-e-a-direita-de-um-grafico-matplotlib/
- 
- 
- 

------------------------------------------------------------------------------------------------
# CONSIDERAÇÕES FINAIS:
Obrigado pela interação. Fico à disposição e disponível para receber dicas ou sanar dúvidas/cuirosidades. Bons estudos e fica na paz!