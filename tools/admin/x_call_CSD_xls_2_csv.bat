ECHO OFF


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

SET WORK_PATH=%CD%

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

: ------------------------------------------------------------
ECHO "CALL %CDS_PATH%\tools\admin\run_CSD_xls2csv.bat %CURRENT_BASELINE% %CLONE_PATH% %WORK_PATH%  %Output_Log%  %Tbl_N% => %Output_Log_Txt% 2>&1"
      CALL %CDS_PATH%\tools\admin\run_CSD_xls2csv.bat %CURRENT_BASELINE% %CLONE_PATH% %WORK_PATH%  %Output_Log%  %Tbl_N%  


      REM >%Output_Log_Txt% 2>&1


