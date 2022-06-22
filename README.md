# Chrome Driver Manager
Script to detect the current installed Google Chrome version and download its corresponding driver.  
Usefull for keeping the driver up-to-date in a project that uses the Selenium framework with Google Chrome.  



You need Python 3.7+, `requests` and `beautifulsoup4` installed to use this program:

```
pip install requests
```

```
pip install beautifulsoup4
```

Then to run the program:
```
python driver_manager.py
```

## Driver output paths for Windows vs Linux:
Windows: `C:\Users\<your-username>\chromedriver_win32\chromedriver.exe`  
Linux: `/home/<your-username/chromedriver_linux64/chromedriver`  