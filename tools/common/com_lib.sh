#!/bin/bash

#-------------------------------------
function file_exists {
    if [[ -f "$1" ]]; then
        return 0
    fi
    return 1
}
#-------------------------------------
function file_not_exists {
    if [[ -f "$1" ]]; then
        return 1
    fi
    return 0
}

#-------------------------------------
function directory_exists {
    if [[ -d "$1" ]]; then
        return 0
    fi
    return 1
}

#-------------------------------------
function directory_not_exists {
    if [[ -d "$1" ]]; then
        return 1
    fi
    return 0
}

#-------------------------------------
function create_directory {
    #echo "`date +%T` create_directory $1"
    if directory_exists $1
    then
        #echo  "rm -rf $1 exists."
        I rm -rf $1
    fi 
    #echo "`date +%T` create_directory $1"
    I mkdir -p $1

    return 1
}

#-------------------------------------
function create_directory_1 {
    #echo "`date +%T` create_directory_1 $1"
    if directory_exists $1
    then
        echo  "rmdir $1 exists."
        rm -rf $1
    fi 
    echo "`date +%T` create_directory_1 $1"
    mkdir $1
    return 1
}


#-------------------------------------
function delete_directory {
    #echo "`date +%T` delete_directory $1"
    if directory_exists $1
    then
        #echo  "$1 exists."
        echo "`date +%T` delete_directory $1"
        rm -rf $1
    fi 
    return 1
}

#-------------------------------------
function delete_directory_1 {
    #echo "`date +%T` delete_directory $1"
    if directory_exists $1
    then
        #echo  "$1 exists."
        echo "`date +%T` delete_directory $1"
        rmdir $1
    fi 
    return 1
}


#-------------------------------------
function delete_file {
    #echo "`date +%T` delete_file $1"
    if file_exists $1
    then
        #echo  "$1 exists."
        #echo "`date +%T` delete_file $1"
        rm -f $1
    fi 
    return 1
}

#-------------------------------------

function unpack_dir () 
{
    if [ -f  $2 ]
    then
        if [ -d $2 ]
        then
          echo -e $2
          rm -rf $2
        fi

        echo "`date +%T` UNZIP: $2 => $1"
        unzip     -d $1 -o $2
    else
        echo "Not found $2"
        #return 0
    fi
    return 1
}

#-------------------------------------

do_mkdir() {
    for p in "$@"
    do
        echo -E mkdir -p "${p:gs.\\./.}"
        mkdir -p "${p:gs.\\./.}"
    done
}

#-------------------------------------
win32_path_to_posix()
{
    local p
    p="${1:gs.\\./.}"
    echo -E "$p"
}

#-------------------------------------
win32_add_path()
{
    path=("$1" $path)
}

#-------------------------------------
win32_cp()
{
    cmd /c copy "$1" "$2"
}

##############################################
# note
#
# DESCRIPTION:
#       echo parameters and save message to $LOGFILE
#
# INPUTS:
#       -t   - add current time to $LOGFILE output
#
##############################################
note() {
    time=
    if [ "x$1" = "x-t" ]; then
        shift
        echo -E "$@"
        echo -E "`cmd /c time /T` ""$@" >&3
    else
        echo -E "$@"
        echo -E "$@" >&3
    fi
}
#-------------------------------------
#-------------------------------------
#-------------------------------------
#--------------------------------------------------
# call: DurationTime  ${STARTTIME} ${TN}
#--------------------------------------------------

function DurationTime ()
{
    STARTTIME=$1
    TN=$2

    d=$( date +%T )
    TN1="$(date +%s%N)"
    ENDTIME="$d"
    # Time interval in nanoseconds
    T="$(($(date +%s%N)-TN))"

    # Seconds
    S="$((T/1000000000))"
    # Milliseconds
    M="$((T/1000000))"
    Min="$((S/60%60))"  
    echo          ---$3------------
    echo   "Start    : $STARTTIME"
    echo   "Finish   : $ENDTIME"
    printf "Duration : %02d:%02d:%02d,%02d\n" "$((S/3600%24))" "$((S/60%60))" "$((S%60))" "$(($M - $S*1000))"
    echo          ---------------
}
#--------------------------------------------------
# SCRIPT_DEBUG_MODE=trace
# SCRIPT_DEBUG_MODE=silent
# SCRIPT_DEBUG_MODE=info

#-------------------------------------
function trace_message()
{
    if [ "${SCRIPT_DEBUG_MODE:-info}" = trace ]; then
        echo -E "$@"
    fi
    return 0
}
#-------------------------------------
function T()
{
	trace_message "$@"
	"$@"
}

#-------------------------------------
function info_message()
{
    if [ "${SCRIPT_DEBUG_MODE:-info}" != silent ]; then
        echo -E "$@"
    fi
    return 0
}
#-------------------------------------
function I()
{
	info_message "$@"
	"$@"
}

#-------------------------------------
function warning_message()
{
    echo -E "$@"
    return 0
}

#-------------------------------------
function error_message()
{
    echo -E "$@" >&2
    return 0
}
#-------------------------------------
function create_not_exist_directory {
    if directory_not_exists $1
    then
        I mkdir -p $1
    fi
    return 0
}

#-------------------------------------
function csv_read()
{
	local filename=$1
	local dataname=$2
    local index=0

	while read line
	do
		eval $dataname[$index]=\"`echo $line|tr -d '\015'`\"
		((index++))
	done < $filename

}
#-------------------------------------
function csv_line()
{
	local dataname=$1
	local prefix=$2
	local index=$3

	
	local oldifs=$IFS
	local header
	local line
	local columnidx
	IFS=,
	eval header=\(\$\{$dataname[0]\}\)
	eval line=\(\$\{$dataname[$index]\}\)
	IFS=$oldifs
	for columnidx in ${!header[*]}
	do
		eval ${prefix}${header[$columnidx]}=\"\$\{line[$columnidx]\}\"
	done
}
#-------------------------------------
#-------------------------------------
#-------------------------------------


