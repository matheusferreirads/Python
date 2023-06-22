#Install Libs
# pip install Orange3
# pip install Numpy

#Import Libs
import Orange
import numpy as np



#IMPORT DATA
#------------------------------------------------------------------------------------------------------------------------------

#IMPORTANTE inserir um c# no ínicio do nome da coluna que será classe, caso queira desconsiderar alguma basta inserir i#
base_census_orange = Orange.data.Table('census_regras.csv')

#Antes do | temos os atributos classificadores, depois temos a classe
base_census_orange.domain



#PREPARING DATA
#-------------------------------------------------------------------------------------------------------------------------------
#Dividindo a base em duas, sendo 0.25% a base de teste e 0.75 a de treino
base_census_orange = Orange.evaluation.testing.sample(base_census_orange, n = 0.25)

base_census_orange
#0.25%
base_census_orange[0]
#0.75%
base_census_orange[1]

base_census_training = base_census_orange[1]
base_census_test = base_census_orange[0]

len(base_census_training), len(base_census_test)



#TRAINING ALGORITIM
#---------------------------------------------------------------------------------------------------------------------------------
#Devido ao tamanho da base demora um pouco, na minha máquina demorou uma média de 15min
cn2_census = Orange.classification.rules.CN2Learner()
regras_census = cn2_census(base_census_training)

#Print das regras| adicionei um count para ver quantas foram criadas
count = 0
for regras in regras_census.rule_list:
  print(regras)
  count += 1
print("\n----------------------------------------")
print('Total de regras: ', count)

#ANALYSIS

try:
    previsoes_census = Orange.evaluation.testing.TestOnTestData(base_census_training, base_census_test, [lambda testdata: regras_census])
    ca = Orange.evaluation.CA(previsoes_census)
    mean = ca[0]*100
    print(previsoes_census)
    print("Previsão gerada com sucesso!")
    print('\n-------------------------------------------')
    print('Mean: {:.2f}%'.format(mean))
except Exception as e:
    print('Erro:', str(e))




