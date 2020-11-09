# -*- coding: utf-8 -*-
import os
import sys

"""
修复 Python 解释器无法从根目录查找模块的问题

因为 bin/*.py 可能会有很多可执行的 Python 程序文件，它们都不是在根目录下
我们执行 bin/ 目录下的程序的方式可能有以下几种

1. 在项目根目录执行,比如: python bin/lh_pdp_repairer.py
2. 在项目 bin 目录执行,比如: python lh_pdp_repairer.py

为解决在任意目录下执行 bin/ 目录下的 .py 文件都可以正常 working (Not found Named xxx Module 问题)
我们把项目根目录作为 Python 解释器查找 Module 的一部分设置到 path 上
"""
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "..")))

if __name__ == '__main__':
    from tools.lanhu.pdp.dm.repairer import ContentRepairer
    rep = ContentRepairer()
    sys.exit(rep.start())
