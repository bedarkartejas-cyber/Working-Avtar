import subprocess
import time
import sys
import os

def run_services():
    print("🚀 Starting Avatar Project Services...")
    
    # Ensure we are in the root directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    # 1. Start the FastAPI Backend
    # Merging stderr into stdout allows us to see the full Traceback
    api_process = subprocess.Popen(
        [sys.executable, "-m", "app.api.main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, 
        text=True,
        bufsize=1
    )
    
    # Wait to see if it crashes
    time.sleep(3)

    # 2. Start the LiveKit Agent
    agent_process = subprocess.Popen(
        [sys.executable, "-m", "app.main", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    try:
        while True:
            # Read and print API logs
            api_line = api_process.stdout.readline()
            if api_line:
                print(f"[API]: {api_line.strip()}")
            
            # Read and print Agent logs
            agent_line = agent_process.stdout.readline()
            if agent_line:
                print(f"[AGENT]: {agent_line.strip()}")
                
            # Exit if the API dies
            if api_process.poll() is not None:
                print("❌ API Process died. See the [API] logs above for the error.")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
    finally:
        api_process.terminate()
        agent_process.terminate()

if __name__ == "__main__":
    run_services()