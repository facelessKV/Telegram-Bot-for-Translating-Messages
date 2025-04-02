🌍 Telegram Bot for Translating Messages

Don't want to waste time translating messages manually? This bot will do it for you!
With this bot, you can easily translate text messages into the required language directly in Telegram.

✅ What does it do?

• 🌐 Translates messages into different languages using popular translation APIs
• 🔄 Easily changes user language preferences
• 🗣️ Supports multiple languages for translation
• 📝 Simple and intuitive interface

🔧 Functionality

✅ Fast and accurate text translations
✅ Personalized translation settings for each user
✅ Compatibility with multiple languages, including rare ones

📩 Want all your messages to be translated instantly?

Contact me on Telegram, and I'll help you set up this bot for your business! 🚀

# Instructions for installing and launching the Telegram Translator bot

## Content

1. [Install Python](#1-install-python)
- [Windows](#windows)
   - [Linux](#linux)
2. [Download-bot-code] (#2-download-bot-code)
3. [Virtual Environment Setup](#3-virtual environment setup)
- [Windows](#windows-1)
- [Linux](#linux-1)
4. [Install Dependencies](#4-install dependencies)
- [Windows](#windows-2)
- [Linux](#linux-2)
5. [Getting Tokens](#5-getting-tokens)
- [Telegram Bot Token](#telegram bot token)
   - [API key for the transfer](#api-key-for-translation)
6. [Bot Setup](#6-bot setup)
7. [Bot Launch] (#7-bot launch)
   - [Windows](#windows-3)
- [Linux](#linux-3)
8. [Using the bot](#8-using the bot)
9. [Problem-solving](#9-problem-solving)

## 1. Installing Python

### Windows

1. Download Python 3.9.7 (recommended version) from the official website: https://www.python.org/downloads/release/python-397 /
- Scroll down and select "Windows installer (64-bit)"

2. Run the installer and be sure to check the box "Add Python 3.9 to PATH"
- Click "Install Now" for the standard installation.

3. After installation, check that Python is successfully installed:
- Open the command prompt (press Win+R, type cmd and press Enter)
   - Enter the command: `python --version`
   - You should see something like: `Python 3.9.7`

### Linux

1. Most Linux distributions already contain Python, but it is recommended to install Python 3.9.:

   **Ubuntu/Debian:**
   ```
   sudo apt update
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install python3.9 python3.9-venv python3.9-dev
   ```

   **CentOS/RHEL:**
   ```
   sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel
   wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
   tar xzf Python-3.9.7.tgz
   cd Python-3.9.7
   ./configure --enable-optimizations
   sudo make altinstall
   ```

2. Check the installation with the command:
   ```
   python3.9 --version
   ```

## 2. Downloading the bot code

1. Create a folder where your bot will be located.

   **Windows:**
- Open File Explorer (Win+E)
- Navigate to the location where you want to create a folder (for example, C:\Bots )
- Create a new folder named "TranslatorBot"

   **Linux:**
   ```
   mkdir -p ~/TranslatorBot
   cd ~/TranslatorBot
   ```

2. Copy the bot file (bot.py ) to this folder.

##3. Setting up a virtual environment

The virtual environment allows you to isolate the bot's dependencies from other programs.

### Windows

1. Open the command prompt as an administrator:
   - Press Win
- Type "cmd"
- Right-click on "Command Prompt"
- Select "Run as administrator"

2. Go to the bot folder:
``
   cd C:\путь\к\вашей\папке\TranslatorBot
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
   
   Now `(venv)` should appear at the beginning of the line, which means that the virtual environment is activated.

### Linux

1. Open the terminal and navigate to the folder with the bot:
``
   cd ~/TranslatorBot
   ```

2. Create a virtual environment:
   ```
   python3.9 -m venv venv
   ```

3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

## 4. Installing dependencies

### Windows

1. Make sure that the virtual environment is activated (there should be a `(venv)` at the beginning of the line).

2. Install the necessary libraries:
``
   pip install aiogram>=3.0.0 httpx
   ```

### Linux

1. Make sure that the virtual environment is activated (there should be a `(venv)` at the beginning of the line).

2. Update pip:
``
   pip install --upgrade pip
   ```

3. Install the necessary libraries:
``
   pip install aiogram>=3.0.0 httpx
   ```

##5. Getting tokens

You will need two tokens: for the Telegram bot and for the transfer API.

### Telegram Bot Token

1. Open Telegram and find @BotFather.

2. Send a message to `/newbot'.

3. Follow the instructions:
   - Enter the name of the bot (for example, "My Translator")
- Enter a unique username for the bot (must end with "bot", for example, "my_translator_bot")

4. After creating the bot, you will receive a token similar to:
   ```
   5555555555:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
   ```

5. Keep this token in a safe place.

### API key for the transfer

For Google Translate API:

1. Go to the Google Cloud Console: https://console.cloud .google.com/

2. Create a new project.

3. Enable the Google Cloud Translation API for your project.

4. Create an API key in the "Credentials" section.

5. Save the received key.

##6. Setting up the bot

1. Open the bot file (bot.py ) in any text editor:
   - Windows: you can use Notepad or another editor.
   - Linux: you can use nano, vim or gedit

2. Find the lines:
``python
   API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   TRANSLATE_API_KEY = 'YOUR_TRANSLATE_API_KEY'
   ```

3. Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token received from BotFather.

4. Replace 'YOUR_TRANSLATE_API_KEY' with the translation API key that you received.

5. Save the file.

##7. Launching the bot

### Windows

1. Make sure that you are in the folder with the bot and the virtual environment is activated.

2. Launch the bot with the command:
   ```
   python bot.py
   ```

3. If everything is configured correctly, you will see the logs of the bot launch.

### Linux

1. Make sure that you are in the folder with the bot and the virtual environment is activated.

2. Launch the bot with the command:
   ```
   python3 bot.py
   ```

3. To run the bot in the background (so that it continues to work after closing the terminal):
   ```
   nohup python3 bot.py > bot.log 2>&1 &
   ```

##8. Using a bot

1. Find your Telegram bot by the name you specified when creating it.

2. Send the `/start` command to receive a welcome message and information about the available commands.

3. Use the following commands:
   - `/translate' — text translation request
   - '/set_lang' — change the translation language
- Or just send any text, and the bot will automatically detect the language and translate it

## 9. Problem solving

**The problem:** When starting the bot, the error "No module named 'aiogram'" appears.
**Solution:** Make sure that you have activated the virtual environment and installed all dependencies (`pip install aiogram>=3.0.0 httpx').

**The problem:** The "Invalid token" error occurred when launching the bot.
**Solution:** Make sure that you copied the BotFather token correctly to the file. bot.py .

**The problem:** The error is "Unauthorized" when trying to translate the text.
**Solution:** Verify that the API key for the transfer is correct and make sure that the API is activated in the Google Cloud console.

**The problem:** The bot does not respond to commands.
**Solution:** Check the bot startup logs for errors. Make sure that the bot is up and running.

---

If you have any questions or problems not listed in this guide, please refer to the aiogram documentation: https://docs.aiogram.dev/
