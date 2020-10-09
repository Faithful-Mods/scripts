#Important:
This script is made by hand, you need python 3 and those modules to work properly:
```bat
pip install PyGithub
pip install getpass
```

## Paint.NET file :
Don't let Paint.NET file such as .pdn file into this script : they are unsupported and they will make the script crash.

## GitHub API :warning:
You are limited as 5000 pushed files per hour, if you try to upload more than 5k files in a row, GitHub will ban you for 1 hour (until your countdown is reset).
More information here : https://docs.github.com/en/free-pro-team@latest/rest/overview/resources-in-the-rest-api#rate-limiting
> If you have a commit with more than 5k files, please make it in multiple time by hand (you can use GitHub Desktop), this script isn't made to take into account the GitHub API limitation. 