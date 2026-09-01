
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
import os, secrets, sqlite3, calendar, hmac

DB=os.environ.get("BUDGET_DB","./budget.db")
APP_PASSWORD=os.environ.get("APP_PASSWORD","change-me")
FRONTEND_ORIGIN=os.environ.get("FRONTEND_ORIGIN","https://wputrick.github.io")

app=FastAPI(title="Household Budget API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["Authorization","Content-Type"],
)

TOKENS=set()

def conn():
    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c

def init_db():
    c=conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS transactions(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      tx_date TEXT NOT NULL,
      description TEXT,
      amount REAL NOT NULL,
      visible_category TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value REAL NOT NULL);
    """)
    defaults={
      "income":7000,
      "target_Groceries":1000,
      "target_General Shopping":500,
      "target_Restaurants / Dining":250,
      "target_Gasoline":250,
      "target_Fixed Essentials":3400
    }
    for k,v in defaults.items():
        c.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)",(k,v))
    c.commit();c.close()

@app.on_event("startup")
def startup(): init_db()

class LoginIn(BaseModel):
    password:str

class TxIn(BaseModel):
    tx_date:str
    description:str
    amount:float
    visible_category:str

def auth(authorization:str|None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401,"Unauthorized")
    token=authorization[7:]
    if token not in TOKENS: raise HTTPException(401,"Unauthorized")

@app.post("/api/login")
def login(payload:LoginIn):
    if not hmac.compare_digest(payload.password,APP_PASSWORD):
        raise HTTPException(401,"Invalid password")
    token=secrets.token_urlsafe(32);TOKENS.add(token)
    return {"token":token}

@app.post("/api/transactions")
def add_tx(payload:TxIn, authorization:str|None=Header(default=None)):
    auth(authorization)
    c=conn()
    c.execute("INSERT INTO transactions(tx_date,description,amount,visible_category) VALUES(?,?,?,?)",
              (payload.tx_date,payload.description,payload.amount,payload.visible_category))
    c.commit();c.close()
    return {"ok":True}

@app.post("/api/demo-seed")
def demo_seed(authorization:str|None=Header(default=None)):
    auth(authorization)
    now=datetime.now()
    month=f"{now.year:04d}-{now.month:02d}"
    rows=[
      (f"{month}-03","ALDI",742.38,"Groceries"),
      (f"{month}-05","Amazon",268.94,"General Shopping"),
      (f"{month}-08","Restaurant",132.16,"Restaurants / Dining"),
      (f"{month}-10","Gas",98.72,"Gasoline"),
      (f"{month}-18","Rent + fixed",3011.43,"Fixed Essentials")
    ]
    c=conn()
    for r in rows:c.execute("INSERT INTO transactions(tx_date,description,amount,visible_category) VALUES(?,?,?,?)",r)
    c.commit();c.close()
    return {"inserted":len(rows)}

@app.get("/api/dashboard")
def dashboard(authorization:str|None=Header(default=None)):
    auth(authorization)
    now=datetime.now()
    month=f"{now.year:04d}-{now.month:02d}"
    c=conn()
    settings={r["key"]:float(r["value"]) for r in c.execute("SELECT key,value FROM settings")}
    rows=c.execute("""SELECT visible_category,SUM(amount) total FROM transactions
                      WHERE substr(tx_date,1,7)=? GROUP BY visible_category""",(month,)).fetchall()
    c.close()
    totals={r["visible_category"]:float(r["total"] or 0) for r in rows}
    income=settings["income"]
    household=sum(totals.values())
    day=max(now.day,1);dim=calendar.monthrange(now.year,now.month)[1]
    projected=household/day*dim if household else 0
    names=["Groceries","General Shopping","Restaurants / Dining","Gasoline","Fixed Essentials"]
    cats=[{"name":n,"spent":totals.get(n,0),"target":settings.get("target_"+n,0)} for n in names]
    return {
      "income":income,
      "householdBurn":household,
      "projected":projected,
      "categories":cats,
      "updatedAt":datetime.now(timezone.utc).isoformat()
    }

@app.get("/api/health")
def health(): return {"ok":True}
