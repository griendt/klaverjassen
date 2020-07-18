import subprocess

if __name__ == "__main__":
    subprocess.run(["python", "-m", "black", ".", "-l120", "-tpy38"])
