@echo off
:: Requirements:
:: - putty
:: - pscp
:: - cputty (https://github.com/dprokscha/cputty)
:: - edge
:: - supernode
:: The last 2 programs are part of n2n (https://github.com/ntop/n2n), previously compiled on an EC2 Amazon Linux 2 instance.
:: You also need to save a Putty config with the SSH key for connecting to the EC2 instances.

set copyn2n=0
echo %* | find /i "-copy" 1>nul && set copyn2n=1

set HOSTS=54.152.18.78 3.93.248.201 54.162.246.45 18.212.65.227 54.147.159.102
if not %copyn2n%==1 goto _start

:_copy
echo Copying n2n
for %%a in (%HOSTS%) do start /min "" pscp -load aws-pd -l ec2-user n2n/* %%a:/home/ec2-user/

:_waitcopy
ping 127.0.0.1 -n 2 1>nul 2>nul
wmic process where "commandline like 'pscp%%aws-pd%%'" get commandline 2>nul | find /i "pscp" 1>nul && goto _waitcopy
echo:

:_start
echo Starting putty
for %%a in (%HOSTS%) do start "" putty -load aws-pd %%a -l ec2-user

echo Starting cputty
start "" cputty
echo cputty started
echo Press Ctrl+Alt+Insert to control all Putty windows
echo Press Ctrl+Alt+End to close it
