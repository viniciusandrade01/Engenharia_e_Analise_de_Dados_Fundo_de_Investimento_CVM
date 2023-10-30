# FUNDO DE INVESTIMENTO CVM - ENGENHERIA E ANALISE DE DADOS
- O Portal Brasileiro de Dados Abertos é a ferramenta disponibilizada pelo governo para que todos possam encontrar e utilizar os dados e as informações públicas, prezando pela simplicidade e organização, a fim de disponibilizar, facilmente, os dados e informações que o usuário necessita. Ele foi idealizado no contexto da Lei de Acesso à Informação (LAI), funcionando como um grande catálogo que facilita a busca e uso de dados publicados pelos órgãos do governo. Isso proporciona ao cidadão um melhor entendimento do governo, no acesso aos serviços públicos, no controle das contas públicas e na participação no planejamento e desenvolvimento das políticas públicas.
Fonte: Portal Dados Abertos CVM (Aba 'Sobre')

- Os fundos de investimento são um tipo de aplicação financeira onde um ou mais investidores (cotistas) agrupam seus recursos para realizar aplicações em ativos mobiliários ou imobiliários - entre eles títulos da dívida pública, ações, debêntures, moedas e derivativos -. Os cotistas são os "donos de fundos", mas há outras pessoas que figuram nesse contexto para que o dinheiro seja aplicado da melhor maneira, seguindo a política do fundo, sendo elas: o gestor - considerado o técnico, ele que escolhe os ativos da carteira -, o auditor - faz auditoria das contas e documentos -, o custodiante - faz a guarda dos ativos e liquidação das operações -, o distribuidor - vende e coloca no mercado -, o administrador - responsável pela constituição do fundo, cálculo da cota, divulgação da carteira etc -, e o próprio cotista - aquele que detém as cotas do fundo -.

- Eles (fundos) são considerados um investimento coletivo, em que os recursos de vários investidores são aplicados em conjunto no mercado, e mediante a proporção dos recursos alocados, cada investidor receberá proporcionalmente ao investimento realizado. Diferente do investimento em ações, nos fundos há um grupo de pessoas apropriadas (e ressarcidas por isso) para escolha dos ativos que satisfazem a política do fundo e, por consequência, o desejo do cotista - que investirá no fundo que lhe atender.

- Vale lembrar que esses fundos possuem algumas taxas (uma das consequências de você não escolher os seus próprios ativos), taxas essas que serão utilizadas para remunerar os envolvidos na aquisição e escolha dos ativos (grupo de pessoas que listei acima), tais como: taxa de administração (que incide sobre o patrimônio mantido pelo investidor) e taxa de performance (uma remuneração baseada no resultado, considerado um bônus, e é 'acionado' quando há ganhos maiores que o previamente estabelecidos). Além dessas taxas, há algumas tributações, tais como: Imposto de Renda (que recai sobre a rentabilidade, ou seja, o valor da rentabilidade será a base para cobrança da taxa do imposto) e o Imposto sobre Operações Financeiras (conhecido, também, como IOF, ele incidirá sobre o rendimento apenas nos resgates feitos em um período inferior a 30 dias a partir da aplicação).
Fonte: https://www.infomoney.com.br/guias/fundos-de-acoes/

- OBS.: ESSE PROJETO NÃO É UMA RECOMENDAÇÃO DE INVESTIMENTO, MAS UMA INICIATIVA DE FORNECER ALGUMAS INFORMAÇÕES, DADOS ÚTEIS - E PÚBLICOS - AOS INVESTIDORES/INTERESSADOS E INSIGHTS.

---------------------------------------------------------------------------------------------
# PROJETO
- Levando em conta a riqueza de dados que a Comissão de Valores Mobiliários (CVM) nos concede (como: valor total da carteira do fundo, patrimônio líquido, valor da cota, captações realizadas no dia, resgates pagos no dia, número de cotistas - informações públicas) com foco prioritário em Fundos de Investimentos, fiz a extração desses dados disponíveis e listados pela autarquia. A partir desses dados - coletados e organizados, os investidores, de diferentes perfis e objetivos financeiros, poderão usá-los como auxiliadores em tomadas de decisões, escolhendo o fundo que lhe atender melhor. Além disso, para melhores resultados, análise de cenários, tendências e decisões mais acertivas: 
- A) listarei os melhores fundos de investimentos (podendo escolher a quantidade para o range) usando, como referência, os maiores patrimônios líquidos;
- B) graficamente, demonstarei a evolução do patrimônio líquido desses melhores fundos, separados e particionados através da data;
- C) informarei como esses melhores fundos são distribuídos, isto é, quais tipos de fundos mais aparecem nesse ranking. A partir dessas informações, estudarei os possíveis motivos;
- D) seguindo esse terceiro passo, demonstrarei, usando todos os fundos listados, como eles estão tipificados, só que agora de maneira geral.

- Para conclusão desse projeto - abordando obtenção dos dados, tratamento, armazenamento deles e geração de gráficos -, foram necessárias algumas etapas, sendo elas:

---------------------------------------------------------------------------------------------
# ETAPAS

# 1) Configuração de Acessos
- Visando uma melhor organização das informações de configurações, inseri as informações necessárias, e de acessos, em um arquivo json, de nome 'data' - localizado dentro da pasta utils -, nesse arquivo há informações pertinentes a fonte extraída, o tipo do arquivo a ser gerado, parâmetros, credenciais da conta cloud AWS - usuário IAM, links necessários, informações essas pré-selecionadas pelo usuário;

# 2) Criei um processo ETL:
- E: Extração dos dados respectivos oriundos das fontes "https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/" e 'https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv' e que serão inseridos no S3 Bucket, da AWS, visando garantir integridade dos dados;

- T: No primeiro link são os dados de valor dos fundos, já no segundo link, são os dados considerados cadastrais. Dessa forma, mesclei ambos usando a coluna 'CNPJ_FUNDO' como referência e obtive a DENOM_SOCIAL dos fundos, que é onde ficará armazenado o nome social atrelado ao cnpj. Posterior a esse processo, fiz os tratamentos necessários para deixar os dados limpos e, por consequência, tê-los de maneira apropriada para obtenção/geração de gráficos/insights.

- L: Logo após os tratamentos, e tendo um dataframe preparado, carreguei os dados em um arquivo csv - nomeado com a estrutura padrão: 'FundosInvestimentoGeral_[%Y%m].csv', para o histórico geral, e 'FundosInvestimentoTopRange_[%Y%m].csv' - sendo %Y o ano com 4 dígitos e %m, o mês em dígito, para ter em mãos um arquivo tratado, limpo e em conformidade, disponível para ser utilizado como ferramenta para obtenção de insights.

# 3) Desenvolvimento e Análise de Gráficos:
- Agora, inserindo um pouco sobre a função do Analista, farei algumas análises quanto aos dados coletados da CVM, levantando hipóteses e cenários.

# A) Análise dos 'toprange' (inserido no data.json) fundos com maiores Patrimônios Líquidos
- Para ponto de partida, classifiquei e listei os melhores fundos usando como referência o Patrimônio Líquido, isto é, considerando os maiores patrimônios como 'melhores' fundos, para a partir desses dados usar nas outras projeções.

# B) Análise da Evolução do Valor Patrimonial Líquido dos 'toprange' ao Longo do Tempo
- Plotei, usando como base esses melhores fundos, um gráfico relacionado a evolução patrimonial líquida desses fundos, tendo como faixa/divisão/separação as datas referenciais disponibilizadas pelos próprios fundos. Com isso, sanarei o possível 'imbróglio' do tópico A - ou que poderia surgir, que é: será que aquele dado informado no patrimônio líquido é ilusório? Foi uma movimentação 'anormal', isto é, o valor foi inserido dia x, e no dia posterior retirado do fundo, trazendo uma falsa percepção? Veremos no histórico.

# C) Análise da Distribuição dos Tipos de Fundos ocupados no 'toprange'
- Sabendo que existe tipos de fundos e que cada fundo é específico para determinada causa, e querendo entender quais são os predominantes, sinalizei os tipos de fundos encontradas nessa ordenação e sua respectiva quantidade, para estudo de motivação e causa.

# D) Análise da Distribuição Geral dos Tipos de Fundos (TP_FUNDO)
- Ainda nesse segmento de tipos de fundos, usarei o histórico dos dados para levantar os tipos e quantidade de fundos listados. Esse levantamento é justamente para entender quais são os que não aparecem nos melhores ordenados, e possíveis causas para tal.

---------------------------------------------------------------------------------------------
# OBSERVAÇÕES:
- Conforme mencionado, há arquivos ausentes nesse repositório - exemplo do data.json, justamente para manter integridade dos dados pessoais. Dessa forma, para obtenção do resultado esperado, criei um arquivo base (de nome data_exemplo.json, dentro da pasta utils), para vocês terem uma noção da estrutura que foi necessária para obtenção do resultado esperado.

- Passo 2 foi realizado usando, prioritariamente e somente, Linguagem de Programação Python e suas principais bibliotecas, sendo algumas delas: pandas, requests, bs4, zipFile.

- Passo 3 foi realizado usando, prioritariamente e somente, Linguagem de Programação Python e suas principais bibliotecas - tanto para manipular os dados quanto para gerar gráficos, sendo algumas delas: pandas, matplotlib e seaborn.
Além disso, das variáveis disponibilizadas para geração de insights, utilizei o Valor Patrimonial Líquido como parâmetro para decisões iniciais, justamente por mexer em uma área totalmente vital nessa categoria, o 'bolso', que significa diretamente o quão saudável o fundo está - analisando historicamente. Embora saiba que usar uma variável como referência geral seja perigoso, a análise é meramente um estudo de caso e não há motivações extras (como indicação de ativo, por exemplo).
---------------------------------------------------------------------------------------------
# CONCLUSÃO (OPINIÃO):
- Levando em conta uma cultura tendo como base os dados e a minha maneira de analisar o cenário a partir deles - sabendo que meu ponto de vista não é via de regra, concluo que se você não tem tempo para análise dos ativos, escolha e estudo deles, fundos de investimento acaba sendo uma ótima opção de investimento, mas que fique bem claro que pelo fato de você não escolher os seus próprios ativos e delegar isso a um terceiro, você pagará alguns impostos/taxas que poderiam ser evitados caso você, o cotista, escolhesse os ativos.
Além disso, analisando os dados gerais, o tipo de Fundo FI (Fundo de Investimento) aparece quase que de forma unânime por conta de alguns aspectos interessantes, sendo eles:
- 1°) Diversificação: permite investir em uma variedade de ativos - como ações, títulos públicos, títulos privados, moedas estrangeiras, commodities etc -, ou seja, oferece uma diversificação automática para o investidor, reduzindo o risco em comparação com investir diretamente em um único ativo.
- 2°) Gestão Profissional: é gerido por profissionais que possuem experiência e conhecimento para tomar decisões de investimento previamente informadas. Isso é especialmente vantajoso para investidores que não têm tempo, conhecimento ou interesse em gerenciar ativamente seus investimentos. Vale lembrar e ressaltar, que por conta dessa ajuda profissional, você precisará remunerá-los, e as taxas informadas no início desse documento possuem essa finalidade.
- 3°) Liquidez: permitindo mais facilidade, por parte do investidor, na hora de resgatar o seu dinheiro, que comparado a alguns modelos de investimento acaba sendo um impecilho e problema.
- 4°) Acessibilidade: certos FI têm valores mínimos de investimento mais acessíveis em comparação com outros veículos de investimento, como fundos exclusivos ou carteiras administradas, tornando-os adequados para investidores com capital inicial limitado.
- 5°) Economia de Escala: esses fundos, geralmente, se beneficiam de economias de escala (que a grosso modo interfere em uma redução no valor). Por terem um grande volume de ativos sob gestão, podem negociar taxas mais favoráveis, o que pode resultar em custos mais baixos para os investidores quando comparados com investir individualmente nos mesmos ativos.
- 6°) Transparência: eles são regulamentados e obrigados a fornecer informações regulares aos cotistas, garantindo transparência nas operações do fundo.
- 7°) Estratégias Personalizadas: alguns FI oferecem acesso a estratégias especializadas, como arbitragem, hedge e investimentos em startups, que podem ser difíceis de implementar para investidores individuais, seja por falta de conhecimento - que os gestores possuem - seja por falta de capital e estratégia.

------------------------------------------------------------------------------------------------
# REFERÊNCIAS:
- Sites que podem contribuir à realização das etapas acima, e que me ajudaram para obtenção do resultado final e esperado:

- https://dados.cvm.gov.br/about
- https://acervolima.com/use-diferentes-eixos-y-a-esquerda-e-a-direita-de-um-grafico-matplotlib/
- https://conteudos.xpi.com.br/aprenda-a-investir/relatorios/guia-completo-sobre-fundos-de-investimento-entenda-como-aplicar-e-o-que-fazer/
- https://investnews.com.br/guias/fundos-de-investimento/#tipos_de_fundos
- https://exame.com/invest/guia/fundos-offshore-o-que-sao-e-quais-sao-os-seus-beneficios/

------------------------------------------------------------------------------------------------
# CONSIDERAÇÕES FINAIS:
Obrigado pela interação. Fico à disposição e disponível para receber dicas ou sanar dúvidas/curiosidades. Bons estudos e fica na paz!