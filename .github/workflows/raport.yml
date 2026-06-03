from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av")

    # poczekaj aż dane się załadują
    page.wait_for_timeout(15000)

    # ✅ kliknij ikonę "drukuj"
    page.click("button[title='Drukuj']")

    # ✅ poczekaj aż widok się zmieni (bardzo ważne)
    page.wait_for_timeout(5000)

    # ✅ TERAZ generujemy PDF (bez okna systemowego)
    page.pdf(
        path="raport.pdf",
        format="A4",
        print_background=True
    )

    browser.close()
