import pafy


def AudioDownloader(url):

    # Xrisimopoioyme to loop se periptosi poy yparxoun perissotera apo ena tragoudia
    # Me me tin methodo new kai thn getbestaudio katebazoume thn kalhterh poothta ixoy apo to YouTube
    # for u in url:
    result = pafy.new(url).getbestaudio().download()