# Setting Up the Python Environment with uv

Based on the course's uv migration guide (August 2026). Works on Windows, macOS, and Linux.

> **Note 1:** This document shows file and directory paths for a Unix operating system. If you are using Windows, change them to Windows style paths (for example, `C:\path\to\assignment-folder`).

> **Note 2:** On Windows, use PowerShell, not Command Prompt. The uv installer and the commands below are written for PowerShell.

## Why uv?

uv is a fast Python package and environment manager that replaces Conda for this course. It handles Python installation, virtual environments, and dependency locking automatically.

- **Fast:** installs packages and resolves dependencies in seconds, 10x to 100x faster than Conda
- **Automatic Python version management:** downloads and runs the exact Python version a project needs, with no manual paths
- **Exact reproducibility:** every project has a universal lockfile (`uv.lock`), so code runs the same on every operating system
- **Simple execution:** `uv run` runs scripts and notebooks inside the project's environment, so there's nothing to activate

## Step 1: Remove Existing Conda Environments (Optional)

If you set up a Conda environment for this course before, you can remove it to free up disk space.

1. Deactivate any running Conda environment:

```bash
conda deactivate
```

2. Remove the course environment (replace `mldev` with your environment's name):

```bash
conda env remove -n mldev
```

3. *(Optional)* List the Conda environments still on your system:

```bash
conda env list
```

> [!NOTE]\
> You do not need to uninstall Anaconda or Miniconda if you use it for other projects. Removing the course environment is enough.

## Step 2: Install uv

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or, on macOS with Homebrew:

```bash
brew install uv
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> [!IMPORTANT]\
> After the installer finishes, close and reopen your terminal so it can find the `uv` command.

### Verify the Installation

```bash
uv --version
```

## Step 3: Set Up Your Course Workspace

### Scenario A: Working With a Provided Assignment or Repository

Use this when you download an assignment folder that already has a `pyproject.toml` and a `uv.lock` file.

1. Open a terminal in the project folder:

```bash
cd path/to/assignment-folder
```

2. Build the environment from the lockfile:

```bash
uv sync
```

### Scenario B: Starting a New Machine Learning Project

1. Create a new project and move into it:

```bash
uv init ml-project
cd ml-project
```

2. Add the core machine learning libraries:

```bash
uv add numpy pandas scikit-learn matplotlib jupyter
```

3. Add PyTorch or TensorFlow if your assignment needs it:

```bash
# For PyTorch
uv add torch torchvision

# For TensorFlow
uv add tensorflow
```

## Step 4: Run Code and Notebooks

There's no `conda activate` with uv. Putting `uv run` in front of a command runs it inside the project's environment.

### Run a Python Script

```bash
uv run main.py
```

### Launch Jupyter Lab

```bash
uv run jupyter lab
```

> [!NOTE]\
> If Jupyter asks for a kernel, select the `.venv` Python kernel.

### Launch VS Code

```bash
uv run code .
```

### Run a Streamlit App

```bash
uv run streamlit run app.py
```

## uv Cheat Sheet

| Task | Command |
|---|---|
| Install project dependencies | `uv sync` |
| Add a package | `uv add <package-name>` |
| Remove a package | `uv remove <package-name>` |
| Run a script | `uv run <script.py>` |
| Launch Jupyter | `uv run jupyter lab` |
| Update dependencies | `uv lock --upgrade` |
| Update uv itself | `uv self update` |

## How uv Keeps Environments Reproducible

- **`pyproject.toml`** lists the packages your project needs, following the PEP 621 standard. `uv add` and `uv remove` update it for you.
- **`uv.lock`** records the exact version of every package, including the packages they depend on. Anyone who runs `uv sync` gets the same versions on Windows, macOS, or Linux.
- **`.venv`** is the project's virtual environment folder, holding its own Python interpreter and packages. uv creates and updates it automatically.
- **Global cache:** uv stores each downloaded package once in a shared cache and hard links it into each project's `.venv`, so ten projects using the same package don't take ten times the disk space.

> [!IMPORTANT]\
> Commit `pyproject.toml` and `uv.lock` to Git so others get the same environment. Don't commit `.venv` (uv rebuilds it with `uv sync`), and don't edit `uv.lock` by hand.

## Troubleshooting & FAQ

**Do I need to install Python first?**\
No. uv downloads and manages the exact Python version the project needs the first time you run `uv sync` or `uv run`.

**`command not found` when running a package's command (like `streamlit`)?**\
The package is installed inside `.venv`, but your shell isn't using that environment. Put `uv run` in front of the command, such as `uv run streamlit run app.py`. Or, activate the environment first with `source .venv/bin/activate` (macOS / Linux) or `.venv\Scripts\activate` (Windows).

**`uv: command not found` right after installing?**\
Close and reopen your terminal so it picks up the new install.

**VS Code isn't picking up my packages.**\
Press `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac), choose **Python: Select Interpreter**, and select the interpreter inside your project's `.venv` folder.

**How do I update uv?**\
Run `uv self update`. If you installed uv with Homebrew, run `brew upgrade uv` instead, since `uv self update` only works with the standalone installer.

## More Help

- uv documentation: https://docs.astral.sh/uv/
- uv command reference: https://docs.astral.sh/uv/reference/cli/
