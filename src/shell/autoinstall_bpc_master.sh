#!/usr/bin/expect
spawn ./install.sh
set timeout 10
send "ddddd"
send "\r\r"
set timeout 10
expect {
    "y/n" {send "y\r";exp_continue}
    set timeout 10
}
expect {
    "*root" {send "\t\t\t\r";exp_continue}
    set timeout 10
}
expect {
    "*Pktminer" {send "\t";exp_continue}
    set timeout 10
}
expect {
    'PCI=*' {send "x";exp_continue}
    set timeout 10
}
send "\t\t\t\t\t\t\t\r"
set timeout 10
expect {
    "*Select Server Ip*" {send "\t\t\t\t\t\t\r"}
    set timeout 10
}
set timeout 1200
expect "Install success"
send "\t\t\r\r" 
set timeout 10
send "exit\r"
set timeout 10
expect eof
