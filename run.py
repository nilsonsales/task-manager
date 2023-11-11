import subprocess
from main import main

def run_main():
    print('running main.py')
    #main()
    subprocess.run(["streamlit", "run", "main.py"])

if __name__ == "__main__":
    run_main()
