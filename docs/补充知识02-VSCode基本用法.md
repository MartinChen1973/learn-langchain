## VS Code 基本用法指南（Python 初学者）

VS Code 是一个功能强大的代码编辑器，支持多种编程语言的开发。

比如要编写一个前端为 UniApp（万能小程序） + 后端用 Java Api + 调用人工智能接口 Python + LLM，可以只在 vscode 中完成。

以下是初次使用 VS Code 进行 Python 编程的一些基本操作步骤。

### 1. 打开目录

在开始编写代码前，需打开项目或代码所在的文件夹：

- 打开 VS Code。
- 选择菜单栏的 **File / Open Folder**（文件 / 打开文件夹）。
- 导航至课程代码目录（可以事先从助教处获得）。
- 选中该文件夹后，点击 **选择文件夹**（Select Folder）以载入项目。

### 2. 安装插件

为提升 Python 编程体验，VS Code 提供了各种插件，建议安装以下必备插件：

- 在左侧侧边栏选择 **Extensions**（扩展）图标，或使用快捷键 `Ctrl + Shift + X`。
  - **Python** 插件（由 Microsoft 提供），该插件包含语法高亮、自动补全、调试等功能。
  - **Pylance** 插件，如有需要也可以安装 ，以提高代码分析和提示性能。

### 3. 配置 Python 解释器

确保使用正确的 Python 解释器，避免因为多版本 Python 导致的依赖问题：

- 菜单栏选择 **View / Command Palette**（视图 / 命令面板），然后输入并选择 **Python: Select Interpreter**。
- 在弹出的解释器列表中，选择所需的 Python 版本
  - 建议使用预先安装并配置好的 Python 环境，例如 Anaconda 或 Python 3.12（2024-11-12 时流行的版本）。
- 确保所选的解释器路径与项目中的 Python 版本一致。

### 4. 使用终端

VS Code 内置了 Terminal（终端），可以直接在编辑器内执行命令行操作：

- 打开终端：在菜单栏中选择 **Terminal / New Terminal**（终端 / 新建终端）。
- 终端窗口会出现在编辑器下方，可以像命令行一样执行 Python 和 `pip` 命令。
- 使用终端窗口而非 windows 自带的 cmd 的原因，是终端会自动位于项目的目录下。

### 5. 利用 VS Code Terminal 和 pip 安装依赖包

为运行项目或课程中的示例代码，可能需要安装特定的依赖包。可以使用 `pip` 命令安装这些包。在安装依赖包前，请确保已经在 VS Code 的 Terminal 中启动虚拟环境（`venv`），以避免对全局 Python 环境造成影响。

- **启用虚拟环境**：
  在 VS Code Terminal 中，确保在当前项目根目录下（一般有一个 README.md）。运行
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
  此时会发现提示行的最前面有一个蓝色的（venv），则表示成功。
  **注意**：每次启动项目都需要重新运行第二行。
- **批量安装依赖包**：
  运行
  ```bash
  pip install -r requirements.txt
  ```
- **安装单个依赖包**：
  如果运行项目时提示某个模块找不到（例如 `langchain`），可以单独安装该模块：
  ```bash
  pip install langchain
  ```

### 6. 运行代码

VS Code 提供了多种方式运行 Python 代码，以下是常用方法：

- 打开 `.py` 文件后，点击右上角的 **Run Python File** 按钮（三角形图标）来运行代码。
- 或者，右键点击文件并选择 **Run Python File in Terminal**（在终端中运行 Python 文件）。
- 运行成功后，终端会显示代码输出结果。如果输出“Hello World!”等预期结果，则环境配置成功。

### 常见问题及解决方案

- **未找到模块错误**：例如 `ModuleNotFoundError: No module named 'dotenv'`，可能的原因是：

  - 依赖包未安装，请参考[利用 pip 安装依赖包](#利用-pip-安装依赖包)。
  - Python 解释器配置错误，请参考[配置 Python 解释器](#配置-python-解释器)。

- \*\*
  pip 不是命令（pip is not a command 或类似错误）：可能的原因是 pip 没有正确安装，或者其路径未添加到系统环境变量中。以下是一些解决方法：

```

```
