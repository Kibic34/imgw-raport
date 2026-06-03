from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av")

    # czekaj aż dane się załadują
    page.wait_for_timeout(15000)

    # kliknij ikonę drukowania (ważne!)
    page.click("button[title='Drukuj']")

    # poczekaj na zmianę widoku
    page.wait_for_timeout(5000)

    # zapisz PDF
    page.pdf(path="raport.pdf", format="A4", print_background=True)

    browser.close()
