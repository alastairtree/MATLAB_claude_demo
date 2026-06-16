# MATLAB + Claude code demo repository

Shows how to write MATLAB code inside a [dev container](https://code.visualstudio.com/docs/devcontainers/tutorial) so that it can be executed via CLI and un automated tests.

## Install prereqs

- Install WSL2 (probably a recent ubuntu distribution) and ensure it is running. From the powershell terminal, run `wsl --install`. https://learn.microsoft.com/en-us/windows/wsl/install
- Install Docker Desktop and ensure it is running. https://docs.docker.com/desktop/setup/install/windows-install/ 
- Install VSCode and the Remote Development extension pack.
- Open WSL2 and run `git clone THIS_REPO_URL` to clone this repository into a linux path (e.g., `/home/username/matlab-claude-demo`).
- Open the cloned repository in VSCode (cd into the repository path, run `code .`) and then click on the button in the bottom left corner "reopen this in a devcontainer". This will build the devcontainer and open a new VSCode window inside the container. Takes ~5m the first time as installing all of MATLAB.
- Type `claude` at the terminal and sign in to your claude account. 

You can always rebuild the entire container by opening the VS Code Command Palette with Cmd+Shift+P on Mac or Ctrl+Shift+P on Windows and Linux, and running Dev Containers: Rebuild Container.

## Setup licence server

MATLAB requires a license server to run. In the devcontainer, you can set the license server by setting the environment variable `MLM_LICENSE_FILE` to point to your license server. You can do this in the `.devcontainer/devcontainer.json` file or in the terminal before running MATLAB commands. The easiest way to do this is once per machine my making an ENV variable in your WSL2 bashrc file. and then forwarding that variable into the devcontainer for all your devcontainers. For example, in your WSL2 terminal, run:

```bash
echo 'export MLM_LICENSE_FILE=27000@your-license-server' >> ~/.bashrc
source ~/.bashrc
```

The devcontainer.json file should have the following line in the "remoteEnv" section:

```json
"remoteEnv": {
        // Forward the license server environment variable from the host machine to the devcontainer:
        "MLM_LICENSE_FILE": "${localEnv:MLM_LICENSE_FILE}",
        // Or just set it to the license server directly:
        // "MLM_LICENSE_FILE": "27000@your-license-server"
    },
```

## Access the MATLAB UI

Option 1: You can run the MATLAB UI inside the devcontainer by running `matlab` in the devcontainer terminal. This will open a new window with the MATLAB UI from linux. This is linux MATLAB inside the container, not windows MATLAB already installed on your machine. You can also run MATLAB commands from the command line in the devcontainer terminal.

Option 2: Desktop MATLAB, in windows, can read files from the WSL2 filesystem. You can open MATLAB in windows and then use the `cd` command to change to the path of the cloned repository (e.g., `cd \\wsl.localhost\Ubuntu-XX.XX\home\username\matlab-claude-demo`) to access the files.

The MATLAB VSCode Extension (pre-installed in devcontainer) will also enable basic running and debugging of files inside vscode. See https://marketplace.visualstudio.com/items?itemName=MathWorks.language-matlab for more info.

Option 3: Use the proxy and access MATLAB UI from your browser. Use the devcontainer setting startInDesktop to start matlab-proxy when container starts.

## Use the MATLAB CLI

```bash
matlab -nodesktop -batch "run('src/hello.m')"
# alternatively, you can run the script directly from the command line:
matlab -nodesktop -batch "cd src; hello"
```

## Calling MATLAB from python

We demonstrate calling MATLAB from python using the `MatlabWrapper.py` script. You can run the script from the devcontainer terminal as follows. This adds some logging, sets up pathing, has error handling around the MATLAB command, and ensures that the MATLAB batch CLI works even when running under github actions.

```bash
# output a default hello from matlab:
python src/MatlabWrapper.py
# Run some custom matlab command:
python src/MatlabWrapper.py "disp('running matlab code from the CLI via python')"
```

## Running unit tests

The HelloTest contains MATLAB unit tests using the built-in `matlab.unittest` framework.

```bash
# Run all tests and assert they pass
matlab -nodesktop -batch "addpath('/workspaces/MATLAB_claude_demo/src'); results = runtests('/workspaces/MATLAB_claude_demo/tests/HelloTest.m'); disp(results); assert(all([results.Passed]), 'Tests failed')"
```

Expected output:
```
Running HelloTest
hello world
..
Done HelloTest
__________
   2 Passed, 0 Failed, 0 Incomplete.
```

To add more tests, create a new class file in `tests/` that extends `matlab.unittest.TestCase`, then add methods annotated with `(Test)`.

## MATLAB projects

By default the `src` folder is setup as a MATLAB project. IN vscode you right click a folder > MATLAB Project > New/Open. You can also open the project in the MATLAB UI by running `matlab` in the devcontainer terminal and then using the "Open Project" option in the MATLAB UI to open the `src` folder as a project. This will enable features like project paths, dependencies, etc.