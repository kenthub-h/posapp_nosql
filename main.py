from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じてNext.jsのURLに制限できます（例: ["http://localhost:3000"]）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 簡易的な商品データ（辞書で代替）
product_master = {
    "001": {"code": "001", "name": "サッポロ生ビール黒ラベル", "price": 250},
    "002": {"code": "002", "name": "サッポロクラシック", "price": 280},
    "003": {"code": "003", "name": "サッポロラガービール", "price": 300},
    "004": {"code": "004", "name": "ヱビスビール", "price": 320},
    "005": {"code": "005", "name": "サッポロ プレミアムアルコールフリー", "price": 150},
}

# 商品情報を格納するモデル
class Product(BaseModel):
    code: str
    name: str
    price: int

# 購入情報を格納するモデル
class Purchase(BaseModel):
    emp_cd: str
    items: List[Product]

# 商品マスタ検索API
@app.get("/product/{code}")
def get_product(code: str):
    product = product_master.get(code.strip())
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 購入API
@app.post("/purchase")
def purchase(purchase: Purchase):
    total_amount = 0
    for item in purchase.items:
        product = product_master.get(item.code)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with code {item.code} not found")
        total_amount += product["price"]

    return {"transaction_id": "dummy_trx_id", "total_amount": total_amount}
