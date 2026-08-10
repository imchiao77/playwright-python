# Playwright Python 自動化測試學習專案

> 建立日期：2026-08-03
> 作者：Elisa Luo
> 環境：macOS Apple Silicon（Mac mini）
> 專案路徑：`/Users/elisaluo/playwright-python`

---

## 📌 專案背景

原本使用 TypeScript 撰寫 Playwright 測試，評估改用 Python 的可行性。
Python 與既有的 Excel 同步腳本（`sync_tc_to_excel.py`）語言一致，維護更方便。

---

## 🔍 TypeScript vs Python 選擇評估

| 考量 | TypeScript | Python |
|------|-----------|--------|
| 已有環境 | ✅ 已建好 | 需補裝 pytest-playwright |
| 搭配 Excel 處理 | 較麻煩 | ✅ pandas 直接用 |
| 搭配 Obsidian 同步腳本 | 需混用 | ✅ 同一語言 |
| 學習資源 | 多 | 多 |
| 官方範例數量 | 較多 | 次之 |

**結論：選擇 Python，統一語言，維護更方便。**

---

## ✅ 環境確認

| 項目 | 版本 | 狀態 |
|------|------|------|
| Python | 3.12.13 | ✅ |
| pip | 26.1.2 | ✅ |
| pytest | 9.1.1 | ✅ |
| Playwright | 1.62.0 | ✅ |
| Chromium 瀏覽器 | 已安裝 | ✅ |

---

## 🛠️ 安裝步驟

### Step 1：建立專案資料夾
```bash
mkdir ~/playwright-python
cd ~/playwright-python
```

### Step 2：建立虛擬環境
```bash
python3 -m venv venv
```

### Step 3：啟動虛擬環境
```bash
source venv/bin/activate
```
> Terminal 開頭出現 `(venv)` 代表啟動成功

### Step 4：安裝 pytest-playwright
```bash
pip install pytest-playwright
```

### Step 5：安裝 Playwright 瀏覽器
```bash
python -m playwright install chromium
```

### Step 6：確認安裝版本
```bash
pip show playwright
python -m pytest --version
```

---

## 📝 每次開始工作前

```bash
# 進入專案資料夾
cd ~/playwright-python

# 啟動虛擬環境
source venv/bin/activate

# 確認 (venv) 出現在 Terminal 開頭即可開始
```

---

## 🧪 測試檔案：test_saucedemo.py

練習目標網站：[https://www.saucedemo.com](https://www.saucedemo.com)

```python
from playwright.sync_api import Page, expect

# 測試一：登入成功
def test_login_success(page: Page):
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

# 測試二：登入失敗（錯誤密碼）
def test_login_fail(page: Page):
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "wrong_password")
    page.click("#login-button")
    expect(page.locator("[data-test='error']")).to_be_visible()

# 測試三：加入購物車
def test_add_to_cart(page: Page):
    # 先登入
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # 加入第一個商品到購物車
    page.click(".btn_inventory:first-of-type")

    # 確認購物車數量顯示 1
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

# 測試四：完整結帳流程
def test_checkout(page: Page):
    # 登入
    page.goto("https://www.saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # 加入商品
    page.click(".btn_inventory:first-of-type")

    # 進入購物車
    page.click(".shopping_cart_link")
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    # 點擊結帳
    page.click("[data-test='checkout']")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    # 填寫收件資訊
    page.fill("[data-test='firstName']", "Elisa")
    page.fill("[data-test='lastName']", "Luo")
    page.fill("[data-test='postalCode']", "10001")
    page.click("[data-test='continue']")

    # 確認訂單頁
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    # 完成訂單
    page.click("[data-test='finish']")
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
```

---

## ▶️ 執行測試指令

```bash
# 執行全部測試
python -m pytest test_saucedemo.py --browser chromium -v

# 執行單一測試
python -m pytest test_saucedemo.py::test_login_success --browser chromium -v

# 執行並顯示瀏覽器畫面（非 headless）
python -m pytest test_saucedemo.py --browser chromium --headed -v
```

---

## ✅ 測試執行結果

| 測試案例 | 結果 | 說明 |
|----------|------|------|
| test_login_success | ✅ PASSED | 正確帳密登入成功 |
| test_login_fail | ✅ PASSED | 錯誤密碼顯示錯誤提示 |
| test_add_to_cart | ✅ PASSED | 購物車數量正確顯示 |
| test_checkout | ✅ PASSED | 完整結帳流程通過 |
| **總執行時間** | **30.50 秒** | 4 passed |

---

## 🏆 已完成里程碑

```
✅ Python 3.12 環境建立
✅ 虛擬環境設定（venv）
✅ pytest-playwright 安裝
✅ Chromium 瀏覽器安裝
✅ 登入測試（成功 / 失敗）
✅ 購物車加入測試
✅ 完整結帳流程測試
✅ 重構為 Page Object Model 架構
✅ 以 `conftest.py` 抽出共用 fixture
```

---

## 🚀 下一步計畫：Page Object Model（POM）

### 目前寫法的問題

每個測試都重複寫登入邏輯，不易維護：

```python
# 每個測試都要重複這三行
page.goto("https://www.saucedemo.com")
page.fill("#user-name", "standard_user")
page.fill("#password", "secret_sauce")
page.click("#login-button")
```

### POM 架構目標

```
playwright-python/
├── venv/
├── pages/
│   ├── login_page.py       ← 登入頁面操作
│   ├── inventory_page.py   ← 商品列表操作
│   ├── cart_page.py        ← 購物車操作
│   └── checkout_page.py    ← 結帳流程操作
├── tests/
│   └── test_saucedemo.py   ← 測試案例（呼叫 pages）
└── conftest.py             ← 共用設定（瀏覽器、登入）
```

### POM 寫法優點

| 項目 | 目前寫法 | POM 寫法 |
|------|----------|----------|
| 程式碼重複 | ❌ 每個測試都重複 | ✅ 集中在 Page Class |
| 維護性 | ❌ 改一個地方要改多處 | ✅ 只改 Page Class |
| 可讀性 | 普通 | ✅ 測試邏輯清晰 |
| 重用性 | 低 | ✅ Page Class 可重複使用 |

---

## 📚 學習資源

| 資源 | 連結 |
|------|------|
| Playwright Python 官方文件 | https://playwright.dev/python/docs/intro |
| pytest 官方文件 | https://docs.pytest.org |
| SauceDemo 練習網站 | https://www.saucedemo.com |

---

*文件維護：Elisa Luo　最後更新：2026-08-03*
