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


I = list(pd.read_excel('Networks.xlsx','LocationData').values[:,0])
A = list(pd.read_excel('Networks.xlsx','LocationData').values[:,1])
C = list(pd.read_excel('Networks.xlsx','LocationData').values[:,2])
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

D_mat = pd.read_excel('demand2.xlsx').values[:,1: number_scenario + 1][0:]
Demand_Multiplier = 2

#D_mat = pd.read_excel('Demand_bp.xlsx').values[:,1:][0:]

current_demand = [D_mat[i,0] for i in range(D_mat.shape[0]) ]
#number_scenario = D_mat.shape[1]




# Create Large number M    
# M = (max(sum(D_mat)) * 12+1)*Demand_Multiplier


M = 300





#Utility  = pd.read_excel('Networks.xlsx','Utility').values[:,1:]
Utility  = pd.read_excel('utility2.xlsx',index_col=[0,1])
#Utility  = pd.read_excel('Utility_bp2.xlsx',index_col=[0,1])
U_dict = Utility.to_dict(orient='index')
Umin = 0.35
Ud = 0

for i in range(1,25):
    U_dict[(i,0)] = {}
    for j in range(number_scenario):
        U_dict[(i,0)][j] = Umin 


########## Power Flow Data #################

PDN_line_mat = pd.read_excel('Networks.xlsx','PDN_line').values
PDN_line_list = []
for i in range(PDN_line_mat.shape[0]):
    PDN_line_list.append((int(PDN_line_mat[i][0]),int(PDN_line_mat[i][1])))
    
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
P_load_mat = pd.read_excel('pload2.xlsx').values[:,1:number_scenario+1]
Q_load_mat = pd.read_excel('qload2.xlsx').values[:,1:number_scenario+1]

# P_load_mat = pd.read_excel('Pload_bp2.xlsx').values[:,1:]
# Q_load_mat = pd.read_excel('Qload_bp2.xlsx').values[:,1:]


TN_resi_nodes = [1,2,3,4,5,11,12,13,19,20,21,22,23,24]
TN_comm_nodes = [7,8,9,10,16,17,18]

######################### PDN parameter ###########################
PDN_resi_nodes = [1,2,22,28,29,30,31,32,17,16,15,12,11,20,19,18,7]
PDN_comm_nodes = [3,4,5,6,8,9,10,13,14,25,26,27,23,24,21]

# First Stage
Gmn = 300  #Distribution Line Cost
L = 0.788 #Substation Capacity Expansion Cost

# Second Stage
# Voltage
Vmax = (12.66*1.05)**2
Vmin = (12.66*0.95)**2
V0 = (12.66*1.00)**2

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
    PMax_dict[nodes[i]] = 1*Pmn[i]/4
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
   QMax_dict[nodes[i]] =1*Qmn[i]/4
   #QMax_dict[nodes[i]] = Qmn[i]*100

# PMax = 1000000000
# QMax = 1000000000

W = 7.7  #Power Needed for each Charging Demand


##################### Parameter Adjustment #########################
G = 30
H = 2*G
H_0 = 1.5

alpha = 1 # adjust Station building related cost; default value = 1
beta = 1 # 1adjust Expansion line; default value = 1
theta = 1 # Downtown Uptown difference


########## TN set ##########
#I TN node
#I = [i+1 for i in range(D_mat.shape[0])]
J = [1, 4,5,10,11,13,14,15,16,20]
# J = [1,4,10,11,15,20]

#Dummy station
J_plus = [0]+J
########## PDN Set ##########
N = [n for n in range(1,33)]  #PDN Nodes
NF = [0]
E = [] #PDN lines
for i in range(PDN_line_mat.shape[0]):
    E.append((int(PDN_line_mat[i][0]),int(PDN_line_mat[i][1])))
    
K = [k for k in range(1,3)]
M_dict = {}

for j in J:
    M_dict[j]={}

for t in range(2):
    if 41 < t < 401:
        Umin_temp = 0.25
    else:
        Umin_temp = 0.35
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


######  TN PDN Corresponding Relation ####
TN_PDN = {1: 1, 5:26, 4: 25, 10:20, 11: 22, 13: 10, 14:23, 15:24, 20:17, 16:18, 0:-1}
# TN_PDN = {1: 21, 2:20, 4:8, 5:5, 10:3, 11: 6, 13:29, 14:7, 15:4, 20:27, 0:-1}
# TN_PDN = {1: 2,0:-1,4:7, 10:1, 20:24}
# TN_PDN = {1: 1,4:6,10:13,11:16,15:23,20:27,0:-1}


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

c2_1_name = ['c2-1_{}'.format(i) for i in J_plus]
c2_1_direction = 'L'

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

for item in c1_1_name:
    core.write(' {:3}{}\n'.format(c1_1_direction,item))
for item in c1_2_name:
    core.write(' {:3}{}\n'.format(c1_2_direction,item))
for item in c2_0_name:
    core.write(' {:3}{}\n'.format(c2_0_direction,item))
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
        variable_constr_dict[key]['obj'] = alpha *  A_dict[key_index]/1000
    
    #first stage 
    for constr in c1_1_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -M_hat_dict[key_index]
            
    #second stage
    if key_index == 0:
        variable_constr_dict[key][c2_0_name[0]] = 1

    for constr in c2_2_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -M_dict[key_index][0]
    for constr in c2_3_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index_j = int(constr.split("_")[1:][-2])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:

            variable_constr_dict[key][constr] = - total_D_dict[0]
                    #variable_constr_dict[key][constr] = - M
        
        
        



# X variable
for key in variable_name_dict['x']:
    key_index = (int(key.split("_")[-1]))
    variable_constr_dict[key] = {}
    
    #obj   
    if key_index>0:     
        variable_constr_dict[key]['obj'] = alpha *  C_dict[key_index]/1000
    
    #first stage
    for constr in c1_1_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = 1
            
    #second stage
    #dummy
    if key_index == 0:
        variable_constr_dict[key][c2_0_name[1]] = 1
        
    for constr in c2_1_name:
        constr_index = int(constr.split("_")[1:][-1])
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
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
        if key_index == (0,1):
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
    
    variable_constr_dict[key]['obj'] = beta * Gmn * key_k
        
    
    for constr in c1_2_name:
        constr_index =(int(constr.split("_")[-2]),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if (key_m,key_n) == constr_index:

            variable_constr_dict[key][constr] = 1
                

    
    
    for constr in c2_9_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
            variable_constr_dict[key][constr] = -Vmax
            
    
    for constr in c2_10_R_name:
        constr_index =((int(constr.split("_")[-3]),int(constr.split("_")[-2])),int(constr.split("_")[-1]))
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index:
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
            variable_constr_dict[key][constr] = -PMax_dict[constr_index] * key_k
            
    for constr in c2_14_name:
        constr_index =( int(constr.split("_")[1:][-2]) , int(constr.split("_")[1:][-1]) )
        
        #key_index = (int(key.split("_")[-1]))
        if constr_index == key_index[0]:
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
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1
    
    
for name in c1_2_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,1))
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
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1

for name in c2_2_name:
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,0))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,0))
    RHS_count +=1

for name in c2_3_name:

    
    if RHS_count%2 == 0:

        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, - total_D_dict[0] ))
            #core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, - M ))
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
    current_P = P_load_mat[key - 1][0]
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name,current_P))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,current_P))
    RHS_count +=1
    
    
for name in c2_6_name:
    key = int(name.split("_")[1:][-1])
    current_Q = Q_load_mat[key - 1][0]
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
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, 0 ))
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
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, Vmax ))
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
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, PMax_dict[constr_index] ))
    else:
        core.write('{:<20s}   {:>25.5f}\n'.format(name,PMax_dict[constr_index]))
    RHS_count +=1 


for name in c2_14_name:
    constr_index =( int(name.split("_")[1:][-2]) , int(name.split("_")[1:][-1]) )
    if RHS_count%2 == 0:
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, QMax_dict[constr_index] ))
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
        core.write('    {:<20s}{:<20s}   {:>25.5f}  '.format('rhs',name, PMax_dict[0,1] ))
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
    
    if 41 < number_scenario < 401:
        Umin = 0.25
    else:
        Umin = 0.35
    
    
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
                stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,constr ,coef))
        
        for constr in c2_3_name:
            constr_index = constr.split("_")[1:][-1:]

            constr_index_k = int(constr_index[0])
            #key_index = (int(key.split("_")[-1]))
            if key_index == constr_index_k:

                coef = - total_D_dict[i]
                    #coef = -M
                stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( key,constr ,coef))
        
        
                
    # Integer Programming             
    for name in c2_3_name:
        coef = - total_D_dict[i]
            #coef = -M
        stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
    for name in c2_4_name:
        index = int(name.split("_")[1:][-1])
        coef = D_mat[index-1][i] * Demand_Multiplier
        stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
    for name in c2_5_name:
        index = int(name.split("_")[1:][-1])
        coef = P_load_mat[index-1][i]
        stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
    for name in c2_6_name:
        index = int(name.split("_")[1:][-1])
        coef = Q_load_mat[index-1][i]
        stoch.write('    {:<20s}{:<20s}{:>25.5f}\n'.format( 'rhs',name ,coef))
        
stoch.write('ENDATA')


stoch.close()











