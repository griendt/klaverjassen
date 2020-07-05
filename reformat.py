import subprocess

if __name__ == "__main__":
    subprocess.run(["black", ".", "-l120", "-tpy38"])
