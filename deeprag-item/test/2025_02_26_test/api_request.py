import requests



url = "http://localhost:8000/upload_file"

with open("test2.txt","","utf-8") as file:
    content = file.read()