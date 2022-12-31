# 以下两个包都是画图的包，第一个很鸡肋，第二个是主要的。安装可能费点功夫，但是打包成exe文件一直失败，所以实在是无能为力了
# 这是专门表示有限状态机，如果按照这个包很麻烦就注释掉它相关的代码
from transitions.extensions import GraphMachine
# 这个是只画图，这个包的安装可能不成功，实在不行可以注释掉相关的代码
from graphviz import Digraph
