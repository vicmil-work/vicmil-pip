# install latest version of vicmil-pip in this file
import urllib.request
with urllib.request.urlopen('https://raw.githubusercontent.com/vicmil-work/vicmil-pip/refs/heads/main/vicmil-pip.py') as f:
    html = f.read().decode('utf-8')
    with open(__file__, "w") as this_file:
        this_file.write(html)