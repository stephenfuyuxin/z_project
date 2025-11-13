# 图示
## single
CPU1 <——> CPU2  
  |          |
SW1         SW2
  |          |
GPU0-3      GPU4-7

默认设置，不同 pcie switch 分属于不同的cpu，cpu/gpu 分属关系；

## multiple
CPU1 <——> CPU2  
  |          
SW1 <-----> SW2
  |          |
GPU0-3      GPU4-7

通过配置修改，完成pcie switch级联，cpu/gpu 归属关系发生变化；

# 配置修改方式
说是有两种方式，ibmc和os，这里记录ibmc方式的，os的暂未尝试，

## 通过 ibmc 后台进行修改
1、ssh登录bmc后台，

2、查询当前root模式，示例如下，
```shell
~# ipmcget -t resource -d pcie
current settings: 0     Setting Mode 0 : double root port

  Position         State|Health     "Description"
------------------------------------------------------------
  cpu1/dev1:       Enable|OK        "PCIe Card"
  cpu1/dev3:       Enable|OK        "PCIe Card"
  cpu1/dev5:       Enable|OK        "PCIe Card"
  cpu1/dev7:       Enable|OK        "PCIe Card"
  cpu2/dev10:      Enable|OK        "PCIe Card"
  cpu2/dev12:      Enable|OK        "PCIe Card"
  cpu2/dev14:      Enable|OK        "PCIe Card"
  cpu2/dev16:      Enable|OK        "PCIe Card"
```

3、设置成单root模式，示例如下，
```shell
~# ipmcset -t resource -d pcie
Usage: ipmcset -t resource -d pcietopology -v <Setting Mode>
Setting Mode : 0
  Upside                        Downside
------------------------------------
  cpu1: {dev1 , dev3 , dev5 , dev7 };
  cpu2: {dev10, dev12, dev14, dev16};
Setting Mode : 1
  Upside                        Downside
------------------------------------
  cpu1: {dev1 , dev3 , dev5 , dev7 , dev10, dev12, dev14, dev16};

~# ipmcset -t resource -d pcie -v 1
Set pcie topology successfully.
```

4、dc掉电生效，掉电重启之后，再次查询当前root模式即可；

## 通过 os 后台进行修改
先安装 ipmitool 工具，以 ubuntu 22.04 为例，
```shell
apt install -y ipmitool
```
通过 os 后台进行查询/修改，
```shell
# 查询root
~# ipmitool raw 0x30 0x9a 0x0e 0x00 0x07

00 01
# 回显为00 01为单root
00 00
# 回显为00 00为双root

# 设置双root：
~# ipmitool raw 0x30 0x9a 0x0f 0x00 0x07 0x00 

# 设置单root:
~# ipmitool raw 0x30 0x9a 0x0f 0x00 0x07 0x01
```

# 效果展示
先查询，默认为双root，修改需掉电重启生效，重启完毕之后再次查询，显示为单root，
```shell
iBMC:/->ipmcget -t resource -d pcie
current settings: 0     Setting Mode 0 : double root port

  Position         State|Health     "Description"
------------------------------------------------------------
  cpu1/dev1:       Enable|OK        "PCIe Card"
  cpu1/dev3:       Enable|OK        "PCIe Card"
  cpu1/dev5:       Enable|OK        "PCIe Card"
  cpu1/dev7:       Enable|OK        "PCIe Card"
  cpu2/dev10:      Enable|OK        "PCIe Card"
  cpu2/dev12:      Enable|OK        "PCIe Card"
  cpu2/dev14:      Enable|OK        "PCIe Card"
  cpu2/dev16:      Enable|OK        "PCIe Card"

iBMC:/->ipmcset -t resource -d pcie -v 1
Set pcie topology successfully.

iBMC:/->
iBMC:/->ipmcget -t resource -d pcie
current settings: 0     Setting Mode 0 : double root port

  Position         State|Health     "Description"
------------------------------------------------------------
  cpu1/dev1:       Enable|OK        "PCIe Card"
  cpu1/dev3:       Enable|OK        "PCIe Card"
  cpu1/dev5:       Enable|OK        "PCIe Card"
  cpu1/dev7:       Enable|OK        "PCIe Card"
  cpu2/dev10:      Enable|OK        "PCIe Card"
  cpu2/dev12:      Enable|OK        "PCIe Card"
  cpu2/dev14:      Enable|OK        "PCIe Card"
  cpu2/dev16:      Enable|OK        "PCIe Card"

# 掉电重启完之后再次查询
iBMC:/->
iBMC:/->ipmcget -t resource -d pcie
current settings: 0     Setting Mode 0 : double root port

  Position         State|Health     "Description"
------------------------------------------------------------
  cpu1/dev1:       Enable|OK        "PCIe Card"
  cpu1/dev3:       Enable|OK        "PCIe Card"
  cpu1/dev5:       Enable|OK        "PCIe Card"
  cpu1/dev7:       Enable|OK        "PCIe Card"
  cpu1/dev10:      Enable|OK        "PCIe Card"
  cpu1/dev12:      Enable|OK        "PCIe Card"
  cpu1/dev14:      Enable|OK        "PCIe Card"
  cpu1/dev16:      Enable|OK        "PCIe Card"
```
