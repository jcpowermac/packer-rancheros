#!/usr/bin/python

# -*- coding: utf-8 -*-
# Joseph Callen

try:
    import sys
    from subprocess import call
    import requests
    import re
    HAS_IMPORTS = True
except ImportError:
    HAS_IMPORTS = False


def parse_checksum(url):
    """Retrieves the contents of the provided url, match using a regex
       and return the first group.

    Args:
        url (str): The url of the iso checksum text file.

    Returns:
        str: The sha256 checksum string 

    """
    result = requests.get(url).content
    match = re.match('^sha256:[ ]*([a-z0-9]*)', result)
    return match.group(1)


def current_version(project):
    """Using the project str request the releases JSON string
       and return the first release url that doesn't 
       include rc in the name or tag_name

    Args:
        project (str): Name of the organization and repository

    Returns:
        str: The release url 

    """
    url = "https://api.github.com/repos/%s/releases" % project
    results = requests.get(url).json()
    for r in results:
        if 'rc' not in r["name"] or 'rc' not in r["tag_name"]:
            return r["url"]


def find_assets(url):
    """Using the url (release) request the dictionary, find the
       assets 'iso-checksum.txt', 'rancheros.iso' and return
       the url for each. 

    Args:
        url (str): The GitHub API release url 

    Returns:
        iso_url (str): The browser download url for the RancherOS ISO
        checksum_url (str): The browser download url for the iso checksum text file

    """
    results = requests.get(url).json()
    for assets in results["assets"]:
        if "iso-checksum" in assets["name"]:
            checksum_url = assets["browser_download_url"]
        elif "rancheros.iso" in assets["name"]:
            iso_url = assets["browser_download_url"]

    return iso_url, checksum_url


def main():

    packer_args = sys.argv[1:]
    # If build is in the packer_args list get the current release details of RancherOS
    # Insert variables into packer command line arguments.
    # This will allow any other packer command line to be passed without modification.
    if 'build' in packer_args:
        url = current_version("rancher/os")
        iso_url, checksum_url = find_assets(url)
        checksum = parse_checksum(checksum_url)
        
        packer_args_length = len(packer_args)
        packer_args[packer_args_length - 1:packer_args_length - 1] = ["-var", "iso_checksum=%s" % checksum]
        packer_args[packer_args_length - 1:packer_args_length - 1] = ["-var", "iso_url=%s" % iso_url]

    packer_args.insert(0, '/opt/hashicorp/bin/packer')
    call(packer_args)

if __name__ == '__main__':
    main()
