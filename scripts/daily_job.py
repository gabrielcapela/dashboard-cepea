from pathlib import Path
import time
import subprocess

# This defines the base directory as the folder where this script is located.
# It ensures the script can locate the other .py files even in production or cloud environments.
BASE_DIR = Path(__file__).parent

def run_script(script_name):
    # Builds the full path to the script to be executed
    script_path = BASE_DIR / script_name
    print(f"\n📌 Running {script_name}...")
    
    # Executes the script as a subprocess and captures its output
    result = subprocess.run(['python', str(script_path)], capture_output=True, text=True)
    
    # Displays the standard output of the script
    print(result.stdout)
    
    # If there was an error, print it
    if result.stderr:
        print("⚠️ Error:", result.stderr)

# Infinite loop to run the three scripts daily
while True:
    print("⏰ Starting CEPEA daily routine...\n")
    
    run_script("cepea_scraper.py")
    run_script("insert_data.py")
    run_script("modeling.py")
    
    print("\n✅ Scripts completed successfully! Sleeping for 24 hours...\n")
    time.sleep(86200)  # Sleep for 24 hours - 2 minutes to account for script execution time
