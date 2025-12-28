import subprocess
import time
import sys

def main():
    procs = []
    bots = ['pasutil1.worker', 'pasutil_tgbot.bot']
    
    for bot in bots:
        try:
            proc = subprocess.Popen([sys.executable, '-m', bot])
            procs.append(proc)
            print(f"Bot {bot} activate (PID: {proc.pid})")
        except Exception as e:
            print(f"start error {bot}: {e}")
    
    try:
        for proc in procs:
            proc.wait()
    except KeyboardInterrupt:
        print("Server is shuting down...")
        for proc in procs:
            proc.terminate()

if __name__ == "__main__":
    print("server on")
    main()
    print("server off")