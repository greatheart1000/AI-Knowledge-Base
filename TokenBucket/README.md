
```
uvicorn main:app --reload --host 0.0.0.0
在 WSL 2 中，默认情况下会有一个虚拟的 NAT 网络用于与 Windows 主机通信。要找到 Windows 主机的 IP 地址，你可以使用以下命令
ip route show | grep -i default | awk '{ print $3 }'

curl http://172.27.152.1:8000/hello

