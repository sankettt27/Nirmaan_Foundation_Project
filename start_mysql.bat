@echo off
echo Starting MySQL Server 8.4...
start /B "" "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe" --defaults-file="D:\mysql_data\my.ini" --console
ping 127.0.0.1 -n 3 >nul
echo MySQL Server is active on port 3306.

