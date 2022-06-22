#!/bin/bash
sudo touch /usr/bin/aria2py
sudo mkdir /etc/aria2py/
sudo wget --no-check-certificate https://github.com/SuperMore/Aria2Py/raw/main/aria2_py.py -O /etc/aria2py/aria2_py.py
sudo wget --no-check-certificate https://github.com/SuperMore/Aria2Py/raw/main/Aria2Py.py -O /etc/aria2py/Aria2Py.py
sudo chmod 777 /etc/aria2py/aria2_py.py
sudo rm -rf /usr/bin/aria2py
sudo cat << EOF > /usr/bin/aria2py
#!/bin/bash
python3 /etc/aria2py/aria2_py.py
EOF
sudo chmod 777 /usr/bin/aria2py
echo 'aria2py安装完成，在终端输入 aria2py 即可运行本程序'
