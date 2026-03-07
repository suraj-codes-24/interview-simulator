import subprocess

try:
    result = subprocess.run(["python", "run_seed.py"], capture_output=True, text=True)
    with open("error_log.txt", "w", encoding="utf-8") as f:
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
    print("Wrote to error_log.txt")
except Exception as e:
    print(e)
