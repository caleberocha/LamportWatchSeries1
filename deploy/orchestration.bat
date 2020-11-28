@echo off

:: Requirements:
:: - putty
:: - pscp
:: - cputty (https://github.com/dprokscha/cputty)
:: - edge
:: - supernode
:: The last 2 programs are part of n2n (https://github.com/ntop/n2n), previously compiled on an EC2 Amazon Linux 2 instance.
:: You also need to save a Putty config with the SSH key for connecting to the EC2 instances.

set HOSTS=52.23.181.127 18.212.13.26 54.175.42.12 54.163.125.195 3.84.24.224
echo Copying n2n
for %a in (%HOSTS%) do pscp -load aws-pd -l ec2-user n2n/* %a:/home/ec2-user/
echo:

echo Starting putty
for %a in (%HOSTS%) do putty -load aws-pd %a -l ec2-user

cputty
