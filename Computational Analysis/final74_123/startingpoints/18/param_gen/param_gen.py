# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 23:04:40 2020

@author: lusha
"""

import pandas as pd, numpy as np, matplotlib.pyplot as plt

if __name__ == '__main__':  
    
    
    '''Create Container to store'''
    P_load_dict = {}
    Q_load_dict = {}
    utility_dict = {}
    D_dict = {}
    
    
    '''generating PDN load'''

    
    cols = ['node','PL','QL']
    load_df = pd.read_csv('DNdata_org.txt', sep="\t", names = cols, skiprows=()ws = 1, header=None)
    #print(load_df)
    
    resi_nodes = [1,2,22,28,29,30,31,32,17,16,15,12,11,20,19,18,7]
    comm_nodes = [3,4,5,6,8,9,10,13,14,25,26,27,23,24,21]
    
    cols = ['resi_power']
    resi_df = pd.read_csv('DN_resid_profile.txt', sep="\t", names = cols, header=None)
    #print(resi_df)
    resi_base = float(resi_df['resi_power'][0])
    for i in range(len(resi_df)):
        resi_df['resi_power'][i] = float(resi_df['resi_power'][i])/resi_base
    #print(resi_df)
    resi_df.plot()
    
    cols =['comm_power']
    comms_df = pd.read_csv('DN_commer_profile.txt', sep="\t", names = cols, header=None)
    #print(comms_df)
    comm_base = float(comms_df['comm_power'][0])
    for i in range(len(comms_df)):
        comms_df['comm_power'][i] = float(comms_df['comm_power'][i])/comm_base
    #print(comms_df)
    comms_df.plot()
    
    OutputFile = open("output_param.txt", "w+")
    for t in range(24):
        if  6 < t < 22:
            num_sc = 6
        else:
            num_sc = 2
        
        
        OutputFile.write("t = "+str(t)+"\n")
        for node in resi_nodes:
            mu_p = load_df['PL'][node] * resi_df['resi_power'][t]*0.2
            sigma = mu_p * 0.1
            s = np.random.normal(mu_p, sigma, num_sc)
            OutputFile.write("Node " + str(node) + " PL scenarios: " + str(s) + "\n")
            if node not in P_load_dict:
                P_load_dict[node] = s
            else:
                P_load_dict[node] = np.concatenate((P_load_dict[node], s), axis=None)
            
            
            
            mu_q = load_df['QL'][node] * resi_df['resi_power'][t]*0.2
            sigma = mu_q*0.1
            s = np.random.normal(mu_q, sigma, num_sc)
            OutputFile.write("Node " + str(node) + " QL scenarios: " + str(s) + "\n")
            
            if node not in Q_load_dict:
                Q_load_dict[node] = s
            else:
                Q_load_dict[node] = np.concatenate((Q_load_dict[node], s), axis=None)
            
            
        for node in comm_nodes:
            mu_p = load_df['PL'][node] * comms_df['comm_power'][t]*0.2
            sigma = mu_p*0.1
            s = np.random.normal(mu_p, sigma, num_sc)
            OutputFile.write("Node " + str(node) + " PL scenarios: " + str(s) + "\n")
            
            if node not in P_load_dict:
                P_load_dict[node] = s
            else:
                P_load_dict[node] = np.concatenate((P_load_dict[node], s), axis=None)
                
                
            mu_q = load_df['QL'][node] * comms_df['comm_power'][t]*0.2
            sigma = mu_q*0.1
            s = np.random.normal(mu_q, sigma, num_sc)
            OutputFile.write("Node " + str(node) + " QL scenarios: " + str(s) + "\n")
            
            if node not in Q_load_dict:
                Q_load_dict[node] = s
            else:
                Q_load_dict[node] = np.concatenate((Q_load_dict[node], s), axis=None)
            
        OutputFile.write("\n")
        
        
    ''''''''''''''''''''''''''''''''''''
    '''generating TN drive time  Utility'''
    ''''''''''''''''''''''''''''''
    
    b = 0.6
    c = 0.024 
    #c= 0     # FreeTN
    
    #distance = pd.read_excel("ShortestDistance.xls")
    resi_nodes = [1,2,3,4,5,6,11,12,13,14,15,19,20,21,22,23,24]
    comm_nodes = [7,8,9,10,16,17,18]
    
    '''Shixin import distance here'''
    ############################################
    distance = pd.read_excel("ShortestDistance.xlsx").values[:,:]
    #distance_dict = distance_mat.to_dict()
    node_str = list(distance[:,0])
    nodes = []
    for i in node_str:
        first = i.replace('(','')
        second = first.replace(")",'')
        third = second.replace(' ','')
        temp = third.split(',')
        temp_node = (int(temp[0]),int(temp[1]))
        nodes.append(temp_node)
    shortest = list(distance[:,1])
    distance_dict = {}
    for i in range(len(node_str)):
        distance_dict[nodes[i]] = shortest[i]
    ###############################################
    
    
    
    travel_time_base = {}
    origin = 0
    TNfile = open('SiouxFalls_trips.tntp.txt','r')
    lines = TNfile.readlines()
    for line in lines:
        if line.startswith("Origin"):
            origin = int(line.split()[1])
            continue
        if origin:
            des_pairs = line.split(";")
            for des_pair in des_pairs:
                if not des_pair.isspace():
                    des = int(des_pair.split(":")[0])
                    t = float(des_pair.split(":")[1])
                    travel_time_base[(origin, des)] = t
                    

    #print(travel_time_base)
    
    cols = ['time','traffic time']
    resi_comm_df = pd.read_csv('resi_comm_traffic_profile.txt', sep="\t", names = cols, header=None)
    resi_comm_df['traffic time'] = resi_comm_df['traffic time'].astype(float)
    for i in range(len(resi_comm_df)):
        resi_comm_df['traffic time'][i] = resi_comm_df['traffic time'][i]/100
    #print(resi_comm_df)
    resi_comm_df.plot(x='time',y='traffic time')
    
    
    cols = ['time','traffic time']
    comm_res_df = pd.read_csv('comm_resi_traffic_profile.txt', sep="\t", names = cols, header=None)
    comm_res_df['traffic time'] = comm_res_df['traffic time'].astype(float)
    for i in range(len(comm_res_df)):
        comm_res_df['traffic time'][i] = comm_res_df['traffic time'][i]/100
    #print(comm_res_df)
    comm_res_df.plot(x='time',y='traffic time')
    
    
    time_mult = {0:1,1:0.9,2:0.8,3:0.8,4:0.9,5:1,6:1.1,7:1.2,8:1.3,9:1.4,10:1.4,11:1.3,
                 12:1.3,13:1.2,14:1.2,15:1.2,16:1.3,17:1.4,18:1.5,19:1.5,20:1.4,21:1.3,22:1.2,23:1.1}
    
    
    for t in range(24):
        if  6<t<22:
            num_sc = 6
        else:
            num_sc = 2
        OutputFile.write("t = "+str(t)+"\n")
        for origin in resi_nodes:
            for des in resi_nodes:
                
                current_distance = distance_dict[(origin,des)]
                # mu_t = 10000000 * current_distance/(3000- travel_time_base[(origin, des)]) 
                
                if current_distance == 0:
                    s = np.array([0]* num_sc)
                else:
                
                    #mu_t = travel_time_base[(origin, des)]
                    
                    #mu_t =500000 * current_distance/(100000- mu_t)
                    mu_t =4* current_distance * time_mult[t] *(1/(1- travel_time_base[(origin, des)]/1000000))
                    sigma = mu_t*0.2
                    s = np.random.normal(mu_t, sigma, num_sc)
                    
                OutputFile.write("Origin " + str(origin) + " Des: " + str(des) + " traffic time: " + str(s) + "\n")
                
                
                p = np.random.normal(0.121, 0.121*0.01, num_sc)
                
                u = np.exp(-s*c - b*p)
                current = (origin, des)
                if current not in utility_dict:
                    utility_dict[current] = u
                else:
                    utility_dict[current] = np.concatenate((utility_dict[current], u), axis=None)
                
        
        
        
        
        for origin in resi_nodes:
            for des in comm_nodes:
                
                current_distance = distance_dict[(origin,des)]
                # mu_t = 10000000 *current_distance/(3000- travel_time_base[(origin, des)])
                # mu_t = mu_t  * resi_comm_df["traffic time"][t]
                if current_distance == 0:
                    s = np.array([0]*num_sc)
            
                
                else:
                   # mu_t = travel_time_base[(origin, des)]  * resi_comm_df["traffic time"][t]
                    #mu_t =500000 * current_distance/(100000- mu_t)
                    mu_t = 4* current_distance * time_mult[t]*(1/(1- travel_time_base[(origin, des)]/1000000))
                    print(mu_t)
                    sigma = mu_t*0.2
                    s = np.random.normal(mu_t, sigma, num_sc)
                OutputFile.write("Origin " + str(origin) + " Des: " + str(des) + " traffic time: " + str(s) + "\n")
                
                
                p = np.random.normal(0.1827, 0.1827*0.01, num_sc)
                u = np.exp(-s*c - b*p)
                current = (origin, des)
                if current not in utility_dict:
                    utility_dict[current] = u
                else:
                    utility_dict[current] = np.concatenate((utility_dict[current], u), axis=None)
                    
        for origin in comm_nodes:
            for des in comm_nodes:
                
                
                current_distance = distance_dict[(origin,des)]
                # mu_t = 10000000 *current_distance/(3000- travel_time_base[(origin, des)])
                # mu_t =  mu_t *2
                
                if current_distance == 0:
                    s = np.array([0]* num_sc)
                else:
                    #mu_t =  travel_time_base[(origin, des)] *2
                
                    #mu_t =500000 * current_distance/(100000- mu_t)
                    mu_t =4* current_distance * time_mult[t]*(1/(1- travel_time_base[(origin, des)]/1000000))

                    
                    sigma = mu_t*0.2
                    s = np.random.normal(mu_t, sigma, num_sc)
                OutputFile.write("Origin " + str(origin) + " Des: " + str(des) + " traffic time: " + str(s) + "\n")
                
                p = np.random.normal(0.1827, 0.1827*0.01, num_sc)
                u = np.exp(-s*c - b*p)
                current = (origin, des)
                if current not in utility_dict:
                    utility_dict[current] = u
                else:
                    utility_dict[current] = np.concatenate((utility_dict[current], u), axis=None)
                
                
        for origin in comm_nodes:
            for des in resi_nodes:
                
                current_distance = distance_dict[(origin,des)]
                
                
                if current_distance == 0:
                    s = np.array([0]*num_sc)
                else:
                    #mu_t = travel_time_base[(origin, des)]  * comm_res_df["traffic time"][t]
                    #mu_t =500000 * current_distance/(100000- mu_t)
                    mu_t =4* current_distance * time_mult[t]*(1/(1- travel_time_base[(origin, des)]/1000000))
                    sigma = mu_t*0.2
                    s = np.random.normal(mu_t, sigma, num_sc)
                OutputFile.write("Origin " + str(origin) + " Des: " + str(des) + " traffic time: " + str(s) + "\n")
                
                p = np.random.normal(0.121, 0.121*0.01, num_sc)
                u = np.exp(-s*c - b*p)
                current = (origin, des)
                if current not in utility_dict:
                    utility_dict[current] = u
                else:
                    utility_dict[current] = np.concatenate((utility_dict[current], u), axis=None)
        OutputFile.write("\n")
    OutputFile.close()
    
    
    
    
    ''''''''''''''''''''''''''''''
    '''generating TN drive time'''
    ''''''''''''''''''''''''''''''
    
    
    total_outflow = {}
    for key, value in travel_time_base.items():
        current_origin = key[0]
        if current_origin not in total_outflow:
            total_outflow[current_origin] = value
        else:
            total_outflow[current_origin] += value
            
    relative_demand = {}
    entire_outflow = sum(total_outflow.values())
    for key,value in total_outflow.items():
        relative_demand[key] = value/entire_outflow
        
        

    cols = ['time','demand']
    demand_df = pd.read_csv('demand_pattern.txt', sep="\t", names = cols,header=None)
    demand_base = list(demand_df["demand"])
    
    
    
    
    for t in range(24):
        if  6<t<22:
            num_sc = 6
        else:
            num_sc = 2
        for i in range(24):
            mu_d = demand_base[t]*relative_demand[i+1]
            sigma = mu_d*0.2
            s = np.round(np.random.normal(mu_d, sigma, num_sc))
            node = i+1
            if node not in D_dict:
                D_dict[node] = s
            else:
                D_dict[node] = np.concatenate((D_dict[node], s), axis=None)
        
        
    
    
    
    
    
    
    
    import collections
    
    P_df = pd.DataFrame(data=collections.OrderedDict(sorted(P_load_dict.items()))).T
    P_df.to_excel('Pload.xlsx')
    Q_df = pd.DataFrame(data=collections.OrderedDict(sorted(Q_load_dict.items()))).T
    Q_df.to_excel('Qload.xlsx')
    U_df = pd.DataFrame(data = utility_dict).T
    U_df.to_csv('Utility.csv')
    D_df = pd.DataFrame(data=D_dict).T
    D_df.to_excel('Demand.xlsx')
    
    
    