##Downloads a github repo
import requests, urllib.parse, zipfile, os.path
import os

class GitZip:
    def __init__(self, url, branch="main"):
        """
        The branch arg is used if not provided in the url. If provided in the url, branch arg is ignored. \n
        Inputs should be one of the following: \n 
        https://github.com/user/repo/tree/branch/ \n
        https://github.com/user/repo/tree/branch \n
        https://github.com/user/repo/ \n
        https://github.com/user/repo \n
        """
        self.OGurl = url #original url
        self.branch = branch
        self.GetRepo = "" #used in GetZipfile
        self.Filename = "" #used in all 3 functions
        self.Size = 0 #zip size
        self.path = "" #download zip path
        URL = urllib.parse.urlparse(url)
        URLPath = URL.path.split('/')
        match len(URLPath):
            case 3:
                URLPath.append("/")
                URLPath[3] = f"archive/{self.branch}"
            case 4:
                URLPath[3] = f"archive/{self.branch}"
            case 5:
                URLPath[3] = "archive"
            case 6:
                URLPath[3] = "archive"
                del URLPath[5]
        self.url = f"{URL.scheme}://{URL.netloc}{'/'.join(URLPath)}.zip/"
        print(f"Converted {self.OGurl} to {self.url}")
    
    def GetZipfile(self): #url is that repo's homepage
        self.GetRepo = requests.get(self.url)
        print(self.GetRepo.status_code)
        self.headers = self.GetRepo.headers
        if not self.Filename: #if filename is "" (empty)
            self.Filename = self.GetRepo.headers["content-disposition"]
            self.Filename = self.Filename[self.Filename.index("=")+1:]
        self.Size = len(self.GetRepo.content)
        print(f"File: {self.Filename}\tSize: {self.Size} bytes (or {int(self.Size)*8} bits!)")
        return self.GetRepo

    def DownloadZip(self, dir=os.path.dirname(__file__)):
        """
        Downloads the zip using the contents of the get request from GetZipfile() \n
        dir decides which directory to put the zip file in
        """
        self.path =  f"{dir}/{self.Filename}"
        with open(self.path, "wb") as z:
            for x in self.GetRepo.iter_content():
                z.write(x)
        print(f"Zip file located at: {self.path}")
        return self.path

    def ExtractZip(self):
        """
        Extracts the zip in the same dir as where the zip is located
        """
        Zip = zipfile.ZipFile(self.path)
        Zip.extractall(path=f"{os.path.dirname(self.path)}/{'.'.join(self.Filename.split(".")[:-1])}")
    
    def DoAll(self, dir=os.path.dirname(__file__)):
        """
        Gets, downloads, and extracts the zip file from github \n
        The filename can be changed via the self.filename variable before calling this method
        """
        self.GetZipfile()
        self.DownloadZip(dir=dir)
        self.ExtractZip()

if __name__ == "__main__":
    GitZip(input("Github Link:")).DoAll()
