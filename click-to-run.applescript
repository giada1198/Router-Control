set unix_path to POSIX path of ((path to me as text) & "::")
# display dialog "Path: " & unix_path -- activate this line to debug if it cannot find the script
do shell script "usr/local/bin/python3 " & unix_path & "main.py & killall applet"