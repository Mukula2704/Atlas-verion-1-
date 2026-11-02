import paramiko
import sys
import argparse

def execute_command(host, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username='root', password=password, timeout=10)
        
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        
        out = stdout.read().decode(errors='ignore').strip()
        err = stderr.read().decode(errors='ignore').strip()
        
        if out:
            print(out)
        if err:
            print(err, file=sys.stderr)
            
        client.close()
        sys.exit(exit_status)
    except Exception as e:
        print(f"[SSH Error]: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Command to execute on the Wyse')
    args = parser.parse_args()
    
    execute_command('192.168.1.2', 'Cool@1327', args.command)
