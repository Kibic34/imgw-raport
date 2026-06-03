from playwright.sync_api import sync_playwright

URL = "https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # na CI musi być True
    context = browser.new_context()
    page = context.new_page()

    page.goto(URL, timeout=60000)

    # ✅ poczekaj aż Angular wyrenderuje UI
    page.wait_for_load_state("networkidle")

    # ✅ spróbuj różnych selektorów (bardziej odporne)
    try:
        page.wait_for_selector("button[title='Drukuj']", timeout=60000)
        page.click("button[title='Drukuj']")
    except:
        # fallback jeśli selector jest inny
        page.locator("button:has-text('Drukuj')").first.click()

    # ✅ poczekaj na widok do druku
    page.wait_for_timeout(5000)

    # ✅ screenshot do debugowania (WAŻNE na GitHub Actions)
    page.screenshot(path="debug.png", full_page=True)

    # ✅ generowanie PDF
    page.pdf(
        path="raport.pdf",
        format="A4",
        print_background=True
    )

    browser.close()
``
