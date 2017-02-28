#!/usr/bin/expect -f 

#spawn ssh -p 9055 fabu@10.0.0.95

spawn ssh -p 9055 10.0.0.61
expect {

"*yes/no" { send "yes\r"; exp_continue}

#"*password:" { send "$passwd\r" }

}

#send "$passwd\r"
send "ls\r"
expect "*$"

send "pwd\r"
send "exit\r"
interact




