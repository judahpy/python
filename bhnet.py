import sys
import socket
import getopt
import threading
import subprocess

#var
listen= False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print "BHP net tool"
    print
    print "usage: bhpnet.py -t target_host -p port"
    print "-l --listen -listening on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute the given file upon receiving a connection"
    print "-c --command - initialize a command shell"
    print "-u --upload=destination - upon receiving a connection upload a file and write to [destination]"
    print
    print
    print "Examples: "
    print " bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print " bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print " bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)
    
def main():
    global listen
    global port
    global execute
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    #read in
    try:
        opts, args = getopt(sys.argv[1:], "hle:t:p:cu", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "unhandled option"

#listen or send data from stdin
if not listen and len(target) and port >0:

    #read in buffer from cmd
    #this will block so ctrl D
    #to stdin
    buffer = sys.stdin.read()

    #send data off
    clien_sender(buffer)

#listen
#upload
if listen:
    server_loop()

    
main()
            
        
