# py-awesome-kit
> Awesome python toolkit repository just for fun!

## 1. 安装Python3
```shell script
# 备份已安装python库
pip3 freeze > python3-installed-libs.txt

# 删除已安装的python
# Linux依赖包下载地址：https://vault.centos.org/7.3.1611/os/x86_64/Packages/
mkdir /env/python3.7
cd /env/Python-3.7.9
./configure --prefix=/env/python3.7 --enable-shared --enable-optimizations
make&&make install

```

## 2. 利用pip下载第三方包及其依赖
* 以安装jupyterlab为例
```shell
mkdir jupyterlab
cd jupyterlab
# 下载
pip3 download jupyterlab -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装
cd ..
pip3 install jupyterlab/jupyterlab-3.0.1-py3-none-any.whl --no-index --find-links=./jupyterlab

```

## 3. 从源码构建并安装py-awesome-kit

```shell script
# 进入项目根目录
cd <project_root>

# 构建/打包
python3 setup.py bdist_wheel

# 安装至python库
pip install dist/py-awesome-kit-<version>-py3-none-any.whl

# 应用开发过程中会频繁变更，每次安装都需要先卸载旧版本很麻烦。
# 使用 develop 开发模式安装的话，实际代码不会拷贝到 site-packages 下，而是除一个指向当前应用的链接（*.egg-link）。
# 这样当前位置的源码改动就会马上反映到 site-packages。使用如下：
pip install -e .  # 或者 python setup.py develop

# 如需卸载，使用如下命令：
pip uninstall py-awesome-kit
```

## 附录：Linux常用命令
### yum安装rpm包及依赖包相关命令
* 查看依赖包: 可以使用`yum deplist`命令来查找rpm包的依赖列表。例如，要查找`git`的rpm依赖包：
```shell
yum deplist git
```

* 方案一（推荐）：`repotrack`命令
```shell
# 安装yum-utils
yum -y install yum-utils

# 下载 git 全量依赖包
repotrack git
```

* 方案二：`yumdownloader`命令
```shell
# 安装yum-utils
yum -y install yum-utils

# 下载 git 依赖包
yumdownloader --resolve --destdir=/tmp git
```
> 参数说明：
> 
> --destdir：指定 rpm 包下载目录（不指定时，默认为当前目录）
> 
> --resolve：下载依赖的 rpm 包。
>
> 注意：仅会将主软件包和基于你现在的操作系统所缺少的依赖关系包一并下载。

* 方案三：yum 的`downloadonly`插件
```shell
# 下载 git 依赖包
yum -y install git --downloadonly --downloaddir=/tmp
```
> 注意：与 yumdownloader 命令一样，也是仅会将主软件包和基于你现在的操作系统所缺少的依赖关系包一并下载。

* 离线安装所有下载的rpm包
```shell
rpm -Uvh --force --nodeps *.rpm
```

* 其他命令
```shell
repoquery git

yum provides git
```

### git使用相关
* 项目之前是基于https克隆，现在通过配置SSH-KEY后想变更为用ssh方式提交
```text
之前已经是https的链接，现在想要用SSH提交怎么办？
直接修改项目目录下 .git文件夹下的config文件，将地址修改一下就好了。
```

### 常见系统配置问题
#### 1. 编写shell脚本后，在bash下单独执行没有问题，但在crontab中无法执行后报错
```shell
# 问题：编写shell脚本后，在bash下单独执行没有问题，但在crontab中无法执行后报如下错误信息：
# [psql: error while loading shared libraries: libpq.so.5: cannot open shared object file: No such file or directory]
# 原因剖析：
# crontab有一个坏毛病，就是它总是不会缺省的从用户profile文件中读取环境变量参数，经常导致在手工执行某个 脚本时是成功的，但是到crontab中试图让它定期执行时就是会出错。

# 解决方案一（推荐）：
# ------------------------------
sudo cp ./bin/greenplum-x86_64.conf /etc/ld.so.conf.d/greenplum-x86_64.conf
sudo ldconfig

# 用以下命令检查是否生效
ldconfig -p | grep green

# ------------------------------
# 解决方案二：通过在每个被crontab调用的shell文件前手动设置LD_LIBRARY_PATH环境变量。
export PATH="$PATH:/opt/mssql-tools/bin"
source /env/greenplum/clients/greenplum_clients_path.sh
source /env/greenplum/loaders/greenplum_loaders_path.sh

```

#### 2. 未设置`PYTHONPATH`环境变量导致的问题
如果系统中未设置`PYTHONPATH`环境变量，将导致`python some_module.py` 启动时会无法当前目录添加到`sys.path`中，
最终导致`import`项目中其他目录下的模块报错：未发现指定模块。

解决办法如下：
```shell
# vim ~/.bashrc  或 vim ~/.bash_profile 或 sudo vim /etc/profile
export PYTHONPATH=":$PYTHONPATH"
```
PS：就算已设置`PYTHONPATH`，如果在crontab中通过shell调用python脚本，仍然会发现当前目录未添加进`sys.path`中，导致模块加载报错。

原因为：crontab启动时是不会执行`~/.bashrc 或 ~/.bash_profile 或 /etc/profile`三个文件中的任何一个文件的，
这将导致crontab的执行上下文中并不存在中`PYTHONPATH`，即本质原因仍然是`PYTHONPATH`未设置问题。
解决办法多种：
1. 在crontab执行的shell中设置`PYTHONPATH`。
2. 修改crontab的全局配置文件（不建议）。


