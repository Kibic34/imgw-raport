from playwright.sync_api import sync_playwright

URL = "https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto(URL, timeout=60000)

    # ✅ czekaj aż tabela się pojawi
    page.wait_for_selector("table", timeout=120000)
    page.wait_for_timeout(5000)

    # ✅ znajdź ikonę drukowania
    print_icon = page.locator("span.pi.pi-print")

    # ✅ debug
    count = print_icon.count()
    print("Znaleziono ikon drukuj:", count)

    if count == 0:
        raise Exception("Nie znaleziono ikony drukowania!")

    # ✅ przejdź do przycisku (rodzica)
    button = print_icon.first.locator("xpath=ancestor::button")

    # ✅ kliknij
    button.click(force=True)

    # ✅ poczekaj aż widok się zmieni
    page.wait_for_timeout(5000)

    # ✅ PDF
    page.pdf(
        path="raport.pdf",
        format="A4",
        print_background=True
    )

    # ✅ debug
    page.screenshot(path="debug.png", full_page=True)

    browser.close()
