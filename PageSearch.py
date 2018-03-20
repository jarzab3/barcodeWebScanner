# import logging settings

from settings import logging as log

# import libraries
from urllib.request import urlopen
from urllib.error import *

from urllib.request import urlopen

from bs4 import BeautifulSoup


class PageSearch():

    """Use of this class if for searching through a page for seek relevant data

    Attributes:
        -
        -

    """
    def __init__(self, url):
        self.url = url

        try:
            self.page = urlopen(url)
            # self.session = requests.Session()
            log.debug("Opened url {}".format(url))

        except ConnectionError:
            log.error("Failed to open session.")

        except HTTPError as error:
            log.error("Failed to open session. Error: {}".format(error))

    def __del__(self):
        log.debug("Clean up")
        pass

    def getLinkPdf(self):
        content = self.soup.findAll('div', attrs={"class": "govuk-govspeak direction-ltr"})
        return content

    def parsePage(self):
        self.soup = BeautifulSoup(self.content, 'html.parser')


    def returnAllLinks(self, baseURL, suffix, element, attrType, attrName):

        soup = BeautifulSoup(self.page, "html.parser")

        nameBox = soup.findAll(element, attrs={attrType: attrName})[0]

        mylinks = nameBox.find_all('a', recursive=True)

        ulrsToReturn = []

        for a in mylinks:

            try:
                tempUrl = a.attrs['href']
            except Exception as eror:
                log.error("Url does not have a 'href' attr. Please check this url: {}".format(a))

            if (tempUrl.endswith(suffix,20)):
                if baseURL != "":
                    ulrsToReturn.append(baseURL + tempUrl)
                else:
                    ulrsToReturn.append(tempUrl)

            else:
                print("Additional or not accepted url: {}".format(tempUrl))


        return ulrsToReturn


    def checkUpdates(self, baseURL, suffix, element, attrType, attrName):

        soup = BeautifulSoup(self.page, "html.parser")

        nameBox = soup.findAll(element, attrs={attrType: attrName})[0]

        mylinks = nameBox.find_all('a', recursive=True)

        ulrsToReturn = []

        for a in mylinks:

            try:
                tempUrl = a.attrs['href']
            except Exception as eror:
                log.error("Url does not have a 'href' attr. Please check this url: {}".format(a))

            if (tempUrl.endswith(suffix,20)):
                if baseURL != "":
                    ulrsToReturn.append(baseURL + tempUrl)
                else:
                    ulrsToReturn.append(tempUrl)

            else:

                print("Error while parsing url: {}".format(tempUrl))

        for i in ulrsToReturn:
            print(i)

        return ulrsToReturn
