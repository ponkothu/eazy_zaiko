from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="在庫管理システム")

# 静的ファイルとテンプレートの設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------- 画面表示用ルート ----------

@app.get("/")
def show_products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return templates.TemplateResponse(request, "products.html", {"products": products})


@app.get("/products/new")
def new_product_form(request: Request):
    return templates.TemplateResponse(request, "product_form.html", {})


@app.post("/products/new")
def create_product_form(
    name: str = Form(...),
    sku: str = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db)
):
    product_data = schemas.ProductCreate(name=name, sku=sku, quantity=quantity, price=price)
    crud.create_product(db, product_data)
    return RedirectResponse(url="/", status_code=303)


@app.post("/products/{product_id}/delete")
def delete_product_form(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, product_id)
    return RedirectResponse(url="/", status_code=303)


# ---------- API(JSON)用ルート ----------

@app.get("/products", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product


@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, quantity: int, db: Session = Depends(get_db)):
    product = crud.update_product(db, product_id, quantity)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return {"message": "削除しました"}