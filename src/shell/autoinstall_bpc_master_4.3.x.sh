#!/usr/bin/expect
set stty_init "rows 200 cols 200"
spawn ./install.sh
set timeout 10
send "ddddddd"
set timeout 10
send "\r\r\r\r\r\r\r\r\r\r\r\r\r\r"
set timeout 10
expect "y/n"
set timeout 10
send "y\r"
set timeout 10
expect -re "Select User" {
    if {[string match {*( )  crossflow*} $expect_out(buffer)]} {
            send "\t\t\t\t"
            send "\r"
        } 
}
set timeout 10
expect -re "Select Network Card" {
    if {[string match {*DPDK*} $expect_out(buffer)]} {
            send "\t"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "j"
            send "\r"
            send "\t\t\t\t"
            send "\r"
        }
}
set timeout 10
expect -re "Setup Config" {
    if {[string match {*( )  172.16.*} $expect_out(buffer)]} {
            send "j"
            send "\r"
        } 
}
send "\t\t\t\t\t\t\t\t"
set timeout 10
send "\r"
set timeout 1200
expect "Installation finished"
send "\r" 
send "exit\r"
expect eof
