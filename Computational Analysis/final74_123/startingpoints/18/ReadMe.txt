[Windows]
	
  1. Open a Command Propmp window (start->cmd, see:
  http://windows.microsoft.com/en-us/windows-vista/open-a-command-prompt-window) 

  2. In the command console, go to the folder
	cd /d D:\iOptimize-win64x86-0.9.8\bin 
		
  3. To run the code, use:
	

Famer:
  iOptimize.exe --readmps=../final/farmer.mps --readtim=../final/farmer.tim 
    --readsto=../final/farmer.sto 
    --dllpath="C:\Program Files\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4
small:
  iOptimize.exe --readmps="G:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final123/small.mps" --readtim="G:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final123/small.tim" 
    --readsto="G:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final123/small.sto" 
    --dllpath="D:\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4	


  iOptimize.exe --readmps="G:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final2/small.mps" --readtim="G:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final2/small.tim" 
    --readsto="G:\My Drive\Charging Station Project\iOptimize-win64x86-0.9.8/final2/small.sto" 
    --dllpath="D:\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4

  iOptimize.exe --readmps=../final2/small.mps --readtim=../final2/small.tim 
    --readsto=../final2/small.sto 
    --dllpath="D:\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4
example:
  iOptimize.exe --readmps=../final/example.mps --readtim=../final/example.tim 
    --readsto=../final/example.sto 
    --dllpath="C:\Program Files\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4

Mini:
  iOptimize.exe --readmps=../final/example.mps --readtim=../final/example.tim 
    --readsto=../final/example.sto 
    --dllpath="C:\Program Files\IBM\ILOG\CPLEX_Studio1210\cplex\bin\x64_win64"
    --dllname=cplex12100.dll -t4

   
  Note: Modify the CPLEX path and version if needed.
        
