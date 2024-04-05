"""
Created on Sun Feb  7 22:43:32 2021

@author: cyril
"""
import pandas as pd
from openpyxl import load_workbook

PDN_resi_nodes = [1,2,22,28,29,30,31,32,17,16,15,12,11,20,19,18,7]
PDN_comm_nodes = [3,4,5,6,8,9,10,13,14,25,26,27,23,24,21]
zero = 0.00001

n = 432
I = list(pd.read_excel('Networks.xlsx','LocationData').values[:,0])
A = list(pd.read_excel('Networks.xlsx','LocationData').values[:,1])
C = list(pd.read_excel('Networks.xlsx','LocationData').values[:,2])

Utility  = pd.read_excel('Utility432.xlsx',index_col=[0,1])
Utility_dict = Utility.to_dict(orient='index')

TN_comm_nodes = [4,5,9,10,11,14,15,22,23,]

J = [1, 4,5,10,11,13,14,15,16,20]
G= 30
H = 2*G
H_0 = 1.5
alpha = 1
beta = 1
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

''' the file reading '''
sol = open('small.sol')

count = 0



''' Read the result for the first stage '''

Z_dict = {}
X_dict = {}
U_dict = {}

for line in sol.readlines():
    count+= 1
    if count == 3:
        obj = float((line.split()[-1]).split('E+')[0])*float((10**float((line.split()[-1]).split('E+')[1])))
    current_list = line.split()[0:3]
    if current_list == []:
        continue
    elif current_list[0] == 'Second-stage':
        break
    elif current_list[0].isdigit() == False:
        continue
    else:
        
        current_value_list = current_list[2].split('+')
        current_value = (float(current_value_list[1][0:-1]))
        
        
        current_variable_list = current_list[1].split('_')
        variable_category = current_variable_list[0]
        if variable_category == 'z':
            current_value = int((float(current_value_list[1][0:-1])))
            current_index = int(current_variable_list[-1])
            Z_dict[current_index] = current_value

        
        
        if variable_category == 'x':
            current_value_list = current_list[2].split('+')
            current_value = 1 * (float(current_value_list[1][0:-1])) * (10**float(current_value_list[-1][-2:]))
            current_index = int(current_variable_list[-1])
            X_dict[current_index] = current_value
            
            
        if variable_category == 'u':
            mn_index = (int(current_variable_list[-3]),int(current_variable_list[-2]))
            k_index = int(current_variable_list[-1])
            if mn_index not in U_dict:
                U_dict[mn_index] = current_value * k_index
            else:
                U_dict[mn_index] += current_value * k_index
                
                
        if variable_category == 'u00':
            current_value_list = current_list[2].split('E')
            
            current_value = (float(current_value_list[0][0:])) * (10**float(current_value_list[-1][0:]))

            #k_index = int(current_variable_list[-1])
            substation += beta * 0.788 * current_value 
        


######## Calculate Cost  #################
for i in J:
    if i in TN_comm_nodes:
        building_cost += theta * alpha*A_dict[i]*Z_dict[i]/1000
        capacity_cost += theta * alpha*C_dict[i]*X_dict[i]/1000
    else:
        building_cost += alpha*A_dict[i]*Z_dict[i]/1000
        capacity_cost += alpha*C_dict[i]*X_dict[i]/1000
    

# for key,value in U_dict.items():
#     key_m = key[0]
#     key_n = key[1]
#     if ((key_m+1) in PDN_resi_nodes) and ((key_n+1) in PDN_resi_nodes): 
#         expanding_cost += beta * Gmn
#     elif ((key_m+1) in PDN_resi_nodes) and ((key_n+1) in PDN_comm_nodes): 
#         expanding_cost += beta * Gmn
#     elif ((key_m+1) in PDN_comm_nodes) and ((key_n+1) in PDN_resi_nodes): 
#         expanding_cost += beta * Gmn
#     else:
#         expanding_cost += beta * Gmn


expanding_cost = sum(U_dict.values())*Gmn*beta

station_cost = building_cost + capacity_cost
total_cost = station_cost + expanding_cost + substation 

print('Objective Value:', obj)
print('Total Cost:', total_cost)
print('TN Cost:', station_cost)
print('Building Cost:',building_cost)
print('Capacity Cost:', capacity_cost)
print('PDN Cost:', substation + expanding_cost)
print('Expanding Cost:', expanding_cost)
print('Substation Cost:', substation)


sol.close()
    
    





''' Read the result for the second stage '''
sol = open('small.sol')



S_dict = {}
Y_dict = {}
#P_dict = {}
#Q_dict = {}
S_total = {}
Y0_dict = {}
Y1_dict = {}


P01_Max = []


current_scenario = 0

min22v = [0,1000]
min23v = [0,1000]

total_utility = 0
total_penalty = 0
unsatisified_utility = 0


total_cars = 0
missed_cars = 0
Unsatisfied_cars = 0

# Y_path = r'C:\Users\cyril\Desktop\Research\iOptimize-win64x86-0.9.8\final\Ysol.xlsx'
# Y_book = load_workbook(Y_path)
# Y_writer = pd.ExcelWriter(Y_path, engine = 'openpyxl')
# Y_writer.book = Y_book



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
        
        # current_sheet = '{}'.format(current_scenario)
        # if current_scenario > 0:
        #     if current_scenario >10:
        #         break
        #     # Write Y
        #     Y_df = pd.DataFrame(data = Y_dict).T
        #     Y_df.to_excel(Y_writer,sheet_name= current_sheet)
        #     Y_writer.save()
        #     continue
    
    
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
                     
        # if variable_category == 'q':
        #     if current_scenario == 370:
        #         # Key of P_dict
        #         origin_index = int(current_variable_list[1])
        #         dest_index = int(current_variable_list[2])
        #         # Value of P
        #         current_value_list = current_list[2].split('+')
        #         # current_value = 30000
        #         current_value = 1 * (float(current_value_list[1][0:-1])) * (10**float(current_value_list[-1][-2:]))
        #                 #     # Put in Dict
        #         if origin_index not in Pmn_Max:
        #             Qmn_Max[(origin_index,dest_index)] = {}
        #             Qmn_Max[(origin_index,dest_index)] = current_value
        #         else:
        #             Qmn_Max[(origin_index,dest_index)] = current_value
                
        
        
        
        
        
        
# print('Average Utility:',  total_penalty/480 + substation + total_cost - obj)
# print('Average Utility:', total_utility/480)
# print('Average Penalty:', total_penalty/480)
# print('Unsatisfied Utility:', unsatisified_utility/480)

# print('Number of Cars Charging:', total_cars/108)
# print('Missed Cars:', missed_cars/108)
# print('Unsatisfied Cars:', Unsatisfied_cars/108)



# print(min22v)
# print(min23v)

print('Satisfied Cars:',total_cars/n - missed_cars/n)
print('Unsatisfied Cars:', Unsatisfied_cars/n + missed_cars/n)

print('Satisfaction: ', total_cost - obj )
print('Sat_Manual:', (total_utility - unsatisified_utility - total_penalty )/n)



''' Find PQmax '''        
# Pmn_df = pd.DataFrame.from_dict(Pmn_Max, orient = 'index')
# Pmn_df.to_excel('Pmn.xlsx')       

# Qmn_df = pd.DataFrame.from_dict(Qmn_Max, orient = 'index')
# Qmn_df.to_excel('Qmn.xlsx')     
    


''' Write Y'''
# Y_df = pd.DataFrame(data = Y_dict).T
# Y_df.to_excel(Y_writer,sheet_name= current_sheet)
# Y_writer.save()
# Y_writer.close()

            

        
        


        
















