import paramiko
import sys
import argparse

def upload_file(host, password, local_path, remote_path):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username='root', password=password, timeout=10)
        
        with open(local_path, 'rb') as f:
            data = f.read()
            
        stdin, stdout, stderr = client.exec_command(f"cat > {remote_path}")
        stdin.write(data)
        stdin.channel.shutdown_write()
        
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print(f"[SUCCESS] Uploaded {local_path} to {remote_path}")
        else:
            print(f"[ERROR] Failed to write {remote_path}: {stderr.read().decode()}", file=sys.stderr)
            
        client.close()
    except Exception as e:
        print(f"[SSH Transfer Error]: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('local', help='Local file path')
    parser.add_argument('remote', help='Remote file path')
    args = parser.parse_args()
    
    upload_file('192.168.1.2', 'Cool@1327', args.local, args.remote)
