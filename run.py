import subprocess
import logging

logger = logging.getLogger()

def run_main():
    logger.info('Starting Streamlit app')
    subprocess.run(["streamlit", "run", "main.py"])

if __name__ == "__main__":
    run_main()
