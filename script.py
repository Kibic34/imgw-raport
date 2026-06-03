from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    page.goto("https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av")

    page.wait_for_selector("button[title='Drukuj']", timeout=60000)
    page.click("button[title='Drukuj']")

    page.wait_for_timeout(5000)

    page.pdf(
        path="raport.pdf",
        format="A4",
        print_background=True
    )

    browser.close()
