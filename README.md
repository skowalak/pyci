`pyci` stands for **Py**thon **c**onfiguration **i**nterface (which is an obvious hommage to OpenWrts [uci][openwrt_uci]) and aims to provice an interface to configure a host system via different inter-process-communication buses.

Currently supported buses are: UNIX Domain Sockets, MQTT
Currently supported backends are: SaltStack, Ansible and our very own Invoke-based backend

[openwrt_uci]: https://openwrt.org/docs/techref/uci
