import pandas as pd


#########################################################
#################### SET UP DATA ########################
#########################################################

##########Fixed Cost and Charging Load cost#################

''' 
Create A J C index with dummy station
J: a list of indexs of real stations
A: a list of the fixed cost
C: a list of the Capacity Cost
A_dict: a dict of A with J as key
C_dict: a dict of C with J as key
'''
# Create List first
# J = list(pd.read_excel('mini.xlsx','LocationData').values[:,0])
# A = list(pd.read_excel('mini.xlsx','LocationData').values[:,1])
# C = list(pd.read_excel('mini.xlsx','LocationData').values[:,2])


I = [i for i in range(1,48) ]+[71]
A = list(pd.read_excel('Networks_123_1.xlsx','LocationData').values[:,1])
C = list(pd.read_excel('Networks_123_1.xlsx','LocationData').values[:,2])
# Create the dictionary
A_dict = {}
for key in I:
    A_dict[key] = A[I.index(key)]
C_dict = {}
for key in I:
    C_dict[key] = C[I.index(key)]
    
zero = 0.001

########## Taffic Flow Data #################
'''
Create Taffic Flow Data
D_mat: a matrix rows for each node; columns for each scenario
current_demand: a list to be replace when in STO file
number_scenaro: number of columns in the D_mat
'''

#########################################################
#################### SET UP DATA ########################
#########################################################

##########Fixed Cost and Charging Load cost#################

''' 
Create A J C index with dummy station
J: a list of indexs of real stations
A: a list of the fixed cost
C: a list of the Capacity Cost
A_dict: a dict of A with J as key
C_dict: a dict of C with J as key
'''
# Create List first
# J = list(pd.read_excel('mini.xlsx','LocationData').values[:,0])
# A = list(pd.read_excel('mini.xlsx','LocationData').values[:,1])
# C = list(pd.read_excel('mini.xlsx','LocationData').values[:,2])


# I = list(pd.read_excel('Networks_123.xlsx','LocationData').values[:,0])
# A = list(pd.read_excel('Networks_123.xlsx','LocationData').values[:,1])
# C = list(pd.read_excel('Networks_123.xlsx','LocationData').values[:,2])


#I = list(pd.read_excel('Networks_123_1.xlsx','LocationData').values[:,0])
I = [i for i in range(1,48) ]+[71]
A = list(pd.read_excel('Networks_123_1.xlsx','LocationData').values[:,1])
C = list(pd.read_excel('Networks_123_1.xlsx','LocationData').values[:,2])
# Create the dictionary
A_dict = {}
for key in I:
    A_dict[key] = A[I.index(key)]
C_dict = {}
for key in I:
    C_dict[key] = C[I.index(key)]
    
zero = 0.001



########## Taffic Flow Data #################
'''
Create Taffic Flow Data
D_mat: a matrix rows for each node; columns for each scenario
current_demand: a list to be replace when in STO file
number_scenaro: number of columns in the D_mat
'''

# D_mat = pd.read_excel('Networks.xlsx','Demand_TN').values[:,1:][0:]


number_scenario = 2

D_mat = pd.read_excel('Demand2.xlsx').values[:,1: number_scenario + 1][0:]
Demand_Multiplier = 4
Load_Multiplier = 1

#D_mat = pd.read_excel('Demand_bp.xlsx').values[:,1:][0:]

current_demand = [D_mat[i,0] for i in range(D_mat.shape[0]) ]
#number_scenario = D_mat.shape[1]




# Create Large number M    
# M = (max(sum(D_mat)) * 12+1)*Demand_Multiplier

M = 900





#Utility  = pd.read_excel('Networks.xlsx','Utility').values[:,1:]
Utility  = pd.read_excel('Utility2.xlsx',index_col=[0,1])
# Utility  = pd.read_excel('Utility2_new.xlsx',index_col=[0,1])
#Utility  = pd.read_excel('Utility_bp2.xlsx',index_col=[0,1])
U_dict = Utility.to_dict(orient='index')
Umin = 0.50
Ud = 1

for i in range(1,75):
    U_dict[(i,0)] = {}
    for j in range(number_scenario):
        if 0 < j < 3:
            U_dict[(i,0)][j] = 0.50
        else:
            U_dict[(i,0)][j] = 0.50



########## Power Flow Data #################

#PDN_line_mat = pd.read_excel('Networks_123.xlsx','PDN_line').values
PDN_line_mat = pd.read_excel('Networks_123_1.xlsx','PDN_line').values
PDN_line_list = []
for i in range(PDN_line_mat.shape[0]):
    PDN_line_list.append((int(PDN_line_mat[i][0])-1,int(PDN_line_mat[i][1]-1)))
    

        
Q_load_dict = {}

#Resistance, Reactance Capacity Power flow
R_dict = {}
X_dict = {}
# Pmax = {}
# Qmax = {}
#G_dict = {}
for i in range(PDN_line_mat.shape[0]):
    R_dict[PDN_line_list[i]] = PDN_line_mat[i][2] * 1/1
    X_dict[PDN_line_list[i]] = PDN_line_mat[i][3] * 1/1

############### PDN Node #################
    
#PDN Node with scenario
P_load_mat = pd.read_excel('Pload_123.xlsx').values[:,1:number_scenario+1]
Q_load_mat = pd.read_excel('Qload_123.xlsx').values[:,1:number_scenario+1]

P_load = pd.read_excel('Pload_123.xlsx',index_col=[0])
Q_load = pd.read_excel('Qload_123.xlsx',index_col=[0])

P_load_dict = P_load.to_dict(orient='index')

for i in range(1,119):
    if i not in P_load_dict.keys(): 
        P_load_dict[i] = {}
        for t in range(108):
                
                P_load_dict[i][4*t]=0
                P_load_dict[i][4*t+1]=0
                P_load_dict[i][4*t+2]=0
                P_load_dict[i][4*t+3]=0
    else:
        for t in range(108):
                current = P_load_dict[i][t]
                P_load_dict[i][4*t]=current
                P_load_dict[i][4*t+1]=current
                P_load_dict[i][4*t+2]=current
                P_load_dict[i][4*t+3]=current
                
                
Q_load_dict = Q_load.to_dict(orient='index')

for i in range(1,119):
    if i not in Q_load_dict.keys(): 
        Q_load_dict[i] = {}
        for t in range(108):
                
                Q_load_dict[i][4*t]=0
                Q_load_dict[i][4*t+1]=0
                Q_load_dict[i][4*t+2]=0
                Q_load_dict[i][4*t+3]=0
    else:
        for t in range(108):
                current = Q_load_dict[i][t]
                Q_load_dict[i][4*t]=current
                Q_load_dict[i][4*t+1]=current
                Q_load_dict[i][4*t+2]=current
                Q_load_dict[i][4*t+3]=current









# First Stage
Gmn = 300  #Distribution Line Cost
L = 0.788 #Substation Capacity Expansion Cost

# Second Stage
# Voltage
Vmax = (2.4*1.05)**2
Vmin = (2.4*0.95)**2
V0 = (2.4*1.00)**2

# Power
PMax = pd.read_excel('Pmn.xlsx').values[:,:]

node_str = list(PMax[:,0])
nodes = []
for i in node_str:
    first = i.replace('(','')
    second = first.replace(")",'')
    third = second.replace(' ','')
    temp = third.split(',')
    temp_node = (int(temp[0]),int(temp[1]))
    nodes.append(temp_node)
Pmn = list(PMax[:,1])
PMax_dict = {}
for i in range(len(node_str)):
    PMax_dict[nodes[i]] = 1.5*Pmn[i]
    #PMax_dict[nodes[i]] = Pmn[i]*100
    
QMax = pd.read_excel('Qmn.xlsx').values[:,:]

node_str = list(QMax[:,0])
nodes = []
for i in node_str:
    first = i.replace('(','')
    second = first.replace(")",'')
    third = second.replace(' ','')
    temp = third.split(',')
    temp_node = (int(temp[0]),int(temp[1]))
    nodes.append(temp_node)
Qmn = list(QMax[:,1])
QMax_dict = {}
for i in range(len(node_str)):
   QMax_dict[nodes[i]] =1.5*Qmn[i]
   #QMax_dict[nodes[i]] = Qmn[i]*100

# PMax = 1000000000
# QMax = 1000000000

W = 7.7  #Power Needed for each Charging Demand
B = 10





########## TN set ##########






##################### Parameter Adjustment #########################
alpha = 1 # adjust Station building related cost; default value = 1
beta = 1 # 1adjust Expansion line; default value = 1
theta = 1 # Downtown Uptown difference



########## PDN Set ##########
N = [n for n in range(1,119)]  #PDN Nodes
NF = [0]
E = [] #PDN lines
for i in range(PDN_line_mat.shape[0]):
    E.append((int(PDN_line_mat[i][0])-1,int(PDN_line_mat[i][1])-1))
    
K = [k for k in range(1,3)]


######  TN PDN Corresponding Relation ####

G = 30
H = 2*G
H_0 = 1.5
J = [1,3,2,6,7,10,12,13,16,20,21,22,25,27, 29,32,35,36,38,45]
TN_PDN = {1:20, 2:22, 3:24, 6:34 ,7:27  ,10:39, 12:61 ,13:62,16:63,  20: 41,
          21:4, 22:64, 25:2, 27:3, 29:66, 32:43, 35:13, 36:10, 38:100, 45:51,0:-1}
J_plus = [0]+J
# TN_PDN = {1: 21, 2:20, 4:8, 5:5, 10:3, 11: 6, 13:29, 14:7, 15:4, 20:27, 0:-1}
# TN_PDN = {1: 2,0:-1,4:7, 10:1, 20:24}
# TN_PDN = {1: 1,4:6,10:13,11:16,15:23,20:27,0:-1}



# ######  TN PDN Corresponding Relation ####
# G = 30
# H = 2*G
# H_0 = 1.5
# J = [1,3,2,6,7,10,12,13,16,20,21,22,23,25,27, 29,32,35,36,38,45]
# TN_PDN = {1:20, 2:22, 3:24, 6:34 ,7:27  ,10:39, 12:61 ,13:62,16:63,  20: 41,
#           21:1, 22:64, 23:3 , 25:4, 27:5, 29:66, 32:43, 35:13, 36:10, 38:100, 45:51,0:-1}
# J_plus = [0]+J


M_dict = {}

for j in J:
    M_dict[j]={}

for t in range(number_scenario):
    if 0 < t < 3:
        Umin_temp = 0.45
    else:
        Umin_temp = 0.45
    for j in J:
        M_dict[j][t] = 0
        for i in I:
            if U_dict[(i,j)][t] > Umin_temp:
                M_dict[j][t] += D_mat[i-1][t] * Demand_Multiplier
            
M_hat_dict = {}               
for j in J:
    M_hat_dict[j] = max([M_dict[j][t] for t in range(number_scenario)])
    

total_D_dict = {}
for t in range(number_scenario):
    total_D_dict[t] = sum(D_mat[:,t])*Demand_Multiplier



J_start = [1,6,10,12,13,16,20,25,29,35,36,38,45]
X_start = {1:10, 6:10, 10:68, 12:10, 13:22 , 16:10 , 20:23 , 25:580 , 29:10 , 35:111 , 36:38 , 38:10 , 45:129 }
U_start = []



J_start = []
X_start = {}
U_start = []

############################### Fast Initial for  H= 2.5G ###############################
J_start = [1,6,10,12,13,16,20,25,29,35,36,38,45]
X_start = {1:10, 6:10, 10:68, 12:10, 13:22 , 16:10 , 20:23 , 25:580 , 29:10 , 
           35:111 , 36:38 , 38:10 , 45:129 }
###########################################################################################################################################################


############################### General start ###############################

J_start = [1,3,2,6,7,10,12,13,16,20,21,22, 23,25,27, 29,32,35,36,38,45]
X_start = {1:10,3:10,2:10,6:10,7:10,10:10,
           12:10,13:10,16:10,20:10,21:10,22:10,23:10,
           25:10,27:10, 29:10,32:10,35:10,36:10,
           38:10,45:10}


#######################################################################################

J_start = [1,3,2,6,7,10,12,13,16,20,21,22, 23,25,27, 29,32,35,36,38,45]
X_start = {1:0,3:0,2:0,6:0,7:0,10:0,
           12:0,13:0,16:0,20:0,21:0,22:0,23:0,
           25:0,27:0, 29:0,32:0,35:0,36:0,
           38:0,45:0}


################

############################### first round ###############################
# J_start = [1,3,2,6,7,10,12,13,16,20,21,25, 29,32,35,36,38,45]
# X_start = {1:56,3:10,2:10,6:28,7:10,10:10,
#            12:10,13:10,16:10,20:10,21:10,22:10,
#            25:580,27:10, 29:10,32:10,35:112,36:10,
#            38:10,45:100}
# #######################################################################################


U_start = []
U_start_2 = [(item[0], item[1]) for item in U_start]
U_start_dict = {}
for item in U_start:
    U_start_dict[(item[0], item[1])] = item[2]
















####################################################
###################   Core File    #################
####################################################
core = open("small.mps", "w")
core.write('{:<14s}{:<15s}\n'.format('NAME',"Transportion"))

########## Write Rows ##########
################################
#Rows includes the objective functions names and the direction of inequality
################################

core.write('ROWS\n')


'''
Create the name of constrains as list
Then write the constrains with their direction
'''
################ STAGE 1 ###################
obj = 'obj'
c1_1_name = ['c1-1_{}'.format(i) for i in J]
c1_1_direction = 'L'

c1_2_name = ['c1-2_{}_{}'.format(i[0], i[1]) for i in E ]
c1_2_direction = 'L'


################ STAGE 2 ###############


##########    TN    ############
c2_0_name = ['c2-0_1', 'c2-0_2']
c2_0_direction = 'E'




c1_1_L_name = ['c1-1_L_{}'.format(i) for i in J]
c1_1_L_direction = 'G'


c2_1_name = ['c2-1_{}'.format(i) for i in J_plus]
c2_1_direction = 'L'



c2_1_L_name = ['c2-1_L_{}'.format(i) for i in J_plus]
c2_1_L_direction = 'G'


c2_2_name = ['c2-2_{}'.format(i) for i in J]
c2_2_direction = 'L'

##### 3-D #######
# c2_3_name = ['c2-3_{}_{}_{}'.format(i, j, k) for i in I for j in J_plus for k in J_plus ]
# c2_3_direction = 'G'


##### 2-D #######
# c2_3_name = ['c2-3_{}_{}'.format(i, k) for i in I for k in J_plus ]
# c2_3_direction = 'G'



##### 1-D #######
c2_3_name = ['c2-3_{}'.format(k) for k in J_plus ]
c2_3_direction = 'G'




c2_4_name = ['c2-4_{}'.format(i) for i in I]
c2_4_direction = "E"



######### PDN   ##########

#Pload node balance
c2_5_name = ['c2-5_{}'.format(i) for i in N]
c2_5_direction = 'E'

#Qload node balance
c2_6_name = ['c2-6_{}'.format(i) for i in N]
c2_6_direction = 'E'

#Ohm's Law
c2_7_name = ['c2-7_{}_{}'.format(i[0],i[1]) for i in E]
c2_7_direction = 'G'

#Vn bound
c2_8_L_name = ['c2-8-L_{}'.format(i) for i in N]
c2_8_L_direction = 'G'
c2_8_R_name = ['c2-8-R_{}'.format(i) for i in N]
c2_8_R_direction = 'L'

#r bound
c2_9_name = ['c2-9_{}_{}_{}'.format(i[0], i[1], k) for i in E for k in K ]
c2_9_direction = 'L'

#vn-rn bound
c2_10_L_name = ['c2-10-L_{}_{}_{}'.format(i[0], i[1], k) for i in E for k in K ]
c2_10_L_direction = 'G'

c2_10_R_name = ['c2-10-R_{}_{}_{}'.format(i[0], i[1], k) for i in E for k in K ]
c2_10_R_direction = 'L'

#t bound
c2_11_name = ['c2-11_{}_{}_{}'.format(i[0], i[1], k) for i in E for k in K ]
c2_11_direction = 'L'

#vn-tn bound
c2_12_L_name = ['c2-12-L_{}_{}_{}'.format(i[0], i[1], k) for i in E for k in K ]
c2_12_L_direction = 'G'

c2_12_R_name = ['c2-12-R_{}_{}_{}'.format(i[0], i[1], k) for i in E for k in K ]
c2_12_R_direction = 'L'

#pmn bound
c2_13_name = ['c2-13_{}_{}'.format(i[0],i[1]) for i in E]
c2_13_direction = 'L'

#qmn bound
c2_14_name = ['c2-14_{}_{}'.format(i[0],i[1]) for i in E]
c2_14_direction = 'L'

#V0 fix
c2_15_name = ['c2-15_{}'.format(i) for i in [0]]
c2_15_direction = 'E'

c2_16_name = ['c2-16']
c2_16_direction = 'L'
c2_17_name = ['c2-17']
c2_17_direction = 'L'

# write the rows
core.write(' {:3}{}\n'.format('N','obj'))


for item in c1_1_L_name:
    core.write(' {:3}{}\n'.format(c1_1_L_direction,item))
for item in c1_1_name:
    core.write(' {:3}{}\n'.format(c1_1_direction,item))
for item in c1_2_name:
    core.write(' {:3}{}\n'.format(c1_2_direction,item))
for item in c2_0_name:
    core.write(' {:3}{}\n'.format(c2_0_direction,item))
    
    
for item in c2_1_L_name:
    core.write(' {:3}{}\n'.format(c2_1_direction,item))  
    
for item in c2_1_name:
    core.write(' {:3}{}\n'.format(c2_1_direction,item))
for item in c2_2_name:
    core.write(' {:3}{}\n'.format(c2_2_direction,item)) 

for item in c2_3_name:
    core.write(' {:3}{}\n'.format(c2_3_direction,item))

for item in c2_4_name:
    core.write(' {:3}{}\n'.format(c2_4_direction,item))

for item in c2_5_name:
    core.write(' {:3}{}\n'.format(c2_5_direction,item))
    
for item in c2_6_name:
    core.write(' {:3}{}\n'.format(c2_6_direction,item))


for item in c2_7_name:
    core.write(' {:3}{}\n'.format(c2_7_direction,item))
    
for item in c2_8_L_name:
    core.write(' {:3}{}\n'.format(c2_8_L_direction,item))
    
for item in c2_8_R_name:
    core.write(' {:3}{}\n'.format(c2_8_R_direction,item))


for item in c2_9_name:
    core.write(' {:3}{}\n'.format(c2_9_direction,item))
    
for item in c2_10_L_name:
    core.write(' {:3}{}\n'.format(c2_10_L_direction,item))
    
for item in c2_10_R_name:
    core.write(' {:3}{}\n'.format(c2_10_R_direction,item))
    
# for item in c2_11_name:
#     core.write(' {:3}{}\n'.format(c2_11_direction,item))
    
    
# for item in c2_12_L_name:
#     core.write(' {:3}{}\n'.format(c2_12_L_direction,item))
    
# for item in c2_12_R_name:
#     core.write(' {:3}{}\n'.format(c2_12_R_direction,item))
    
    
for item in c2_13_name:
    core.write(' {:3}{}\n'.format(c2_13_direction,item))
    
for item in c2_14_name:
    core.write(' {:3}{}\n'.format(c2_14_direction,item))
    
for item in c2_15_name:
    core.write(' {:3}{}\n'.format(c2_15_direction,item))
    
for item in c2_16_name:
    core.write(' {:3}{}\n'.format(c2_16_direction,item))
    
for item in c2_17_name:
    core.write(' {:3}{}\n'.format(c2_17_direction,item))



########## Write Columns ##########
################################
#Columns include the variable names and coefficients
################################
core.write('COLUMNS\n')

'''
Create the name of variables and corresponding coefficient at the corresponding constrains
1. Create the category of the variables
2. Create a dict with the category as key and names as values
3. Create a nested dict, primary key: variable names; secondary key: constraint name
    Value: Coefficients
'''

# Create category variable name dict
variable_category_list = ['z' , 'x' ,'y','s', 'u', 'p','q','v','u00','r','t' ]

variable_name_dict = {}

for key in variable_category_list:
    if key == 'z':
        variable_name_dict[key] = []
        for i in J_plus:
            current_name = 'z_{}'.format(i)
            variable_name_dict[key].append(current_name)
            
    if key == 'x':
        variable_name_dict[key] = []
        for i in J_plus:
            current_name = 'x_{}'.format(i)
            variable_name_dict[key].append(current_name)

    if key == 'y':
        variable_name_dict[key] = []
        for i in I:
            for j in J_plus:
                #index = (i,j)
                current_name = 'y_{}_{}'.format(i,j)
                variable_name_dict[key].append(current_name)
                
    if key == 's':
        variable_name_dict[key] = []
        for i in J_plus:
            current_name = 's_{}'.format(i)
            variable_name_dict[key].append(current_name)
            
    if key == 'u':
        variable_name_dict[key] = []
        for e in E:
            for k in K:
                current_name = 'u_{}_{}_{}'.format(e[0],e[1],k)
                variable_name_dict[key].append(current_name)
                
    if key == 'p':
        variable_name_dict[key] = []
        for e in E:
            current_name = 'p_{}_{}'.format(e[0],e[1])
            variable_name_dict[key].append(current_name)
            
    
    if key == 'q':
        variable_name_dict[key] = []
        for e in E:
            current_name = 'q_{}_{}'.format(e[0],e[1])
            variable_name_dict[key].append(current_name)
            
    
    if key == 'v':
        variable_name_dict[key] = []
        for n in N:
            current_name = 'v_{}'.format(n)
            variable_name_dict[key].append(current_name)
            
        for n in NF:
            current_name = 'v_{}'.format(n)
            variable_name_dict[key].append(current_name)
            
    if key == 'r':
        variable_name_dict[key] = []
        for e in E:
            for k in K:
                current_name = 'r_{}_{}_{}'.format(e[0],e[1],k)
                variable_name_dict[key].append(current_name)
                
                
    # if key == 't':
    #     variable_name_dict[key] = []
    #     for e in E:
    #         for k in K:
    #             current_name = 't_{}_{}_{}'.format(e[0],e[1],k)
    #             variable_name_dict[key].append(current_name)
            
    
    if key == 'u00':
        variable_name_dict[key] = ['u00']


            
    
'''
Ways to create third dict:
    1. manually add variable names based on the variable dict
    2. split the variable name index 
    3. manually identify and add the category of constraints the variables appear
    4. split the constraint name index
    5. match the index
'''
# Coefficient nested dict
variable_constr_dict = {}


# Z variable
for key in variable_name_dict['z']:
    
    
    key_index = (int(key.split("_")[-1]))
    variable_constr_dict[key] = {}
    
    
    #obj except dummy station 
    if key_index>0:
        if key_index in J_start:
            variable_constr_dict[key]['obj'] = -alpha *  A_dict[key_index]/1000
        else:
            variable_constr_dict[key]['obj'] = alpha *  A_dict[key_index]/1000
    
    #first stage 
    for constr in c1_1_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if key_index in J_start:
                variable_constr_dict[key][constr] = M_hat_dict[key_index]
            else:
                variable_constr_dict[key][constr] = -M_hat_dict[key_index]
                
    
    
    for constr in c1_1_L_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if key_index in J_start:
                variable_constr_dict[key][constr] = B
            else:
                variable_constr_dict[key][constr] = -B

    
    
            
    #second stage
    if key_index == 0:
        variable_constr_dict[key][c2_0_name[0]] = 1

    for constr in c2_2_name:
            
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if key_index in J_start:
                variable_constr_dict[key][constr] = M_dict[key_index][0]
            else:
                variable_constr_dict[key][constr] = -M_dict[key_index][0]


    for constr in c2_3_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index_j = int(constr.split("_")[1:][-2])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if key_index in J_start:
                variable_constr_dict[key][constr] =  total_D_dict[0]
            else:
                variable_constr_dict[key][constr] =  -total_D_dict[0]
                    #variable_constr_dict[key][constr] = - M
        
        
        



# X variable
for key in variable_name_dict['x']:
    key_index = (int(key.split("_")[-1]))
    variable_constr_dict[key] = {}
    
    #obj   
    if key_index>0:     
        if key_index in J_start:
            variable_constr_dict[key]['obj'] = -alpha *  C_dict[key_index]/1000
        else:
            variable_constr_dict[key]['obj'] = alpha *  C_dict[key_index]/1000
    
    #first stage
    for constr in c1_1_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if key_index in J_start:
                variable_constr_dict[key][constr] = -1
            else:
                variable_constr_dict[key][constr] = 1
    
    for constr in c1_1_L_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if key_index in J_start:
                variable_constr_dict[key][constr] = -1
            else:
                variable_constr_dict[key][constr] = 1
    
    
    #second stage
    #dummy
    if key_index == 0:
        if key_index in J_start:
            variable_constr_dict[key][c2_0_name[1]] = -1
        else:
            variable_constr_dict[key][c2_0_name[1]] = 1
        
    for constr in c2_1_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if key_index in J_start:
                variable_constr_dict[key][constr] = 1
            else:
                variable_constr_dict[key][constr] = -1
            
    
# U00 variable
for key in variable_name_dict['u00']:
    
    #obj 
    variable_constr_dict[key] = {}
    variable_constr_dict[key]['obj'] = beta * L
    
    #second stage
    for constr in c2_16_name:
        variable_constr_dict[key][constr] = -1
        
    for constr in c2_17_name:
        variable_constr_dict[key][constr] = -1
            
# Y variable
for key in variable_name_dict['y']:
    key_index = (key.split("_")[1:])
    key_index_i = int(key_index[0])
    key_index_j = int(key_index[1])
    variable_constr_dict[key] = {}
    
    #obj
    if key_index_j > 0:
        variable_constr_dict[key]['obj'] = -G*U_dict[(key_index_i,key_index_j)][0]
    
    
    #second stage
    for constr in c2_1_name:
        constr_index = (constr.split("_")[1:])
        #key_index = (int(key.split("_")[-1]))
        if int(constr_index[0]) == int(key_index[1]):
            variable_constr_dict[key][constr] = 1
    
    
    for constr in c2_3_name:
        constr_index = constr.split("_")[1:][-1:]

        constr_index_k = int(constr_index[0])
        #key_index = (int(key.split("_")[-1]))
        if U_dict[(key_index_i,key_index_j)][0] < Umin:
            variable_constr_dict[key][constr] = -1
        else:
            coef = U_dict[(key_index_i,key_index_j)][0] \
                - max(U_dict[(key_index_i,constr_index_k)][0] - Ud,Umin )
            if coef >= 0:
                coef = 0
            else:
                coef = -1
            #variable_constr_dict[key][constr] = U_dict[(key_index_i,key_index_j)][0] \
                #- max(U_dict[(key_index_i,constr_index_k)][0] - Ud,Umin )
            variable_constr_dict[key][constr] = coef
            
    
    for constr in c2_4_name:
        constr_index = (constr.split("_")[1:])
        #key_index = (int(key.split("_")[-1]))
        if int(constr_index[0]) == int(key_index[0]):
            variable_constr_dict[key][constr] = 1
            
    
    for constr in c2_5_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == TN_PDN[key_index_j]:
            variable_constr_dict[key][constr] = -W        
    

# S variable
for key in variable_name_dict['s']:
    key_index = (int(key.split("_")[-1]))
    variable_constr_dict[key] = {}
    
    if key_index == 0:
        variable_constr_dict[key]['obj'] = H_0 * G
        
    if key_index > 0:
        variable_constr_dict[key]['obj'] = H
    #second stage
    for constr in c2_1_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -1
    
    for constr in c2_2_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1
            
    for constr in c2_2_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1

  
    for constr in c2_5_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == TN_PDN[key_index]:
            variable_constr_dict[key][constr] = W


# P variable
for key in variable_name_dict['p']:
    key_index = (int(key.split("_")[-2]),int(key.split("_")[-1]))
    variable_constr_dict[key] = {}

  
    for constr in c2_5_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index[0]:
            variable_constr_dict[key][constr] = -1
        if constr_index == key_index[1]:
            variable_constr_dict[key][constr] = 1
            
            
    for constr in c2_7_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -2 * R_dict[key_index]
            
    for constr in c2_13_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1
            
    for constr in c2_16_name:
        if key_index in [(0,2),(0,6)]:
            variable_constr_dict[key][constr] = 1
        


    

# Q variable
for key in variable_name_dict['q']:
    key_index = (int(key.split("_")[-2]),int(key.split("_")[-1]))
    variable_constr_dict[key] = {}

  
    for constr in c2_6_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index[0]:
            variable_constr_dict[key][constr] = -1
        if constr_index == key_index[1]:
            variable_constr_dict[key][constr] = 1
            
            
    for constr in c2_7_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -2 * X_dict[key_index]
            
    for constr in c2_14_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1
            
    for constr in c2_17_name:
        if key_index == (0,1):
            variable_constr_dict[key][constr] = 1


#V variable
for key in variable_name_dict['v']:
    key_index = int(key.split("_")[-1])
    variable_constr_dict[key] = {}
    
    for constr in c2_7_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index[0] == key_index:
            variable_constr_dict[key][constr] = 1000
            
        if constr_index[1] == key_index:
            variable_constr_dict[key][constr] = -1000
            
    for constr in c2_8_L_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1
            
    for constr in c2_8_R_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1
            
    
    for constr in c2_10_L_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        if key_index == constr_index[0][0]:
            variable_constr_dict[key][constr] = 1
        if key_index == constr_index[0][1]:
            variable_constr_dict[key][constr] = -1
        
    
    for constr in c2_10_R_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        if key_index == constr_index[0][0]:
            variable_constr_dict[key][constr] = 1
        if key_index == constr_index[0][1]:
            variable_constr_dict[key][constr] = -1
            
            
    # for constr in c2_12_L_name:
    #     constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
    #     if key_index == constr_index[0][1]:
    #         variable_constr_dict[key][constr] = 1
    
    # for constr in c2_12_R_name:
    #     constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
    #     if key_index == constr_index[0][1]:
    #         variable_constr_dict[key][constr] = 1
            
    for constr in c2_15_name:
        if key_index == 0:
            variable_constr_dict[key][constr] = 1
    
    




# r variable
for key in variable_name_dict['r']:
    key_index = ((int(key.split("_")[-3]),int(key.split("_")[-2])),int(key.split("_")[-1]))
    variable_constr_dict[key] = {}
    
    for constr in c2_7_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index[0]:
            variable_constr_dict[key][constr] = 1
            
    for constr in c2_9_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1
            
    for constr in c2_10_L_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -1
            
    for constr in c2_10_R_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -1
            
    
            

# t varible
# for key in variable_name_dict['t']:
#     key_index = ((int(key.split("_")[-3]),int(key.split("_")[-2])),int(key.split("_")[-1]))
#     variable_constr_dict[key] = {}
    
#     for constr in c2_7_name:
#         constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
#         #key_index = (int(key.split("_")[-1]))
#         if constr_index == key_index[0]:
#             variable_constr_dict[key][constr] = -1
    
#     for constr in c2_11_name:
#         constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
#         #key_index = (int(key.split("_")[-1]))
#         if constr_index == key_index:
#             variable_constr_dict[key][constr] = 1
            
#     for constr in c2_12_L_name:
#         constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
#         #key_index = (int(key.split("_")[-1]))
#         if constr_index == key_index:
#             variable_constr_dict[key][constr] = -1
            
#     for constr in c2_12_R_name:
#         constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
#         #key_index = (int(key.split("_")[-1]))
#         if constr_index == key_index:
#             variable_constr_dict[key][constr] = -1

# u variable
for key in variable_name_dict['u']:
    key_index = ((int(key.split("_")[-3]),int(key.split("_")[-2])),int(key.split("_")[-1]))
    key_m = key_index[0][0]
    key_n = key_index[0][1]
    key_k = key_index[1]
    variable_constr_dict[key] = {}
    
    # if ((key_m+1) in PDN_resi_nodes) and ((key_n+1) in PDN_resi_nodes): 
    #     variable_constr_dict[key]['obj'] = beta * Gmn
    # elif ((key_m+1) in PDN_resi_nodes) and ((key_n+1) in PDN_comm_nodes): 
    #     variable_constr_dict[key]['obj'] = beta * Gmn/2
    # elif ((key_m+1) in PDN_comm_nodes) and ((key_n+1) in PDN_resi_nodes): 
    #     variable_constr_dict[key]['obj'] = beta * Gmn/2
    # else:
    #     variable_constr_dict[key]['obj'] = beta * Gmn/4   
    
    if (key_m, key_n, key_k) in U_start:
        variable_constr_dict[key]['obj'] = -beta * Gmn * key_k
    else:
        variable_constr_dict[key]['obj'] = beta * Gmn * key_k
        
    
    for constr in c1_2_name:
        constr_index =(int(constr.split("_")[-2]),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if (key_m,key_n) == constr_index:
            if (key_m, key_n, key_k) in U_start:
                variable_constr_dict[key][constr] = -1
            else:
                variable_constr_dict[key][constr] = 1
                

    
    
    for constr in c2_9_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if (key_m, key_n, key_k) in U_start:
                variable_constr_dict[key][constr] = Vmax
            else:
                variable_constr_dict[key][constr] = -Vmax
            
    
    for constr in c2_10_R_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            if (key_m, key_n, key_k) in U_start:
                variable_constr_dict[key][constr] = -Vmax
            else:
                variable_constr_dict[key][constr] = Vmax
            
    # for constr in c2_11_name:
    #     constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
    #     #key_index = (int(key.split("_")[-1]))
    #     if constr_index == key_index:
    #         variable_constr_dict[key][constr] = -Vmax
            
            
    # for constr in c2_12_R_name:
    #     constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
    #     #key_index = (int(key.split("_")[-1]))
    #     if constr_index == key_index:
    #         variable_constr_dict[key][constr] = Vmax
            
    
    for constr in c2_13_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index[0]:
            if (key_m, key_n, key_k) in U_start:
                variable_constr_dict[key][constr] = PMax_dict[constr_index] * key_k
            else:
                variable_constr_dict[key][constr] = -PMax_dict[constr_index] * key_k
            
            
            
    for constr in c2_14_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index[0]:
            if (key_m, key_n, key_k) in U_start:
                variable_constr_dict[key][constr] = QMax_dict[constr_index] * key_k
            else:
                variable_constr_dict[key][constr] = -QMax_dict[constr_index] * key_k


# write the columns
for name in variable_constr_dict.keys():
    count = 0
    for k,v in variable_constr_dict[name].items():
        if count%2 ==0:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format(name,k,v))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(k,v))
        count +=1
    if count %2 ==1:
        core.write('\n')
        
        
        

###########RHS##########
#for 
core.write("RHS\n")

RHS_count = 0

for name in c1_1_name:
    key_index = int(name.split("_")[1:][-1])
    if RHS_count%2 == 0:
        if key_index in J_start:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,M_hat_dict[key_index]-X_start[key_index]))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        if key_index in J_start:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,M_hat_dict[key_index]-X_start[key_index]))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1
    
    
for name in c1_1_L_name:
    key_index = int(name.split("_")[1:][-1])
    if RHS_count%2 == 0:
        if key_index in J_start:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,B-X_start[key_index]))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        if key_index in J_start:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,B-X_start[key_index]))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1
    
    
for name in c1_2_name:
    key_index = (int(name.split("_")[1:][-2]),int(name.split("_")[1:][-1]) )
    
    if RHS_count%2 == 0:
        if key_index in U_start_2:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 0 ))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 1 ))
    else:
        if key_index in U_start_2:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,1))
            
    RHS_count +=1
    
for name in c2_0_name:
    if RHS_count%2 == 0:
        if name == 'c2-0_1':
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,1))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        if name == 'c2-0_1':
            core.write('{:<20s}   {:>25.5f}\n'.format(name,1))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1
  
for name in c2_1_name:
    key_index = int(name.split("_")[1:][-1])
    if RHS_count%2 == 0:
        if key_index in J_start:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,X_start[key_index]))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        if key_index in J_start:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,X_start[key_index]))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1


for name in c2_1_L_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1 


for name in c2_2_name:
    key_index = int(name.split("_")[1:][-1])
    if RHS_count%2 == 0:
        if key_index in J_start:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,M_dict[key_index][0]))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        if key_index in J_start:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,M_dict[key_index][0]))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1

for name in c2_3_name:

    key_index = int(name.split("_")[1:][-1])
    if RHS_count%2 == 0:
        if key_index in J_start:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, - 2*total_D_dict[0] ))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, - total_D_dict[0] ))   
            #core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, - M ))
    else:

        if key_index in J_start:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,- 2*total_D_dict[0] ))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,- total_D_dict[0] ))
            #core.write('{:<20s}   {:>25.5f}\n'.format(name,- M))
    RHS_count +=1


for name in c2_4_name:
    key = int(name.split("_")[1:][-1])
    demand = D_mat[key -1][0] * Demand_Multiplier
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,demand))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,demand))
    RHS_count +=1
    
for name in c2_5_name:
    key = int(name.split("_")[1:][-1])
    current_P = P_load_dict[key][0] *Load_Multiplier
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,current_P ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,current_P))
    RHS_count +=1
    
    
for name in c2_6_name:
    key = int(name.split("_")[1:][-1])
    current_Q = Q_load_dict[key][0]*Load_Multiplier
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,current_Q))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,current_Q))
    RHS_count +=1
  
for name in c2_7_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 0 ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1 
    
for name in c2_8_L_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, Vmin ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,Vmin))
    RHS_count +=1   
    
    
for name in c2_8_R_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, Vmax ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,Vmax))
    RHS_count +=1  
    
for name in c2_9_name:
    constr_index =(int(name.split("_")[-3]),int(name.split("_")[-2]),int(name.split("_")[-1]))
    
    if RHS_count%2 == 0:
        if constr_index in U_start:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, Vmax ))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 0 ))
    else:
        if constr_index in U_start:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,Vmax))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1 
    

for name in c2_10_L_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 0 ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1   
    
    
for name in c2_10_R_name:
    constr_index =(int(name.split("_")[-3]),int(name.split("_")[-2]),int(name.split("_")[-1]))
    if RHS_count%2 == 0:
        if constr_index in U_start:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,  0))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, Vmax ))
    else:
        if constr_index in U_start:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,0 ))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,Vmax))
    RHS_count +=1 
    
    
# for name in c2_11_name:
#     if RHS_count%2 == 0:
#         core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 0 ))
#     else:
#         core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
#     RHS_count +=1 
    
    
# for name in c2_12_L_name:
#     if RHS_count%2 == 0:
#         core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 0 ))
#     else:
#         core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
#     RHS_count +=1   
    
    
# for name in c2_12_R_name:
#     if RHS_count%2 == 0:
#         core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, Vmax ))
#     else:
#         core.write('{:<20s}   {:>25.5f}\n'.format(name,Vmax))
#     RHS_count +=1 
    
    
for name in c2_13_name:
    constr_index =( int(name.split("_")[1:][-2]) , int(name.split("_")[1:][-1]) )
    if RHS_count%2 == 0:
        if constr_index in U_start_2:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, (1+U_start_dict[constr_index] )* PMax_dict[constr_index] ))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, PMax_dict[constr_index] ))
    else:
        if constr_index in U_start_2:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,(1+U_start_dict[constr_index] )*PMax_dict[constr_index]))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,PMax_dict[constr_index]))
            
    RHS_count +=1 


for name in c2_14_name:
    constr_index =( int(name.split("_")[1:][-2]) , int(name.split("_")[1:][-1]) )
    if RHS_count%2 == 0:
        if constr_index in U_start_2:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, (1+U_start_dict[constr_index] )*QMax_dict[constr_index] ))
        else:
            core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, QMax_dict[constr_index] ))
    else:
        if constr_index in U_start_2:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,(1+U_start_dict[constr_index] )*QMax_dict[constr_index]))
        else:
            core.write('{:<20s}   {:>25.5f}\n'.format(name,QMax_dict[constr_index]))
    RHS_count +=1 
    
for name in c2_15_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, V0 ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,V0))
    RHS_count +=1 
    
for name in c2_16_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 2*PMax_dict[0,1] ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,PMax_dict[0,1]))
    RHS_count +=1 
    
for name in c2_17_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, QMax_dict[0,1] ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,QMax_dict[0,1]))
    RHS_count +=1 

###########bounds##########

core.write('\nBOUNDS\n')
for item in variable_name_dict['z']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('BV','Bnd',item))
    #core.write('{:^4s}{:<20s}{:<20s}{:<20s}\n'.format('UP','Bnd',item,'1'))

for item in variable_name_dict['x']:
    key_index = int(item.split("_")[1:][-1])
    if key_index in J_start:
        core.write('{:^4s}{:<20s}{:<20s}{:<20s}\n'.format('UP','Bnd',item, str(X_start[key_index]) ) )
        core.write('{:^4s}{:<20s}{:<20s}{:<20s}\n'.format('LO','Bnd',item,  '-1000' )  )
    else:
        core.write('{:^4s}{:<20s}{:<20s}{:<20s}\n'.format('PL','Bnd',item,'0'))

for item in variable_name_dict['s']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('PL','Bnd',item))
    
for item in variable_name_dict['y']:
    core.write('{:^4s}{:<20s}{:<20s}{:<20s}\n'.format('PL','Bnd',item,'0'))
    
for item in variable_name_dict['p']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('PL','Bnd',item))
    
for item in variable_name_dict['q']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('PL','Bnd',item))
    
    
for item in variable_name_dict['v']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('PL','Bnd',item))
    
for item in variable_name_dict['r']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('PL','Bnd',item))
    
# for item in variable_name_dict['t']:
#     core.write('{:^4s}{:<20s}{:<20s}\n'.format('PL','Bnd',item))
    
for item in variable_name_dict['u']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('BV','Bnd',item))
    #core.write('{:^4s}{:<20s}{:<20s}{:<20s}\n'.format('UP','Bnd',item,'1'))
 
    
##################################################### 
for item in variable_name_dict['u00']:
    core.write('{:^4s}{:<20s}{:<20s}\n'.format('PL','Bnd',item))
#####################################################

core.write('ENDATA')

core.close()







####################################################
##################    Time File   ##################
####################################################
time = open("small.tim", "w")
time.write('{:<14s}{:<15s}\n'.format('TIME',"Transportion"))
time.write('{:<14s}{:<15s}\n'.format('PERIODS',"EXPLICIT"))
time.write('    {:<20s}\n'.format('PERIOD1'))
time.write('    {:<20s}\n'.format('PERIOD2'))

time.write('ROWS\n')


for name in c1_1_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD1'))
    
    
for name in c1_2_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD1'))

for name in c2_0_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))


for name in c2_1_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    

for name in c2_2_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))    

    
for name in c2_3_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2')) 
    
for name in c2_4_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))

for name in c2_5_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_6_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_7_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_8_L_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_8_R_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_9_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
    
for name in c2_10_L_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_10_R_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
    
# for name in c2_11_name:
#     time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
# for name in c2_12_L_name:
#     time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
# for name in c2_12_R_name:
#     time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_13_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_14_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_15_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_16_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in c2_17_name:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))



time.write('COLUMNS\n')

for name in variable_name_dict['x']:
    if name == 'x_0':
        time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    else:
        time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD1'))
  
for name in variable_name_dict['z']:
    if name == 'z_0':
        time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    else:
        time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD1'))    
        
for name in variable_name_dict['u']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD1'))


###########################################    
for name in variable_name_dict['u00']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD1'))
###########################################
    
for name in variable_name_dict['y']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in variable_name_dict['s']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in variable_name_dict['p']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in variable_name_dict['q']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in variable_name_dict['v']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
for name in variable_name_dict['r']:
    time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    
# for name in variable_name_dict['t']:
#     time.write('    {:<20s}{:<20s}\n'.format(name,'PERIOD2'))
    

time.write('ENDATA')
            
time.close()




####################################################
###################   STOCH File    #################
####################################################

stoch = open("small.sto", "w")
stoch.write('{:<24s}{:<20s}\n'.format('STOCH',"Transportion"))

stoch.write('SCENARIOS\n')


stoch.write('{:^4s}{:<20s}{:<20s}{:>25.5f}  {}\n'.format('SC','SCO',"'ROOT'",1/number_scenario,'PERIOD2'))


for i in range(1,number_scenario):
    sc = 'SC'+str(i)
    stoch.write('{:^4s}{:<20s}{:<20s}{:>25.5f}  {}\n'.format('SC', sc,"'ROOT'",1/number_scenario,'PERIOD2'))
    

    
    
    for key in variable_name_dict['y']:
        key_index = (key.split("_")[1:])
        key_index_i = int(key_index[0])
        key_index_j = int(key_index[1])
        variable_constr_dict[key] = {}
        
        if key_index_j != 0:
            stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,'obj' ,-G*U_dict[(key_index_i,key_index_j)][i]))
        
        for constr in c2_3_name:
            constr_index = constr.split("_")[1:][-1:]


            constr_index_k = int(constr_index[0])
            #key_index = (int(key.split("_")[-1]))
            if U_dict[(key_index_i,key_index_j)][i] < Umin:
                coef = -1
            else:
                coef = U_dict[(key_index_i,key_index_j)][i] \
                - max(U_dict[(key_index_i,constr_index_k)][i] - Ud,Umin )
                if coef >= 0:
                    coef = 0
                else:
                    coef = -1
            stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,constr ,coef))
                
                
            
                
            
            
            
    for key in variable_name_dict['z']:
        key_index = int((key.split("_")[-1]))
        
        for constr in c2_2_name:
            constr_index = int(constr.split("_")[1:][-1])
            #key_index = (int(key.split("_")[-1]))
            if constr_index == key_index:
                    
                coef = -M_dict[key_index][i]
                
                if key_index in J_start:
                    stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,constr , -coef))
                else:
                    stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,constr , coef))
                    
                    
        
        for constr in c2_3_name:
            constr_index = constr.split("_")[1:][-1:]

            constr_index_k = int(constr_index[0])
            #key_index = (int(key.split("_")[-1]))
            if key_index == constr_index_k:

                coef = - total_D_dict[i]
                    #coef = -M
                    
                if key_index in J_start:
                    stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,constr , -coef))
                else:
                    stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,constr ,coef))
        
        
                
    # Integer Programming      
    for name in c2_2_name:
        key_index = int(name.split("_")[1:][-1])
        coef =  M_dict[key_index][i]
            #coef = -M
        if key_index in J_start:
            stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        else:
            stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,0))
       
    for name in c2_3_name:
        key_index = int(name.split("_")[1:][-1])
        coef = - total_D_dict[i]
            #coef = -M
        if key_index in J_start:
            stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,2*coef))
        else:
            stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
    for name in c2_4_name:
        index = int(name.split("_")[1:][-1])
        coef = D_mat[index-1][i] * Demand_Multiplier
        stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
    for name in c2_5_name:
        index = int(name.split("_")[1:][-1])
        coef = P_load_dict[index][i] * Load_Multiplier
        stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
    for name in c2_6_name:
        index = int(name.split("_")[1:][-1])
        coef = Q_load_dict[index][i]* Load_Multiplier
        stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
stoch.write('ENDATA')


stoch.close()























