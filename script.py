from playwright.sync_api import sync_playwright

URL = "https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, timeout=60000)

    # ✅ poczekaj aż tabela się załaduje (kluczowe!)
    page.wait_for_selector("table", timeout=120000)

    # ✅ dodatkowy czas na Angular (ważne na CI)
    page.wait_for_timeout(10000)

    # ✅ screenshot żeby zobaczyć co się dzieje
    page.screenshot(path="debug.png", full_page=True)

    # ✅ generuj PDF BEZ kliknięcia "Drukuj"
    page.pdf(
        path="raport.pdf",
        format="A4",
        print_background=True
    )

    browser.close()
