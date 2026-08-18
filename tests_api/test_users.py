"""
JSONPlaceholder /users 端點測試

示範 API 測試的驗證層次：status → 欄位存在 → 型別 → 值 → 錯誤情境。
重點在於避免「只斷言 status 200」的假測試。
"""

import pytest
from playwright.sync_api import APIRequestContext

pytestmark = pytest.mark.api


# 依實際回應歸納出的契約：欄位名稱 -> 預期型別
USER_SCHEMA = {
    "id": int,
    "name": str,
    "username": str,
    "email": str,
    "phone": str,
    "website": str,
    "address": dict,
    "company": dict,
}

ADDRESS_SCHEMA = {
    "street": str,
    "suite": str,
    "city": str,
    "zipcode": str,
    "geo": dict,
}


# ==================== 單筆查詢 ====================

def test_get_user_returns_ok(api: APIRequestContext):
    """GET /users/2 應回傳 200"""
    response = api.get("/users/2")

    assert response.status == 200, f"預期 200，實際 {response.status}"
    assert response.ok


def test_get_user_contains_required_fields(api: APIRequestContext):
    """回應應包含契約定義的所有必要欄位"""
    user = api.get("/users/2").json()

    missing = [field for field in USER_SCHEMA if field not in user]

    assert not missing, f"缺少欄位：{missing}"


def test_get_user_field_types_match_contract(api: APIRequestContext):
    """每個欄位的型別應符合契約"""
    user = api.get("/users/2").json()

    mismatches = {
        field: {"expected": expected.__name__, "actual": type(user[field]).__name__}
        for field, expected in USER_SCHEMA.items()
        if field in user and not isinstance(user[field], expected)
    }

    assert not mismatches, f"型別不符：{mismatches}"


def test_get_user_nested_address_structure(api: APIRequestContext):
    """address 巢狀結構應完整，且 geo 座標為字串型別"""
    address = api.get("/users/2").json()["address"]

    missing = [field for field in ADDRESS_SCHEMA if field not in address]
    assert not missing, f"address 缺少欄位：{missing}"

    # 注意：JSONPlaceholder 的經緯度以字串傳遞，非數值
    # 這類型別選擇是介面對接的常見陷阱，明確測出來以免下游誤用
    geo = address["geo"]
    assert isinstance(geo["lat"], str), f"lat 型別為 {type(geo['lat']).__name__}"
    assert isinstance(geo["lng"], str), f"lng 型別為 {type(geo['lng']).__name__}"

    # 雖為字串，內容應可轉為有效經緯度
    assert -90 <= float(geo["lat"]) <= 90, f"緯度超出範圍：{geo['lat']}"
    assert -180 <= float(geo["lng"]) <= 180, f"經度超出範圍：{geo['lng']}"


def test_get_user_id_matches_request(api: APIRequestContext):
    """回傳的 id 應與請求的路徑參數一致"""
    user = api.get("/users/2").json()

    assert user["id"] == 2, f"請求 id=2，回傳 id={user['id']}"


def test_get_user_email_format(api: APIRequestContext):
    """email 應符合基本格式"""
    email = api.get("/users/2").json()["email"]

    assert "@" in email, f"email 格式異常：{email}"
    assert "." in email.split("@")[-1], f"email 網域異常：{email}"


# ==================== 列表查詢 ====================

def test_get_users_list_returns_all(api: APIRequestContext):
    """GET /users 應回傳 10 筆使用者"""
    users = api.get("/users").json()

    assert isinstance(users, list), f"預期 list，實際 {type(users).__name__}"
    assert len(users) == 10, f"預期 10 筆，實際 {len(users)} 筆"


def test_all_users_conform_to_schema(api: APIRequestContext):
    """列表中每一筆都應符合欄位契約"""
    users = api.get("/users").json()

    problems = []
    for user in users:
        for field, expected in USER_SCHEMA.items():
            if field not in user:
                problems.append(f"id={user.get('id')} 缺少 {field}")
            elif not isinstance(user[field], expected):
                problems.append(
                    f"id={user.get('id')} 的 {field} 型別為 "
                    f"{type(user[field]).__name__}，預期 {expected.__name__}"
                )

    assert not problems, "契約違反：\n" + "\n".join(problems)


def test_user_ids_are_unique(api: APIRequestContext):
    """使用者 id 不應重複"""
    ids = [user["id"] for user in api.get("/users").json()]

    assert len(ids) == len(set(ids)), f"id 重複：{ids}"


# ==================== 錯誤情境 ====================

def test_get_nonexistent_user_returns_404(api: APIRequestContext):
    """查詢不存在的使用者應回傳 404"""
    response = api.get("/users/9999")

    assert response.status == 404, f"預期 404，實際 {response.status}"


@pytest.mark.parametrize(
    "path,description",
    [
        ("/users/abc", "非數字 id"),
        ("/users/-1", "負數 id"),
        ("/users/0", "id 為 0"),
    ],
)
def test_invalid_user_id_does_not_return_success(
    api: APIRequestContext, path: str, description: str
):
    """異常 id 不應回傳 200 與使用者資料"""
    response = api.get(path)

    assert response.status != 200, (
        f"{description}（{path}）意外回傳 200：{response.text()[:100]}"
    )