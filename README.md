# YTDownloader
Youtube downloader without ads 😱😱😱😱
very basic and i did it in like 2 hours

also i used chatgpt for installation guide so lmk if there is anything wrong with it LOL


> [!IMPORTANT]  
> THIS IS FOR EDUCATIONAL PURPOSES ONLY DO NOT DO ANYTHING MALICIOUS WITH THIS<br>
> I AM NOT LIABLE FOR THE DAMAGES DONE USING THIS TOOL

## Running from source

Welcome to YTDownloader! This guide will walk you through the steps to get YTDownloader up and running on your machine.

## Step 1: Installing Python

YTDownloader is a Python-based application, which means you need to have Python installed on your computer to run it. Here's how you can install Python:

### For Windows Users

1. Go to the official Python website's download page: [Python Downloads](https://www.python.org/downloads/windows/)
2. Click on "Download Python" (choose the version recommended for your Windows).
3. Once the installer is downloaded, run it.
4. Make sure to check the box that says "Add Python to PATH" at the beginning of the installation process.
5. Follow the rest of the prompts to install Python.
6. To confirm the installation, open your Command Prompt and type `python --version` and press Enter. If you see a version number, it means Python is installed correctly.

### For macOS Users

1. Go to the official Python website's download page: [Python Downloads](https://www.python.org/downloads/mac-osx/)
2. Click to download the latest version for macOS.
3. Open the downloaded package and follow the instructions to install Python.
4. To confirm the installation, open the Terminal and type `python3 --version` and press Enter. You should see the version of Python that you installed.

### For Linux Users

Most Linux distributions come with Python pre-installed. To check if Python is installed and to see which version you have, open a terminal and type:
```bash
python3 --version
```
If Python is not installed or you want a newer version, you can install it using your distribution's package manager. For example, on Ubuntu, you can install Python by typing:
```bash
sudo apt update
sudo apt install python3
```

## Step 2: Cloning the Repository

Now that you have Python installed, the next step is to get the code from the YTDownloader GitHub repository.

1. Open your terminal (Command Prompt for Windows, Terminal for macOS and Linux).
2. Navigate to the directory where you want to clone the repository using `cd` command. For example:
```bash
cd path/to/your/directory
```
3. Now, clone the repository by running:
```bash
git clone https://github.com/notpoiu/ytdownloader.git
```
4. After cloning, you need to navigate into the cloned repository:
```bash
cd ytdownloader
```

## Step 3: Installing Required Packages

YTDownloader requires some additional packages to work, which are listed in the `requirements.txt` file. To install them:

1. Ensure you're in the repository directory (`ytdownloader`).
2. Run the following command in your terminal:
```bash
pip install -r requirements.txt
```
This command will automatically install all the required packages for YTDownloader.

---

And that's it! You've successfully set up YTDownloader on your system. If you encounter any issues, feel free to create an issue in the GitHub repository, and someone will assist you.

Happy downloading!
