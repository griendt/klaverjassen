import subprocess

if __name__ == "__main__":
    subprocess.run(["python", "-m", "black", ".", "-l120", "-tpy38"])
    subprocess.run(["python", "-m", "mypy", "--disallow-untyped-defs", "--disallow-any-generics", "."])
