set original_dir=%CD%
set venv_root_dir="C:\Hard - Data\Python\Python - Projects\Hard-Telegram-Bot\venv"
cd %venv_root_dir%
call %venv_root_dir%\Scripts\activate.bat

python telegrambot.py

call %venv_root_dir%\Scripts\deactivate.bat
cd %original_dir%
exit /B 1