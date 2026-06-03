from playwright.sync_api import sync_playwright
from datetime import datetime

# ✅ Google Drive
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ✅ Wklej ID folderu z Google Drive (z URL)
FOLDER_ID = "15PTzTmfvPhpTLvV4vrDbG7XEcLfuhKPG"

URL = "https://hydro.imgw.pl/#/list/hydro?rpp=20&pf=0&c=229&cols=c,n,r,ic,csv,csd,tc,wv,dtw,dta,mdf,av"

# =========================
# ✅ POBIERANIE CSV
# =========================

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    print("Otwieranie strony...")
    page.goto(URL, timeout=60000)

    # ✅ czekamy na tabelę
    page.wait_for_selector("table", timeout=120000)
    page.wait_for_timeout(5000)

    # ✅ znajdź ikonę download
    download_icon = page.locator("span.pi.pi-download")

    count = download_icon.count()
    print("Znaleziono ikon download:", count)

    if count == 0:
        raise Exception("Nie znaleziono przycisku CSV!")

    # ✅ przycisk
    button = download_icon.first.locator("xpath=ancestor::button")

    # ✅ nazwa pliku
    today = datetime.now().strftime("%Y.%m.%d")
    filename = f"{today}_RaportIMGW.csv"

    print("Klikam download...")

    # ✅ pobranie pliku
    with page.expect_download() as download_info:
        button.click(force=True)

    download = download_info.value
    download.save_as(filename)

    print(f"Zapisano lokalnie: {filename}")

    browser.close()

# =========================
# ✅ UPLOAD DO GOOGLE DRIVE
# =========================

print("Upload na Google Drive...")

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

service = build("drive", "v3", credentials=creds)

file_metadata = {
    "name": filename,
    "parents": [FOLDER_ID],
    "mimeType": "text/csv"
}

media = MediaFileUpload(filename, mimetype="text/csv")

file = service.files().create(
    body=file_metadata,
    media_body=media,
    fields="id",
    supportsAllDrives=True  # ✅ KLUCZOWE!
).execute()

print(f"✅ Wysłano na Google Drive! ID: {file.get('id')}")
