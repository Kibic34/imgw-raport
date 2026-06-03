from playwright.sync_api import sync_playwright

URL = "https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    print("Otwieranie strony...")
    page.goto(URL, timeout=60000)

    # ✅ czekamy aż tabela się załaduje
    page.wait_for_selector("table", timeout=120000)

    # ✅ dodatkowy bufor (Angular)
    page.wait_for_timeout(5000)

    # ✅ znajdź ikonę download
    download_icon = page.locator("span.pi.pi-download")

    count = download_icon.count()
    print("Znaleziono ikon download:", count)

    if count == 0:
        raise Exception("Nie znaleziono przycisku CSV!")

    # ✅ przejdź do przycisku
    button = download_icon.first.locator("xpath=ancestor::button")

    # ✅ pobierz plik
    print("Klikam przycisk download...")
    with page.expect_download() as download_info:
        button.click(force=True)

    download = download_info.value

    # ✅ zapisz plik
    download.save_as("raport.csv")
    print("Zapisano raport.csv")

    browser.close()
