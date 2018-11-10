import bs4, requests, os, re, pyperclip
from selenium import webdriver
from ebooklib import epub

userlink = pyperclip.paste()
driver = webdriver.Chrome()
driver.get(userlink)
# driver.get(userlink + '?depth=1') # ?depth=1 Returns only top level comments

def makefile():
    inHTML = driver.execute_script("return document.body.innerHTML")  # GET DATA FROM SITE
    siteText = bs4.BeautifulSoup(inHTML, 'html.parser')  # PARSE THROUGH BS
    toplevelcomments = siteText.findAll("div", {"class": "md"})
    toplevelcomments.pop(0)

    cleancomments = []
    for i in range(len(toplevelcomments)):
        cleancomments.append(str(toplevelcomments[i]))
    bookready = ''.join(cleancomments)

    title = driver.title
    title = re.sub(r'[^\w\s]','', title)

    # Make Ebook
    book = epub.EpubBook()
    # set metadata
    book.set_identifier('id123456')
    book.set_title(title)
    book.set_language('en')
    book.add_author('Reddit')

    # create chapter
    c1 = epub.EpubHtml(title=title, file_name='chap_01.xhtml', lang='hr')
    c1.content = bookready

    # add chapter
    book.add_item(c1)

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file
    book.add_item(nav_css)

    # basic spine
    book.spine = ['nav', c1]

    # write to the file
    epub.write_epub(title + '.epub', book, {})

makefile()

driver.quit()
