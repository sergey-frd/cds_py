@ ECHO OFF
set STARTTIME=%TIME%
echo          ---------------
echo Start    : %STARTTIME% %0
echo          ---------------



set CURRENT_BASELINE=CSD_0.3_009
set Tbl_N=09

set CLONE_PATH=C:\Git\ws01


set RELEASE_BRANCH_N=%CURRENT_BASELINE:~4,3%
set CURRENT_BASELINE_N=%CURRENT_BASELINE:~8,3%
set RELEASE_BRANCH=cds_%RELEASE_BRANCH_N%
set CURRENT_BASELINE_NO=%RELEASE_BRANCH_N%_%CURRENT_BASELINE_N%

rem set CLONE_N=w03
rem set CLONE_PATH=C:\Git\%CLONE_N%
set CLONE_PATH=C:\Git\ws01
set CDS_PATH=%CLONE_PATH%\cds
: ------------------------------------------------------

: -------------------------------------------------
SET CDS_PATH=%CLONE_PATH%\cds
SET cds_tool=%CDS_PATH%\tools
SET tool_genScripts=%cds_tool%\genScripts
SET tool_codeCheck=%tool_genScripts%\codeChecks
SET TOOL_COMMON=%cds_tool%\common
set SCRIPT_DIR=%CDS_PATH%\tools\admin
set tool_admin=%cds_tool%\admin
set tool_gen_db=%cds_tool%\gen_db
: -------------------------------------------------

IF EXIST c:\Python26\python.exe (
    SET PYTHON_PATH=c:\Python26\python.exe
)
IF EXIST c:\Python27\python.exe (
    SET PYTHON_PATH=c:\Python27\python.exe
)

rem SET WORK_PATH=%CD%
SET WORK_PATH=%CLONE_PATH%\work

echo "CURRENT_BASELINE    %CURRENT_BASELINE%"
echo "RELEASE_BRANCH_N    %RELEASE_BRANCH_N%"
echo "CURRENT_BASELINE_N  %CURRENT_BASELINE_N%"
echo "CURRENT_BASELINE_NO %CURRENT_BASELINE_NO%"
echo "RELEASE_BRANCH      %RELEASE_BRANCH%"
rem SET PATH=c:\Program Files (x86)\Git\bin;C:\Python27;%PATH%.

rem !!! SET Output_Log=\\Fileril103\dev\Objects\cpss\%RELEASE_BRANCH%\logs\%CURRENT_BASELINE%
SET Output_Log=%CLONE_PATH%\work\%RELEASE_BRANCH%\logs\%CURRENT_BASELINE%
SET Output_Log_Txt=%CLONE_PATH%\work\%RELEASE_BRANCH%\logs\%CURRENT_BASELINE%\run_CSD_xls2csv_%CURRENT_BASELINE%.txt

ECHO "CLONE_PATH=%CLONE_PATH%"
ECHO "WORK_PATH=%WORK_PATH%"
ECHO "Output_Log=%Output_Log%"
ECHO "Output_Log_Txt=%Output_Log_Txt%"
ECHO "Tbl_N=%Tbl_N%"

IF NOT EXIST %Output_Log% (
    mkdir %Output_Log%
)

:: SET LOG_DIR=%WORK_PATH%\Logs_%release_number%_%project_number%_%create_date%
:: 
:: IF NOT EXIST %LOG_DIR% (
::     mkdir %LOG_DIR%
:: )

: ------------------------------------------------------------
SET CONF_GEN_DB=%tool_gen_db%\gen_db_0.json
ECHO "CONF_GEN_DB=%CONF_GEN_DB%"


REM echo  "%PYTHON_PATH% %tool_gen_db%\cdb_gen_db.py %CONF_GEN_DB% >%Output_Log%\cdb_gen_db.txt"
REM       %PYTHON_PATH% %tool_gen_db%\cdb_gen_db.py %CONF_GEN_DB%  
       rem >%Output_Log%\cdb_gen_db.txt  


echo  "%PYTHON_PATH% %tool_gen_db%\cdb_plan.py %CONF_GEN_DB% >%Output_Log%\cdb_gen_db.txt"
       %PYTHON_PATH% %tool_gen_db%\cdb_plan.py %CONF_GEN_DB%  
       rem >%Output_Log%\cdb_plan.txt  


:: SET CONF_CDS_1=%tool_gen_db%\conf_cds_1.json
:: ECHO "CONF_CDS_1=%CONF_CDS_1%"


::echo  "%PYTHON_PATH% %tool_gen_db%\main_cds_5.py %CONF_GEN_DB% >%LOG_DIR%\main_cds_1.txt"
::       %PYTHON_PATH% %tool_gen_db%\main_cds_5.py %CONF_GEN_DB% 

CALL %TOOL_COMMON%\duration.bat %STARTTIME%
