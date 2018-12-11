
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@ ECHO OFF
rem @ ECHO ON

set STARTTIME=%TIME%
echo          ---------------
echo Start    : %STARTTIME% %0 STARTED
echo          ---------------

: ------------------------------------------------------------

set CURRENT_BASELINE=%1
set CLONE_PATH=%2
SET WORK_PATH=%3
SET Output_Log=%4
set Tbl_N=%5


echo "CURRENT_BASELINE    %CURRENT_BASELINE%"
rem set CURRENT_BASELINE=CDS_4.2_044

set RELEASE_BRANCH_N=%CURRENT_BASELINE:~4,3%
set CURRENT_BASELINE_N=%CURRENT_BASELINE:~8,3%
set RELEASE_BRANCH=cds_%RELEASE_BRANCH_N%
set CURRENT_BASELINE_NO=%RELEASE_BRANCH_N%_%CURRENT_BASELINE_N%

set DB_NN=%CURRENT_BASELINE_N%
set DB_N=db_%RELEASE_BRANCH_N%_%CURRENT_BASELINE_N%

set CDS_PATH=%CLONE_PATH%\cds

set cds_tool=%CDS_PATH%\tools
set tool_genScripts=%cds_tool%\genScripts
set tool_admin=%cds_tool%\admin
set tool_DB=%cds_tool%\DB
set tool_codeCheck=%tool_genScripts%\codeChecks
set TOOL_COMMON=%cds_tool%\common

SET WORK_DRIVE=%WORK_PATH:~0,2%

rem SET SQL3=c:\utils\sqlite-tools-win32\sqlite3.exe
rem SET SQL3=c:\temp\cds_bin\sqlite3.exe 
SET SQL3=c:\Git\ws01\cds\cds_bin\sqlite3.exe 

REM IF NOT EXIST %SQL3% (
REM    copy f:\Objects\cds\bin\sqlite3.exe %SQL3%
REM )

IF EXIST c:\Python26\python.exe (
    SET PYTHON_PATH=c:\Python26\python.exe
)
IF EXIST c:\Python27\python.exe (
    SET PYTHON_PATH=c:\Python27\python.exe
)

SET DB_PATH=%db%

SET Input_Csv_Lnx_BM=%Input_Log_Csv%\Build_Linux_BM_Images_Report.csv 
SET Input_Csv_Lnx_WM=%Input_Log_Csv%\Build_Linux_WM_Images_Report.csv 
SET Input_Csv_Win=%Input_Log_Csv%\Win_Report.csv

SET DEL_OLD_TABLE=Y
SET DB_TABLE=LnxImg

rem SET MODE_PARM_BM="BM"
rem SET MODE_PARM_WM="WM"

::-------------------------------------------------------------------

rem SET Input_Csv_Win=\\Fileril103\dev\Objects\cds\%RELEASE_BRANCH%\logs\%CURRENT_BASELINE%\Win_Report.csv 
rem SET Input_Csv_Lnx_BM=\\Fileril103\dev\Objects\cds\%RELEASE_BRANCH%\logs\%CURRENT_BASELINE%\Build_Linux_BM_Images_Report.csv 
rem SET Input_Csv_Lnx_WM=\\Fileril103\dev\Objects\cds\%RELEASE_BRANCH%\logs\%CURRENT_BASELINE%\Build_Linux_WM_Images_Report.csv 

rem SET Input_Csv_Win=c:\Git\4.2_work\4_customer\Objects\cds\cds_4.2\CDS_4.2_044\Win_Report.csv 
rem SET Input_Csv_Lnx_BM=c:\Git\4.2_work\4_customer\Objects\cds\cds_4.2\CDS_4.2_044\Build_Linux_BM_Images_Report.csv
rem SET Input_Csv_Lnx_WM=c:\Git\4.2_work\4_customer\Objects\cds\cds_4.2\CDS_4.2_044\Build_Linux_WM_Images_Report.csv

rem \swdev\fileril103\Objects\cds\${RELEASE_BRANCH}\logs\${LAST_BASELINE}

SET TEMP_DB=%WORK_PATH%\Build_UT_Analyze
set db2=%TEMP_DB%\Build_UT.db
SET DEL_OLD_TABLE=Y
SET OPTION="all"
SET  XML_PATH=%TEMP_DB%\XML
SET compile_XML_Win=%XML_PATH%\compile_Win.xml
SET compile_XML_BM=%XML_PATH%\compile_Linux_BM.xml
SET compile_XML_WM=%XML_PATH%\compile_Linux_WM.xml

SET compile_err_XML_Win=%XML_PATH%\compile_err_Win.xml
SET compile_err_XML_BM=%XML_PATH%\compile_err_Linux_BM.xml
SET compile_err_XML_WM=%XML_PATH%\compile_err_Linux_WM.xml

SET compile_err_XML=%XML_PATH%\compile_err.xml

SET DB_PATH=%db2%
SET OPTION="all"

rem SET IN_UT_LOG=\\Fileril103\dev\Objects\cds\%RELEASE_BRANCH%\log\%CURRENT_BASELINE%
rem SET IN_UT_LOG=c:\Git\4.2_work\4_customer\Objects\cds\cds_4.2\log\CDS_4.2_044
SET IN_UT_LOG_ERR=\\Fileril103\dev\Objects\cds\%RELEASE_BRANCH%\logs\%CURRENT_BASELINE%
rem SET IN_UT_LOG_ERR=c:\Git\4.2_work\err_44\

SET IN_UT_LOG=\\Fileril103\dev\Objects\cds\%RELEASE_BRANCH%\%CURRENT_BASELINE%

rem f:\Objects\cds\cds_4.2\CDS_4.2_044\automaticImageTesting\logs\.. 

rem SET IN_UT_LOG_32_BM=%IN_UT_LOG%\automaticImageTesting\logs
rem SET IN_UT_LOG_32_WM=%IN_UT_LOG%\linux\WM_images
rem SET IN_UT_LOG_64_WM=%IN_UT_LOG%\linux\WM_images_64_bit
rem 
rem SET OUT_TIME_FILE_BM=%TEMP_DB%\csv\time_BM.csv
rem SET OUT_TIME_FILE_WM=%TEMP_DB%\csv\time_WM.csv
rem set OUT_TIMEOUT_FILE_ALL=%TEMP_DB%\csv\UT_time.csv
rem 
rem SET Board_Img_Test_Cases=%tool_DB%\Board_Img_Test_Cases.csv
rem SET Images_CSV=%tool_DB%\Images.csv
rem 
rem SET CURRENT_UT_XML_WM=%XML_PATH%\UT_WM_all.xml
rem SET CURRENT_UT_XML_BM=%XML_PATH%\UT_BM_all.xml
rem 
rem SET CURRENT_UT_XML_FAIL_WM=%XML_PATH%\UT_WM_fail_only.xml
rem SET CURRENT_UT_XML_FAIL_BM=%XML_PATH%\UT_BM_fail_only.xml

SET OPTION_ALL="all"
SET OPTION_FAIL="fail_only"

SET DB_TABLE_UT=UT
SET DB_TABLE_ERR=compl_err


::======================================================
REM set History_Path=f:\Objects\cds\bin_history
set History_Path=c:\Git\ws01\cds

rem set History_Path=c:\temp\cds_bin_history\6
rem f:\Objects\cds\bin_history\DB\
set current_db=%History_Path%\DB\%CURRENT_BASELINE_N%
set out_dir=%current_db%\Out_Csv
set DB_Dictionary=%out_dir%\DB_Dictionary.csv

set db=%current_db%\%DB_N%.db
rem SET SQL3=c:\utils\sqlite-tools-win32\sqlite3.exe
REM SET SQL3=c:\temp\cds_bin\sqlite3.exe 
REM
REM IF NOT EXIST %SQL3% (
REM    copy f:\Objects\cds\bin\sqlite3.exe %SQL3%
REM )

SET DB_SQL=%db%
SET DB_PATH=%db%

rem SET db=%Admin_Path_DB%\DB_UT_%CURRENT_BASELINE_N%\%DB_N%.db 
rem SET db=%Admin_Path_DB%\XML_%CURRENT_BASELINE_N%\%DB_N%.db 

set Admin_Path=n:\shared\admin\lern_ut4
set Admin_Path_DB=%Admin_Path%\db

rem del %db% 

rem f:\Objects\cds\bin_history\tbl\Common_Tbl_6.xlsx 
SET xlsx=%History_Path%\tbl\Common_Tbl_%Tbl_N%.xlsx
SET xlsx=%History_Path%\tbl\cds_db_0_%Tbl_N%.xlsx


rem SET Input_Log_Csv=%Admin_Path%\log\%CURRENT_BASELINE_N%
rem SET Input_Csv=%Input_Log_Csv%\Build_Linux_BM_Images_Report.csv 
rem SET Input_Csv=%Admin_Path%\log\Win_Report.csv 
rem SET Input_Csv_Lnx_BM=%Input_Log_Csv%\Build_Linux_BM_Images_Report.csv 
rem SET Input_Csv_Lnx_WM=%Input_Log_Csv%\Build_Linux_WM_Images_Report.csv 
rem SET Input_Csv_Win=%Input_Log_Csv%\Win_Report.csv

SET DEL_OLD_TABLE=Y
SET DB_TABLE=LnxImg

SET MODE_PARM_BM="BM"
SET MODE_PARM_WM="WM"


SET DUMP_FILE=%out_dir%\db_dump.dmp

SET DUMP_FILE=%out_dir%\db_dump.dmp
SET DEF_TBL_FILE=%out_dir%\def_tbl.sql




::--------------------------------------------------------------

echo "Tbl_N              =%Tbl_N%"
echo "WORK_DRIVE          %WORK_DRIVE%"
echo "CURRENT_BASELINE    %CURRENT_BASELINE%"
echo "RELEASE_BRANCH_N    %RELEASE_BRANCH_N%"
echo "CURRENT_BASELINE_N  %CURRENT_BASELINE_N%"
echo "CURRENT_BASELINE_NO %CURRENT_BASELINE_NO%"
echo "RELEASE_BRANCH      %RELEASE_BRANCH%"

echo "CLONE_PATH        %CLONE_PATH%"
echo "CDS_PATH         %CDS_PATH%"
echo "DEF_TBL_FILE      %DEF_TBL_FILE%"
echo "PYTHON_PATH       %PYTHON_PATH%"
echo "DB_PATH           %DB_PATH%"
echo "SQL3              %SQL3%"
                          
rem echo "Input_Csv_Lnx_BM  %Input_Csv_Lnx_BM%"
rem echo "Input_Csv_Win     %Input_Csv_Win%"
echo "DEL_OLD_TABLE     %DEL_OLD_TABLE%"
echo "DB_TABLE          %DB_TABLE%"

echo "TEMP_DB=%TEMP_DB%"
rem echo "OUT_TIME_FILE_BM=%OUT_TIME_FILE_BM%"
rem echo "Board_Img_Test_Cases=%Board_Img_Test_Cases%"
rem echo "Images_CSV=%Images_CSV%"
rem 
rem echo "IN_UT_LOG=%IN_UT_LOG%"
rem echo "IN_UT_LOG_32_BM=%IN_UT_LOG_32_BM%"
rem echo "IN_UT_LOG_32_WM=%IN_UT_LOG_32_WM%"
rem echo "IN_UT_LOG_64_WM=%IN_UT_LOG_64_WM%"
rem echo "IN_UT_LOG_ERR=%IN_UT_LOG_ERR%"
rem 
rem echo "OUT_TIME_FILE_WM=%OUT_TIME_FILE_WM%"
rem echo "OUT_TIME_FILE_BM=%OUT_TIME_FILE_BM%"
rem echo "OUT_TIME_FILE_WM=%OUT_TIME_FILE_WM%"
rem echo "OUT_TIMEOUT_FILE_ALL=%OUT_TIMEOUT_FILE_ALL%"

echo "Output_Log=%Output_Log%"

echo "db2             %db2%"
echo "TEMP_DB         %TEMP_DB%"
rem echo "Input_Csv_Win   %Input_Csv_Win%"
rem echo "XML_PATH        %XML_PATH%"
rem echo "compile_XML_Win %compile_XML_Win%"
rem                          
rem echo "compile_XML_BM  %compile_XML_BM%"
rem echo "compile_XML_WM  %compile_XML_WM%"
rem echo "DB_TABLE_ERR    %DB_TABLE_ERR%"

echo DUMP_FILE      %DUMP_FILE%
echo DEF_TBL_FILE   %DEF_TBL_FILE%

echo Tbl_N          %Tbl_N%
echo History_Path   %History_Path%

echo DB_PATH         %DB_PATH% 
echo SQL3           %SQL3%
echo Admin_Path     %Admin_Path%
echo Admin_Path_DB  %Admin_Path_DB%
rem echo Input_Csv_Lnx_BM  %Input_Csv_Lnx_BM%
rem echo Input_Csv_Win  %Input_Csv_Win%
echo DEL_OLD_TABLE  %DEL_OLD_TABLE%
echo DB_TABLE       %DB_TABLE%
echo DB_Dictionary  %DB_Dictionary%

echo xlsx           %xlsx%
echo db             %db%
echo out_dir        %out_dir%
echo DB_SQL         %db% 
echo DB_Dictionary  %DB_Dictionary%
echo DUMP_FILE      %DUMP_FILE%

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

IF EXIST %out_dir% (
    ECHO rd /s /q %out_dir%
    rd /s /q %out_dir%
)
ECHO mkdir %out_dir%
mkdir %out_dir%

echo  "%PYTHON_PATH% %tool_admin%\CDS_xls2db.py %xlsx% %db% %out_dir% %DB_Dictionary%
       %PYTHON_PATH% %tool_admin%\CDS_xls2db.py %xlsx% %db% %out_dir% %DB_Dictionary%

echo %SQL3% %db% .dump to %DUMP_FILE%
     %SQL3% %db% .dump   >%DUMP_FILE%

echo  "%PYTHON_PATH% %tool_admin%\create_def_tbl.py %DUMP_FILE% %DEF_TBL_FILE%
       %PYTHON_PATH% %tool_admin%\create_def_tbl.py %DUMP_FILE% %DEF_TBL_FILE%

:: ::-------------------------------------------------------------------
:: 
:: SET TEMP_DB=c:\temp\DB
:: rem set db2=%current_db%\%DB_N%_2.db
:: set db2=%TEMP_DB%\%DB_N%_2.db
:: 
:: echo db2            %db2%
:: echo TEMP_DB        %TEMP_DB%
:: 
:: IF EXIST %TEMP_DB% (
::     ECHO rd /s /q %TEMP_DB%
::     rd /s /q %TEMP_DB%
:: )
:: ECHO mkdir %TEMP_DB%
:: mkdir %TEMP_DB%
:: 
:: 
:: IF EXIST %db2% (
::     del %db2%
:: )
:: 
:: echo "%SQL3% %db2%  < %tool_DB%\db_dump.dmp"
::       %SQL3% %db2%  < %tool_DB%\db_dump.dmp
:: 


CALL %TOOL_COMMON%\duration.bat %STARTTIME%
