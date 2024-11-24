![Banner](img/banner.jpg)

<div align="center">
  
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mrrobinofficial/shutdownx/blob/HEAD/LICENSE.txt)
![Build Status](https://github.com/mrrobinofficial/shutdownx/actions/workflows/build-and-release.yml/badge.svg)
![Testing Status](https://github.com/mrrobinofficial/shutdownx/actions/workflows/testing.yml/badge.svg)

_A simple interactive cli tool for scheduling a shutdown on Windows_ 

</div>

#

ShutdownX is a Windows tool that allows you to schedule automatic shutdowns using a simple interface. You can schedule the shutdown based on a specific time or set a timer for the duration.

![Showcase](img/showcase.gif)

## ⚙️ Requirements

- **Python 3.8+**: Required to build and run the project.
- **Windows OS**: ShutdownX is designed to work on Windows.

## 🛠️ Dependencies
- [inquirer](https://pypi.org/project/inquirer/): Used for interactive prompts.
- [rich console](https://rich.readthedocs.io/en/latest/console.html): Used for enhanced console output.
- [PyInstaller](https://pyinstaller.org/en/stable/): Used to package the Python script as a standalone `.exe` file.
- [Commitizen](https://github.com/commitizen/cz-cli): Automates version bumping and changelog updates based on conventional commit messages.

## 🚀 Installation

You can install ShutdownX using one of the following methods:

- **Release**: Download the pre-built `.exe` file from the [Releases](https://github.com/MrRobinOfficial/shutdownx/releases) section.
- **Manual Installation**: Follow the instructions in the [Manual Installation](#manual-installation) section.

> [!TIP]
> You can add the `shutdownx.exe` file to your `PATH` variable to make it accessible from any directory.

### Manual Installation

### 1. Clone the repository:
First, clone the repository to your local machine:
```bash
git clone git@github.com:MrRobinOfficial/shutdownx.git
cd shutdownx
```

### 2. Modifying the Repository:

When you are working with the project, remember to run the tests:

```bat
CALL .\scripts\test.bat
```

```powershell
& .\scripts\test.ps1
```

### 3. Building the Executable:

You can run the build script to build the `.exe` file from the source code:

```bat
CALL .\scripts\build.bat
```

```powershell
& .\scripts\build.ps1
```

This script will create a virtual environment, install the required dependencies, and build the `.exe` file.

The `.exe` file will be generated in the `dist` folder.

## 🔥 Usage

After building the `.exe` file, you can use the tool to schedule a shutdown in one of two modes:

### 1. **Using Arguments**:

You can specify the shutdown time or duration using command-line arguments:

#### **Shutdown by Specific Time**:
To schedule the shutdown at a specific time, use the `--time` argument followed by the time in **HH:MM** or **HH:MM AM/PM** format. For example:
```bash
shutdownx.exe --time 12:30
```
This will shut down the computer at **12:30 PM**.

#### **Shutdown by Duration**:
Alternatively, you can specify a shutdown timer using the `--duration` argument, providing a duration in formats like **2h 30m**, **2 hours 10 minutes**, **15s** or **01:30**. For example:
```bash
shutdownx.exe --duration "2 hours 30 minutes"
```
This will shut down the computer after **2 hours and 30 minutes**.

**Note**: You can **only specify one** option: either a specific time with `--time` or a duration with `--duration`. Using both arguments together will result in an error.

### 2. **Interactive Mode**:

If you prefer a guided experience, the tool also offers an **interactive mode**. Simply run the executable without any arguments:
```bash
shutdownx.exe
```
The tool will prompt you to choose between setting a shutdown by **specific time** or **duration**. It will then guide you through confirming your selection and scheduling the shutdown, making it easier to use without needing to manually enter complex arguments.

## 🆘 Support
If you have any questions or issue, just write either to my [YouTube channel](https://www.youtube.com/@mrrobinofficial), [Email](mailto:mrrobin123mail@gmail.com) or [Twitter DM](https://twitter.com/MrRobinOfficial).