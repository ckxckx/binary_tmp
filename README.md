# Redbud 线下基础设施

对于线下模式，无论是攻防还是解题模式，基本工作模式均为：**远程人员<——借助 openvpn——>现场人员**。

## 基本要求

- 安装支持 openvpn 服务软件
  - Windows / Linux：openvpn，https://openvpn.net/
  -  Mac OS：tunnelblick
- 熟悉基本的 Linux 命令行操作
  - 多个 terminal 快速管理
    - tmux for Linux
    - iterm for Mac OS
- 熟悉基本的 ssh 命令
  - 快速**无密码别名**登录—>**统一脚本？**
    - ssh-copy-id 将公钥传递到远程服务器上。
    - 配置 config 文件，设置对应服务器域名
  - scp 传文件
  - 。。。

## 远程玩家

只需要使用 `redbud_infrastructure/redbud-center/ovpn-keys/common-client.tar.gz` 连接vpn 即可。

## 基本设备

### servers

目前主要有两台服务器

|  名字，简称   |             IP / 域名             |                    说明                     |
| :-----------: | :-------------------------------: | :-----------------------------------------: |
| redbud-center | 123.57.210.184 / eadom.firesun.me |      用于远程人员通过外网接入现场内网       |
|  redbud-nuc   |                无                 | Next Unit of Computing，与外网建立 vpn 连接 |
|    交换机     |                                   |             配置 VLAN，网络隔离             |

## 网络拓扑

### 基本拓扑图

有待画一个图。

### 全局核心拓扑

|       ip        |        位置        |                        说明                        |
| :-------------: | :----------------: | :------------------------------------------------: |
|  172.16.200.1   |   redbud-center    |                      固定 ip                       |
| 172.16.200.101  |     redbud-nuc     |                      固定 ip                       |
| 172.16.200.0/24 | 远程人员，世界各地 | redbud-center 为其分配 IP，通过 common-client 连入 |

### 比赛现场拓扑

|       ip        |    位置    |       说明        |
| :-------------: | :--------: | :---------------: |
|  172.16.201.1   | redbud-nuc |      固定 ip      |
| 172.16.201.0/24 | redbud-nuc | 为现场人员分配 ip |

### 交换机

交换机端口的 VLAN 划分。

![](figure/switcher.jpeg)

这里处于同一个 vlan 之间的端口可以互相通信。

一般来说，配置如下

- 1 号端口接 NUC，并与 NUC 形成 trunk 连接。
- 2 号端口接现场网线。
- 选手接入 5 6 7 8 端口。

## Redbud center 基本配置

基本流程如下

1. 先获取赛场内网 ip 段
   1. gamebox 段
   2. scoreboard 段
   3. flag 段
   4. 本机用户段


1. 利用 `/etc/openvpn/subnet.sh` 脚本写入 `ccd/redbud-nuc` 和 `server.conf`，配置相关的 IP 和路由，使得远程用户可以直接连接到内网，使用方式如下(以下操作在vps上进行，而非nuc)

   ```sh
   # $1 for commad
   # $2 for ip, e.g. 192.168.0.1
   # $3 for mask, e.g. 255.255.255.0
   
   # add subnet
   ./subnet.sh add ip mask
   # clean all the subnet
   ./subnet.sh clean
   # show all the subnet
   ./subnet show
   ```

3. 重新 openvpn 服务，便于远程用户接入。

   ```shell
   service openvpn restart
   ```

   

## NUC 基本配置

NUC 主要提供一下服务

- 为远程人员提供现场接入网络服务。

- 为线下赛准备的内网工具

目前使用的系统为`Ubuntu 16.04` 。

### network 端口

|   端口   | 描述                                                         |
| :------: | :----------------------------------------------------------- |
|   wan0   | 保留网口，NUC 的原生网口，目前静态IP **172.16.233.1**，紧急情况使用 |
|  wan0.1  | LAN 口，vlan id = 1，连接交换机的 5，6，7，8 这几个网口      |
| wan0.2-4 | WAN 口，分别对应 vlan id = 2 3 4，可以连接主办方外网         |
|   lan0   | LAN 口，USB 网卡，在启动前需要插好                           |
|  wlan0   | 无线，普通不用                                               |

配置文件位于 `/etc/network/interfaces` ，控制命令

如果需要 wan0 和 lan0 都使用静态 IP，则可以启动 wifi 用作内网，需要修改 dhcpd 的设置`/etc/dhcpd.conf`,关闭`172.16.201.0/24`上的dhcp，开启`172.16.202.0/24`上的dhcp。之后重启dhcpd，启动hostapd，生成wifi热点。

设置 wan0 和 lan0 静态IP的方法，编辑`/etc/netctl/wan0-static`与`/etc/netctl/lan0-static`，并使用netctl启动。无线网络hostapd的配置在`/etc/hostapd/hostapd.conf`里面有wifi的SSID和密码。

### wifi 连接

如果需要用 wifi 来连接外网

```
wicd-curses
```

连接wifi以后需要查看并设置路由表，以便连接赛场内网络

设置路由规则：
```
ip route
ip route del default
ip route add default via 192.168.8.1
ip route add 192.168.60.0/24 via 192.168.50.1
ip route del 192.168.60.0/24
具体网段和ip视情况而定。
```



LAN 口 IP 为 172.16.201.1, DHCP 分配 172.16.201.0/24。

路由器内使用 rebud-nuc.tar.gz 证书连接到 redbud-center。

配置文件位于 /etc/openvpn。

启动命令如下

```
systemctl start openvpn@redbud-nuc
```

### iptables

INPUT 默认禁止除了内网的 IP 连接，除了 SSH 和 HTTP

配置在 /etc/iptables/iptables.rules

### Index:80

主页引导页，仅允许内网地址访问

`/download/`: 内部文件下载页面，包括pcap的下载
`/log/`: 服务器日志
`/ext/`: 暴露给外部的路径，使用的是不同的日志

## 文件共享

共享规则

- 为 pwn 和 web 分别创建一个目录。

主要用于共享

- 题目
- 攻击脚本
- patch binary

如果设置密码，请设置为`lyksg` ，意为留一刻时光。

## 聊天工具

### Bearychat

比赛时协作，务必在比赛时使用该方式进行交流

- 团队名：redbud
- 注册地址：https://redbud.bearychat.com/，可以考虑使用邮箱注册。

### RocketChat:3000

一个离线环境的RocketChat备份，在无法连接外网的情况下可以使用

```
cd /root/docker/rocketchat
docker-compose up -d
```

## 运维与攻击脚本

参见对应目录的详细说明

- `bxtools` : 自动化攻击框架以及一些后门工具，目前由`BrieflyX`维护
- `php logger`: web工具，php的logger
- `inotify monitor`: 使用inotify监视flag状况，check本轮是否被读过
- `center server`: 全队提交flag的接口，所有的攻击成功后可以通过简单地`curl http://172.16.xxx.xxx/flag/ThisIsFlag`进行提交，并将每轮flag的提交情况记录在数据库中。之前`Firesun`有用tornado写过一个简单的版本，不过没有界面，需要一个前端界面看的比较清楚。



