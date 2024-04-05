This is the repo for the paper: https://ieeexplore.ieee.org/document/10306294

Our Model is Solved in SMPS format with iOptimize available: https://zbmath.org/software/20377


STEP 1:
Create SMPS files: run the python file (SMPS_startingpoint.py) at each folder. 

STEP 2: 
Input SMPS to the terminal to obtain solution file (.sol). Please adjust the directory according. The following is an example
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Run 74-123-Network:

Adjust your first stage solution after the solution for smaller scenario cases is availble

iOptimize.exe --readmps="F:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final74_123/startingpoints/2/small.mps" --readtim="F:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final74_123/startingpoints/2/small.tim" 
    --readsto="F:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final74_123/startingpoints/2/small.sto" 
    --dllpath="D:\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4

Run 24-33-Networks:
iOptimize.exe --readmps="F:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final24_33/432_3/small.mps" --readtim="F:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final24_33/432_3/small.tim" 
    --readsto="F:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final24_33/432_3/small.sto" 
    --dllpath="D:\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4

  Note: Modify the CPLEX path and version if needed.

STEP 3: 
Read the solution file:
Run read_final.py


   

        
