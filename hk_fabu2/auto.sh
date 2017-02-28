#!/usr/bin/expect -f
set ip [lindex $argv 0]
set port [lindex $argv 1]
set passwd [lindex $argv 2]

#1、免秘钥登陆
spawn ssh -p $port $ip
expect {

"*yes/no" { send "yes\r"; exp_continue}

"*password:" { send "$passwd\r" }

}

send "$passwd\r"
expect "*#"

#2、创建fabu账号
send "useradd -p `openssl passwd -1 -salt 'a' $passwd` fabu\r"
send "mkdir /home/fabu/.ssh\r"
send "chown fabu:fabu /home/fabu/.ssh\r"
send "exit\r"

#3、拷贝秘钥文件
spawn scp -P$port /home/fabu/.ssh/id_rsa.pub root@$ip:/home/fabu/.ssh/pub_key
expect {

"*yes/no" { send "yes\r"; exp_continue}

"*password:" { send "$passwd\r" }

}


#4、再次登陆并设置文件属性
spawn ssh -p $port $ip
expect {

"*yes/no" { send "yes\r"; exp_continue}

"*password:" { send "$passwd\r" }

}

send "$passwd\r"
expect "*#"

send "cat /home/fabu/.ssh/pub_key >> /home/fabu/.ssh/authorized_keys\r"
send "chmod 600 /home/fabu/.ssh/authorized_keys\r"
send "chown fabu:fabu /home/fabu/.ssh/authorized_keys\r"
send "chmod 700 /home/fabu/.ssh\r"
send "exit\r"
interact

#5、验证第一次登陆
spawn su fabu
expect "*$"
send "ssh -p $port $ip\r"
expect {
"*yes/no" { send "yes\r"; exp_continue}
}
#send "pwd\r"
send "exit\r"
#send "exit\r"
#interact
