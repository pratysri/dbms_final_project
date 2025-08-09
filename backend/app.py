from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr, conint, condecimal
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from db import get_conn

app = FastAPI(title="DBMS Final API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Pydantic models
# -------------------------
class ProductIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    stock_qty: conint(ge=0)

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    stock_qty: int
    active: bool

class CustomerIn(BaseModel):
    name: str
    email: EmailStr

class CustomerOut(BaseModel):
    id: int
    name: str
    email: EmailStr

class CreditCardIn(BaseModel):
    customer_id: int
    brand: str
    last4: str = Field(..., min_length=4, max_length=4)
    exp_month: conint(ge=1, le=12)
    exp_year: conint(ge=2024)
    token: str

class PurchaseItemIn(BaseModel):
    product_id: int
    qty: conint(gt=0)

class PurchaseIn(BaseModel):
    customer_id: int
    items: List[PurchaseItemIn]

class PurchaseOut(BaseModel):
    id: int
    customer_id: int
    purchased_at: datetime
    total_amount: Decimal
    status: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)] = None
    stock_qty: Optional[conint(ge=0)] = None

class ActiveUpdate(BaseModel):
    active: bool

class ProductLowStockOut(BaseModel):
    id: int
    name: str
    stock_qty: int

class PurchaseItemOut(BaseModel):
    product_id: int
    product_name: str
    qty: int
    unit_price: Decimal

class PurchaseDetailOut(BaseModel):
    id: int
    customer_id: int
    purchased_at: datetime
    total_amount: Decimal
    status: str
    items: List[PurchaseItemOut]

# -------------------------
# Endpoints
# -------------------------

@app.get("/products", response_model=List[ProductOut])
def list_products(search: Optional[str] = None, min_price: Optional[Decimal] = None, max_price: Optional[Decimal] = None):
    q = "SELECT id, name, description, price, stock_qty, active FROM product WHERE active = TRUE"
    params = []
    if search:
        q += " AND name ILIKE %s"
        params.append(f"%{search}%")
    if min_price is not None:
        q += " AND price >= %s"
        params.append(min_price)
    if max_price is not None:
        q += " AND price <= %s"
        params.append(max_price)
    q += " ORDER BY price ASC, name ASC"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(q, params)
        return cur.fetchall()

@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate):
    fields = []
    params = []
    if payload.name is not None:
        fields.append("name = %s")
        params.append(payload.name)
    if payload.description is not None:
        fields.append("description = %s")
        params.append(payload.description)
    if payload.price is not None:
        fields.append("price = %s")
        params.append(payload.price)
    if payload.stock_qty is not None:
        fields.append("stock_qty = %s")
        params.append(payload.stock_qty)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    params.append(product_id)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            f"UPDATE product SET {', '.join(fields)} WHERE id = %s RETURNING id, name, description, price, stock_qty, active",
            params,
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        return row

@app.patch("/products/{product_id}/active", response_model=ProductOut)
def set_product_active(product_id: int, payload: ActiveUpdate):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE product SET active = %s WHERE id = %s RETURNING id, name, description, price, stock_qty, active",
            (payload.active, product_id),
        )
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        return row

@app.get("/products/low_stock", response_model=List[ProductLowStockOut])
def low_stock(threshold: int = 5):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, stock_qty FROM product WHERE stock_qty < %s ORDER BY stock_qty ASC",
            (threshold,),
        )
        return cur.fetchall()

@app.post("/products", response_model=ProductOut, status_code=201)
def add_product(payload: ProductIn):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO product(name, description, price, stock_qty) VALUES (%s,%s,%s,%s) RETURNING id, name, description, price, stock_qty, active",
            (payload.name, payload.description, payload.price, payload.stock_qty),
        )
        return cur.fetchone()

@app.post("/customers", response_model=CustomerOut, status_code=201)
def add_customer(payload: CustomerIn):
    with get_conn() as conn, conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO customer(name, email) VALUES (%s,%s) RETURNING id, name, email",
                (payload.name, payload.email),
            )
        except Exception as e:
            # likely duplicate email
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        return cur.fetchone()

@app.get("/customers/{customer_id}/credit_cards")
def list_credit_cards(customer_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, customer_id, brand, last4, exp_month, exp_year, created_at
            FROM credit_card
            WHERE customer_id = %s
            ORDER BY created_at DESC
            """,
            (customer_id,),
        )
        return cur.fetchall()

@app.post("/credit_cards", status_code=201)
def add_credit_card(payload: CreditCardIn):
    with get_conn() as conn, conn.cursor() as cur:
        # simple validation for brand set; rely on DB constraint too
        if payload.brand not in ("Visa","Mastercard","Amex","Discover"):
            raise HTTPException(status_code=400, detail="Unsupported brand")
        cur.execute(
            """INSERT INTO credit_card(customer_id, brand, last4, exp_month, exp_year, token)
               VALUES (%s,%s,%s,%s,%s,%s)
               RETURNING id""",
            (payload.customer_id, payload.brand, payload.last4, payload.exp_month, payload.exp_year, payload.token),
        )
        return {"id": cur.fetchone()["id"]}

@app.post("/purchases", response_model=PurchaseOut, status_code=201)
def create_purchase(payload: PurchaseIn):
    if not payload.items:
        raise HTTPException(status_code=400, detail="At least one item is required")
    with get_conn() as conn, conn.cursor() as cur:
        try:
            # lock rows to prevent race on stock
            product_ids = tuple({it.product_id for it in payload.items})
            cur.execute(f"SELECT id, price, stock_qty FROM product WHERE id IN %s AND active = TRUE FOR UPDATE", (product_ids,))
            products = {row["id"]: row for row in cur.fetchall()}

            # validate stock and compute total
            total = Decimal("0.00")
            for it in payload.items:
                if it.product_id not in products:
                    raise HTTPException(status_code=400, detail=f"Product {it.product_id} not found/active")
                if products[it.product_id]["stock_qty"] < it.qty:
                    raise HTTPException(status_code=400, detail=f"Insufficient stock for product {it.product_id}")
                total += (products[it.product_id]["price"] * it.qty)

            # create purchase
            cur.execute("INSERT INTO purchase(customer_id, total_amount) VALUES (%s,%s) RETURNING id, customer_id, purchased_at, total_amount, status",
                        (payload.customer_id, total))
            purchase = cur.fetchone()
            pid = purchase["id"]

            # insert items & reduce stock
            for it in payload.items:
                price_now = products[it.product_id]["price"]
                cur.execute("""INSERT INTO purchase_item(purchase_id, product_id, qty, unit_price)
                               VALUES (%s,%s,%s,%s)""", (pid, it.product_id, it.qty, price_now))
                cur.execute("UPDATE product SET stock_qty = stock_qty - %s WHERE id = %s", (it.qty, it.product_id))

            return purchase
        except HTTPException:
            raise
        except Exception as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/purchases/{purchase_id}", response_model=PurchaseDetailOut)
def get_purchase_detail(purchase_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, customer_id, purchased_at, total_amount, status FROM purchase WHERE id = %s",
            (purchase_id,),
        )
        purchase = cur.fetchone()
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        cur.execute(
            """
            SELECT p.id AS product_id, p.name AS product_name, pi.qty, pi.unit_price
            FROM purchase_item pi
            JOIN product p ON p.id = pi.product_id
            WHERE pi.purchase_id = %s
            ORDER BY p.name ASC
            """,
            (purchase_id,),
        )
        items = cur.fetchall()
        purchase["items"] = items
        return purchase

@app.get("/customers/{customer_id}/purchases")
def get_customer_purchases(customer_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT pu.id, pu.purchased_at, pu.total_amount, pu.status
            FROM purchase pu
            WHERE pu.customer_id = %s
            ORDER BY pu.purchased_at DESC
        """, (customer_id,))
        purchases = cur.fetchall()

        # Optionally include items per purchase (kept simple)
        return purchases

@app.get("/")
def root():
    return {"ok": True, "message": "DBMS Final API running"}
