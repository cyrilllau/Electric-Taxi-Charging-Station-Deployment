"""
Created on Sun Feb  7 22:43:32 2021

@author: cyril
"""
import pandas as pd
from openpyxl import load_workbook

PDN_resi_nodes = [1,2,22,28,29,30,31,32,17,16,15,12,11,20,19,18,7]
PDN_comm_nodes = [3,4,5,6,8,9,10,13,14,25,26,27,23,24,21]
zero = 0.00001

number_scenario = 108
D_mat = pd.read_excel('demand108.xlsx').values[:,1: number_scenario + 1][0:]
Demand_Multiplier = 2
I = list(pd.read_excel('Networks.xlsx','LocationData').values[:,0])
A = list(pd.read_excel('Networks.xlsx','LocationData').values[:,1])
C = list(pd.read_excel('Networks.xlsx','LocationData').values[:,2])

Utility  = pd.read_excel('utility108.xlsx',index_col=[0,1])
Utility_dict = Utility.to_dict(orient='index')

TN_comm_nodes = [4,5,9,10,11,14,15,22,23,]

J = [1, 4,5,10,11,13,14,15,16,20]
J_plus = [0,1, 4,5,10,11,13,14,15,16,20]
G= 30
H = 2*G
H_0 = 1.5
alpha = 1
beta = 0.5
theta = 1

# Create the dictionary
A_dict = {}
for key in I:
    A_dict[key] = A[I.index(key)]
C_dict = {}
for key in I:
    C_dict[key] = C[I.index(key)]

obj = 0
total_cost = 0
station_cost = 0
building_cost = 0
capacity_cost = 0
expanding_cost = 0 
substation = 0

Gmn = 300

count = 0


''' Read the result for the second stage '''
sol = open('delta1.sol')



S_dict = {}
Y_dict = {}
#P_dict = {}
#Q_dict = {}
S_total = {}
Y0_dict = {}  #Odds of unsat/sat
Y1_dict = {}  #Sat


P01_Max = []


current_scenario = 0

S_dict[current_scenario] = {}
Y_dict[current_scenario] = {}



min22v = [0,1000]
min23v = [0,1000]

total_utility = 0
total_penalty = 0
unsatisified_utility = 0


total_cars = 0
missed_cars = 0
Unsatisfied_cars = 0


for line in sol.readlines()[count:]:
    current_list = line.split()
    current_sheet = '{}'.format(current_scenario)
    #print(line)
    if current_list == []:
        continue
    
    
    #########################################################
    # If we want to output all result, we should do it here #
    #########################################################
    
    elif current_list[0] == 'Second-stage':
        current_scenario = int(current_list[-1])
        S_total[current_scenario] = 0
        S_dict[current_scenario] = {}
        Y_dict[current_scenario] = {}

    
    
    elif current_list[0].isdigit() == False:
        continue
    else:
        #current_list = current_list[1:3]
        current_variable_list = current_list[1].split('_')
        variable_category = current_variable_list[0]
        
        
        if variable_category == 'y':
            # Key of Y_dict
            origin_index = int(current_variable_list[1])
            dest_index = int(current_variable_list[2])
            
            # Value of Y_dict
            current_value_list = current_list[2].split('E')
            current_value = 1 * (float(current_value_list[0][0:])) * (10**float(current_value_list[-1][0:]))
            
            Y_dict[current_scenario][(origin_index,dest_index)] = current_value
            
            # Put in Dict
            # if origin_index not in Y_dict:
            #     Y_dict[origin_index] = {}
            #     Y_dict[origin_index][dest_index] = current_value
            # else:
            #     Y_dict[origin_index][dest_index] = current_value
                
            if dest_index != 0:    
                total_utility += G * current_value * Utility_dict[(origin_index,dest_index)][current_scenario]  
                total_cars += current_value
                
        if variable_category == 's':
            # Value of S
            current_index = int(current_variable_list[1])
            current_value_list = current_list[2].split('E')
            
            current_value = (float(current_value_list[0][0:])) * (10**float(current_value_list[-1][0:]))
            
            
            S_total[current_scenario] = current_value
            
            if current_index == 0:
                unsatisified_utility += current_value * H_0 * G
                Unsatisfied_cars += current_value
            
            if current_index >= 1:
                total_penalty += current_value * H
                S_dict[current_scenario][current_index] = current_value 
                missed_cars += current_value


        if variable_category == 'v':
            current_index = int(current_variable_list[1])
            current_value_list = current_list[2].split('E')
            current_value = (float(current_value_list[0][0:])) * (10**float(current_value_list[-1][0:]))
            if current_index == 22:
                if current_value < min22v[1]:
                    min22v = [current_scenario,current_value]
            if current_index == 23:
                if current_value < min23v[1]:
                    min23v = [current_scenario,current_value]
                    
            
            
        if variable_category == 'p':
             origin_index = int(current_variable_list[1])
             dest_index = int(current_variable_list[2])
             current_value_list = current_list[2].split('+')
             current_value = 1 * (float(current_value_list[1][0:-1])) * (10**float(current_value_list[-1][-2:]))
             if origin_index ==0:
                 if dest_index == 1:
                     P01_Max.append(current_value)
                     
                
        

penalty_origin = {} #where the penalty comes from

for t in range(108): 
    penalty_origin[t] = {}
    for j in J:
        penalty_origin[t][j] = []
        if S_dict[t][j]>0:
            for i in I:
                if Y_dict[t][(i,j)]>0:
                    penalty_origin[t][j].append(i)


penalty_origin_demand = {}
for t in range(108): 
    penalty_origin_demand[t]= {}
    for j in J:
        penalty_origin_demand[t][j] = sum(Demand_Multiplier* D_mat[i-1,t] for i in penalty_origin[t][j])

ratio_eachtime = {}

total_sat_test = 0
total_cars = 0
total_p = 0


#for t in range(108):
    

S_total_dict2 = {}
for j in J:
    S_total_dict2[j] = 0

for t in range(108):
    ratio_eachtime[t] = {}
    Y0_dict[t] ={}
    Y1_dict[t] ={}
    for i in I:
        current_sat = 0
        current_pen = 0
        for j in J_plus:
            if j > 0:
                current_sat += G * Y_dict[t][(i,j)] * Utility_dict[(i,j)][t]
                total_sat_test += G * Y_dict[t][(i,j)] * Utility_dict[(i,j)][t]
                total_cars += Y_dict[t][(i,j)] 
                if S_dict[t][j]>0.1:
                    if Y_dict[t][(i,j)]>0:
                        current_pen += Demand_Multiplier* D_mat[i-1,t]/ penalty_origin_demand[t][j] * H * S_dict[t][j]
                        total_p += Demand_Multiplier* D_mat[i-1,t]/ penalty_origin_demand[t][j]*S_dict[t][j]
                        S_total_dict2[j] += Demand_Multiplier* D_mat[i-1,t]/ penalty_origin_demand[t][j]*S_dict[t][j]
            else:
                current_pen += H_0 * G*Y_dict[t][(i,j)]
                total_cars += Y_dict[t][(i,j)] 
                total_p += Y_dict[t][(i,j)]
                
        Y0_dict[t][i] = current_sat
        Y1_dict[t][i] = current_pen



# for t in range(108):
#     for j in J:
#         if S_dict[t][j]>0.1:
#             for i in I:
#                 if Y_dict[t][(i,j)]>0:
#                 S_total_dict2[j] += S_dict[t][j]
        
            



S_total_dict = {}
for j in J:
    S_total_dict[j] = 0
    for t in range(108):
        S_total_dict[j] += S_dict[t][j]





                    
LT_Y0 = {}
LT_Y1 = {}
Districts = {'ED':[10,16,7,8,9,17,18], 'ND':[1,2,3,4,5,6],'SD':[13,19,20,21,22,23,24], 
             'WD':[11,12,14,15]   }
for i in I:
    current_s = sum([Y0_dict[t][i] for t in range(108)])/108
    current_u = sum([Y1_dict[t][i] for t in range(108)])/108
    LT_Y0[i] = current_s
    LT_Y1[i] = current_u

LT_Y0_D = {}
LT_Y1_D = {}

for d in Districts.keys():
    LT_Y0_D[d] = sum([LT_Y0[i] for i in Districts[d]])
    LT_Y1_D[d] = sum([LT_Y1[i] for i in Districts[d]])
    
ratio_D = {}
for d in Districts.keys():
    ratio_D[d] = LT_Y0_D[d]/LT_Y1_D[d]
    
    
net_SAT = {}
for d in Districts.keys():
    net_SAT[d] = LT_Y0_D[d]-LT_Y1_D[d]


print("SAT:",LT_Y0_D)
print("Penalty:",LT_Y1_D)
print('Ratio:', ratio_D)

print('Check Utility:', sum(LT_Y0_D.values()))
print('Check Penalty:', sum(LT_Y1_D.values()))



print()
print()
print('NetSAT:', net_SAT)












