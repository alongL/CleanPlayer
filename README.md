# Intro

[CleanPlayer][] 通过修改 Flash 文件, 改变程序逻辑, 从而移除 Flash 程序内部的广告和跟踪功能.

[CleanPlayer-client][] 提供了一套 Flash 自动 patch 工具.

# Usage

0. Clone repo
0. 运行 init.py

# 相关知识

## Flash 程序修改流程

### Recompile with source code
0. 反编译 Flash 文件, 获得源代码 ([ActionScript][])
0. 阅读源代码
0. 修改源代码, 重编译成 Flash 文件

### [Hex Editing][]
0. 反编译 Flash 文件, 获得源代码 ([ActionScript][])
0. 阅读源代码
0. 用 Hex 编辑器修改 Flash 文件

### [Bytecode][] Editing
0. 反编译 Flash 文件, 获得源代码([ActionScript][])
0. 阅读源代码
0. 反编译 Flash 文件, 获得字节码 ([Bytecode][])
0. 用文本编辑器修改字节码
0. 将修改后的字节码重编译成 Flash 文件

## 反编译 Flash

[Sothink SWF Decompiler][] 是商业化的 Flash 反编译软件, 能够反编译出较完整的 [ActionScript][] 源代码, 但由于反编译出来的 [ActionScript][] 源代码存在较多语法错误, 无法通过编译, 只能通过 Hex 修改或字节码修改的方法来改变 Flash 的程序逻辑.

而 Hex 修改较为麻烦, 限制很多, 很难实现自动化, 所以本项目使用字节码修改的方法.

## 阅读 [ActionScript][] 源代码

[FlashDevelop][] 是一个开源免费的 [ActionScript][] 开发 IDE, 能极大地提高 [ActionScript][] 源代码阅读效率.

## [RABCDAsm][]

[RABCDAsm][] 是一套工具集, 包括 Flash assembler/disassembler, 可以将 Flash 文件反编译成字节码, 也可以将字节码重编译成 Flash 文件.

[RABCDAsm][] 作者
[CyberShadow][] 所写的 <[README for RABCDAsm][]> 较为系统地介绍了 Flash hacking 的相关知识.

[WinRABCDAsm][] 是 [RABCDAsm][] 的图形化前端, 极大地简化了 Flash assemble/disassemble 操作.

## [Flash Player Plugin content debugger][]

Debug 版本的Flash Player, 有助于查看 Flash 文件输出的 Error/Warning/Info.

## [Wamp][]

Windows + Apache + Mysql + PHP, 用于搭建本地调试环境.

## [Notepad++][]

[Notepad++][] 是一个开源免费的文本编辑器, 它自带的 LISP 高亮规则对 .asasm 字节码文件的支持度较好.

如果需要更佳的代码高亮体验, 可以使用 Eclipse 加载 [RABCDAsm][] 的 asasm.hrc 高亮规则.

## diff & patch

[GnuWin32][] 是 GNU 工具包的 Windows 移植, [GetGnuWin32][] 是 [GnuWin32][] 的自动化安装包.

本项目使用 diff -u 和 patch -u 生成补丁和应用补丁.

## [Python][]
[Python][] 是一种脚本语言, 本项目使用 [Python 2.7.3][] 书写 init.py, 完成以下功能
0. 自动同步 Flash 文件
0. 反编译 Flash 文件, 获得字节码
0. 应用字节码补丁
0. 将修改后的字节码重编译成 Flash 文件

## [TortoiseGit][]

字节码修改的过程较多较烦, 用 [Git][] 管理版本可以减少犯错的成本. [TortoiseGit][] 是 [Git][] 的图形化前端.

## [GitHub for Windows][]

[GitHub for Windows][] 是 [GitHub][] 的 Windows 客户端.

# License

[CleanPlayer-client][] is distributed under the terms of the [GPL v3][] or later, the full text of the GNU General Public License can be found in the file `COPYING`.

# Appendix

项目根目录下各目录/文件说明:

    root
    ├─ bin               --- 可能用到的 .exe 程序
    ├─ input             --- 存放原始 Flash 文件
    ├─ output            --- 保存修改好的 Flash 文件
    ├─ patch             --- 字节码补丁
    ├─ tools             --- 工具
    │   └─ WinRABCDAsm
    │       └─ RABCDAsm
    ├─ init.py           --- 初始化脚本
    ├─ link.json         --- 用于建立 ./bin/ 到 ./tools/WinRABCDAsm/RABCDAsm/ 的符号连接
    ├─ README.md
    └─ url.json          --- Flash 文件的下载地址



[Bytecode]: https://en.wikipedia.org/wiki/Bytecode
[Sothink SWF Decompiler]: http://www.sothink.com/product/flashdecompiler/
[ActionScript]: https://en.wikipedia.org/wiki/ActionScript
[FlashDevelop]: http://www.flashdevelop.org/
[RABCDAsm]: https://github.com/CyberShadow/RABCDAsm/
[CyberShadow]: http://blog.thecybershadow.net/
[README for RABCDAsm]: https://github.com/CyberShadow/RABCDAsm/blob/master/README.md
[WinRABCDAsm]: http://sourceforge.net/projects/winrabcdasm/
[Wamp]:http://www.wampserver.com/
[Notepad++]: http://notepad-plus-plus.org/
[GnuWin32]: http://gnuwin32.sourceforge.net/
[GetGnuWin32]: http://getgnuwin32.sourceforge.net/
[TortoiseGit]: https://code.google.com/p/tortoisegit/
[Git]: http://git-scm.com/
[GitHub for Windows]: http://windows.github.com/
[GitHub]: https://github.com/
[Python]: http://www.python.org/
[Python 2.7.3]: http://www.python.org/download/releases/2.7.3/
[Flash Player Plugin content debugger]: https://www.adobe.com/support/flashplayer/downloads.html
[GPL v3]: https://www.gnu.org/licenses/gpl.html


致谢： 鲁夫的爱