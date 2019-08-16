import requests
import bs4

def getHTML(url):
    """ This functions gets html from the
    parameter url.

    :param url: The url to pull from.
    :type name: string.
    :returns: unstructured HTML.
    """
    # Use requests to get html from API
    html = requests.get(url)

    return (html.text)

def extractFromHTML(url, comp_to_find):
    """ This function extracts url contents using
    beautiful soup.

    :param url: The url to pull from.
    :type name: string.
    :param comp_to_find: The component to find in html code.
    :type comp_to_find: string.
    :returns: Specified HTML contents.
    """
    # Use getHTML to get HTML
    html = getHTML(url)
    # Parse html with bs4
    html_parsed = bs4.BeautifulSoup(html, 'html.parser')
    ## Find component in parsed html code
    comp = html_parsed.find(comp_to_find)

    return (comp)

def extractTickersFromTable(url, comp_to_find):
    """ This function extract tickers from HTML
    table 

    :param url: The url to pull from.
    :type name: string.
    :param comp_to_find: The component to find in html code.
    :type comp_to_find: string.
    :returns: Ticker list.
    """
    # Extract table
    table = extractFromHTML(url, comp_to_find)
    # Extract rows
    rows = table.find_all('a')
    # Extract tickers
    tickers = [el.get('title') for el in rows]
    
    return(tickers)
