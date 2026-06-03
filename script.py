from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av")

    # ✅ czekaj aż przycisk naprawdę się pojawi
    page.wait_for_selector("button[title='Drukuj']", timeout=120000)

    # ✅ kliknij dopiero wtedy
    page.click("button[title='Drukuj']", force=True)

    # ✅ poczekaj aż coś się zmieni (opcjonalnie lepiej:)
    page.wait_for_load_state("networkidle")

    # ✅ PDF
    page.pdf(
        path="raport.pdf",
        format="A4",
        print_background=True
    )

    browser.close()
