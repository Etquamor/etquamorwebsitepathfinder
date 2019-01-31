__author__ = "Etquamor"
__date__ = "31.01.2019"

import requests
import sys
import argparse


def parameterChecker():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", "-s", help="target site", type=str, required=True)
    parser.add_argument("--pathlist", "-pl", help="pathlist path", type=str)
    parser.add_argument("--extension", "-e", help="extension [Optional]", type=str, required=False)
    parser.add_argument("--adminpanel","-ap", help="Admin panel find parameter [Optional]", action='store_true')
    arguments = parser.parse_args()
    
    if arguments.pathlist and arguments.adminpanel:
        print("\n[#] You cannot use admin panel wordlist and defined wordlist same time!\n")
        exit()
    if arguments.adminpanel:
        pathList = pathlistEditor("wordlists/pathlists/adminPanels.txt", None, False, False)
    else:
        pathList = pathlistEditor(arguments.pathlist, arguments.extension,
                                                    bool(not arguments.pathlist),
                                                        bool(arguments.extension))
    pathFinder(arguments.site, pathList)

def pathlistEditor(pathlistPath, extension, defaultPath=True, extensionDefined=False):
    paths = []
    if defaultPath:
        pathlistPath = "wordlists/pathlists/commonPaths.txt"
    with open(pathlistPath,"r") as pathlistFile:
            
        for i in pathlistFile.readlines():
            if extensionDefined:
                if extension in i.strip():
                    paths.append(i.strip())
                else:
                    paths.append(i.strip()+extension)
            else:
                paths.append(i.strip())
    return paths

def pathFinder(site, pathList, foundPaths = []):
    if not site.endswith("/"):
        site += "/"
    print("\n[#] Total number of loaded paths ==>",len(pathList),"\n")
    try:
        for path in pathList:
            if (pathList.index(path)+1)%150==0:
                print("[*]",pathList.index(path)+1,"paths tried.","Total number of found paths ==>",len(foundPaths),"\n")
            req = requests.get(site+path)
            if req.status_code==200:
                print("[+] Path found! :",path,"\n")
                foundPaths.append(site+path)
            else:
                continue
    except requests.ConnectionError:
        print("\n[!] Connection Error!\n\n[!] Disconnecting...\n")
    except KeyboardInterrupt:
        print("\n[-] Pressed Ctrl+C\n\nQuitting...")
    print(("-"*15)+"\nFound Paths:\n")
    for path in foundPaths:
        print("==>",path)

if __name__=='__main__':
    try:
        parameterChecker()
    except Exception as e:
        print("[-] Unexpected Error!\n[#] Error ==>",e)
        exit()
