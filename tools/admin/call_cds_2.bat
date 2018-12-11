
@ ECHO OFF
set STARTTIME=%TIME%
echo          ---------------
echo Start    : %STARTTIME% %0
echo          ---------------


:: SET project_name=cpss
:: SET release_number=4.2
:: SET project_number=317
:: SET release_date=1805
:: SET release_YYYY_MM=2018.5
:: SET create_date=180605
:: 
:: SET base_line=cpss_%release_number%
:: SET release_stream=CPSS_%release_number%_%release_date%
:: SET out_base_name=CPSS_UserGuide_API
:: SET out_base_root=c:\Git
:: 
:: SET src_clone_path=%out_base_root%\ws01
:: SET release_clone_path=%out_base_root%\ws01
:: 
:: SET src_cpss_path=%src_clone_path%\cpss
:: SET release_cpss_path=%release_clone_path%\cpss
:: 
:: SET bin_doxygen="c:\Program Files\doxygen\bin\doxygen.exe"
:: SET bin_7z="c:\Program Files\7-Zip\7z.exe"
:: 
:: rem SET in_html_base=\\Fileril103\dev\Objects\cpss\bin_history\UG\CPSS_User_Guide-Responsive_HTML5_LATEST
:: SET in_html_base=\\Fileril103\dev\Objects\cpss\bin_history\UG\Ug_180604\CPSS_User_Guide-Responsive_HTML5
:: rem SET in_html_DXCH=\\Fileril103\dev\Objects\cpss\bin_history\UG\Ug_180604\CPSS_User_Guide-DxCh
:: SET in_html_DXCH=\\Fileril103\dev\Objects\cpss\bin_history\UG\Ug_180604\CPSS_User_Guide-Responsive_HTML5
:: SET in_html_PIPE=\\Fileril103\dev\Objects\cpss\bin_history\UG\Ug_180604\CPSS_User_Guide_PIPE-Responsive_HTML5
:: 
:: SET update_html_path=\\Fileril103\dev\Objects\cpss\bin_history\UG\Update\CPSS_User_Guide
:: SET in_html_base_ug=%in_html_base%\CPSS_User_Guide\
:: rem SET update_html_name=API_Appendix\API_Appendix.htm
:: 
:: SET temp_dir=c:/temp_%release_number%_%project_number%_%create_date%
:: SET create_cust_temp_dxy_bat=%temp_dir%/create_cust_temp_dxy.bat
:: SET create_customer_dxy_bat=%temp_dir%/create_customer_dxy.bat
:: SET create_internal_dxy_bat=%temp_dir%/create_internal_dxy.bat
:: 
:: IF NOT EXIST %temp_dir% (
::     mkdir %temp_dir%
:: )
:: 
:: IF EXIST c:\Python26\python.exe (
::     SET PYTHON_PATH=c:\Python26\python.exe
:: )
:: IF EXIST c:\Python27\python.exe (
::     SET PYTHON_PATH=c:\Python27\python.exe
:: )
:: 
:: rem set CURRENT_BASELINE=CPSS_4.2_148
:: rem set CURRENT_BASELINE=CPSS_4.2_200
:: 
:: set CURRENT_BASELINE_N=%project_number%
:: set CURRENT_BASELINE_NO=%release_number%_%CURRENT_BASELINE_N%
:: set CURRENT_BASELINE=CPSS_%CURRENT_BASELINE_NO%
:: 
:: 
:: set RELEASE_BRANCH_N=%CURRENT_BASELINE:~5,3%
:: set CURRENT_BASELINE_N=%CURRENT_BASELINE:~9,3%
:: set RELEASE_BRANCH=cpss_%RELEASE_BRANCH_N%
:: set CURRENT_BASELINE_NO=%RELEASE_BRANCH_N%_%CURRENT_BASELINE_N%
:: 
:: rem set CLONE_N=w03
:: rem set CLONE_PATH=C:\Git\%CLONE_N%
:: rem set CLONE_PATH=C:\Git\w06
:: set CLONE_PATH=C:\Git\ws01
:: set CPSS_PATH=%CLONE_PATH%\cpss
:: 
:: set RELEASE_BRANCH_N=%CURRENT_BASELINE:~5,3%
:: set CURRENT_BASELINE_N=%CURRENT_BASELINE:~9,3%
:: set RELEASE_BRANCH=cpss_%RELEASE_BRANCH_N%
:: set CURRENT_BASELINE_NO=%RELEASE_BRANCH_N%_%CURRENT_BASELINE_N%
:: 
:: : -------------------------------------------------
:: SET CPSS_PATH=%CLONE_PATH%\cpss
:: SET cpss_tool=%CPSS_PATH%\tools
:: SET tool_genScripts=%cpss_tool%\genScripts
:: SET tool_codeCheck=%tool_genScripts%\codeChecks
:: SET TOOL_COMMON=%cpss_tool%\common
:: set SCRIPT_DIR=%CPSS_PATH%\tools\admin
:: set tool_admin=%cpss_tool%\admin
:: set tool_DoxyGen=%cpss_tool%\DoxyGen\ug
:: : -------------------------------------------------
:: 
:: SET WORK_PATH=%CD%
:: SET WORK_DRIVE=%WORK_PATH:~0,2%
:: SET LOG_DIR=%WORK_PATH%\Logs_%release_number%_%project_number%_%create_date%
:: 
:: IF NOT EXIST %LOG_DIR% (
::     mkdir %LOG_DIR%
:: )
:: 
:: : -------------------------------------------------
:: :: %WORK_DRIVE%
:: 
:: echo "-------------------"
:: echo "  The parameters are:"
:: echo "-------------------"
:: echo "RELEASE_BRANCH      = %RELEASE_BRANCH%"
:: echo "CURRENT_BASELINE    = %CURRENT_BASELINE%"
:: echo "CURRENT_BASELINE_NO = %CURRENT_BASELINE_NO%"
:: echo "LOG_DIR             = %LOG_DIR%"
:: echo "-------------------"
:: 
:: rem SET CONF_DOXY4UG=%WORK_PATH%\conf_doxy4ug.ini
:: rem SET CONF_DOXY4UG=%tool_DoxyGen%\conf_doxy4ug_204.ini
:: rem SET CONF_DOXY4UG=%tool_DoxyGen%\conf_doxy4ug_all_293.ini
:: rem SET CONF_DOXY4UG=%tool_DoxyGen%\conf_doxy4ug_DXCH_293.ini
:: 
:: rem SET CONF_DOXY4UG=%tool_DoxyGen%\conf_doxy4ug_family_293.ini
:: rem SET CONF_DOXY4UG=%tool_DoxyGen%\conf_doxy4ug_family_309_1.json
:: 
:: rem SET CONF_DOXY4UG=%tool_DoxyGen%\conf_doxy4ug_family.json
:: 
:: rem SET CONF_DOXY4UG=%tool_DoxyGen%\conf_doxy4ug0604_family_317_1.json
:: 
:: 
:: 
:: 
:: rem echo  "%PYTHON_PATH% %tool_DoxyGen%\main_ug_api.py %CONF_D_XML_2_DB% >%LOG_DIR%\main_ug_api.txt"
:: rem        %PYTHON_PATH% %tool_DoxyGen%\main_ug_api.py %CONF_D_XML_2_DB% >%LOG_DIR%\main_ug_api_int2.txt  



:: SET CONF_DOXY4UG=%tool_DoxyGen%\conf_cds_1.json
:: ECHO "CONF_DOXY4UG=%CONF_DOXY4UG%
:: SET CONF_D_XML_2_DB=%CONF_DOXY4UG%


echo  "%PYTHON_PATH% %tool_DoxyGen%\main_cds_5.py %CONF_D_XML_2_DB% >%LOG_DIR%\main_cds_1.txt"
       %PYTHON_PATH% %tool_DoxyGen%\main_cds_5.py %CONF_D_XML_2_DB% 

       rem >%LOG_DIR%\main_cds_1.txt  

CALL %TOOL_COMMON%\duration.bat %STARTTIME%
