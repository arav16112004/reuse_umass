from typing import Optional, List
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.db.sessions import get_session
from app.models.item import Item
from app.models.request import Request as ItemRequest

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# --- Pages ---

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/my-requests", response_class=HTMLResponse)
async def my_requests_page(request: Request):
    return templates.TemplateResponse("requests.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# --- htmx fragments: items ---

@router.get("/fragments/items/list", response_class=HTMLResponse)
async def list_items_fragment(
    request: Request,
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_session)
):
    stmt = select(Item).where(Item.is_claimed == False)
    if category and category != "All Items":
        stmt = stmt.where(Item.category == category)
    if q:
        stmt = stmt.where((Item.title.ilike(f"%{q}%")) | (Item.description.ilike(f"%{q}%")))
    
    stmt = stmt.order_by(Item.created_at.desc())
    items = db.exec(stmt).all()
    
    return templates.TemplateResponse("fragments/items_list.html", {"request": request, "items": items})

@router.get("/fragments/items/create-form", response_class=HTMLResponse)
async def create_item_form(request: Request):
    return templates.TemplateResponse("fragments/create_item_form.html", {"request": request})

@router.post("/fragments/items/create", response_class=HTMLResponse)
async def create_item(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    condition: str = Form(...),
    location: str = Form(...),
    owner_email: str = Form(...),
    photo_url: Optional[str] = Form(None),
    db: Session = Depends(get_session)
):
    item = Item(
        title=title, description=description, category=category,
        condition=condition, location=location, owner_email=owner_email,
        photo_url=photo_url
    )
    db.add(item)
    db.commit()
    
    # Return success message
    return """
    <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4">
        <strong class="font-bold">Success!</strong>
        <span class="block sm:inline">Item posted successfully.</span>
        <button hx-get="/fragments/items/list" hx-target="#items-container" class="underline mt-2">Refresh List</button>
    </div>
    """

@router.get("/fragments/items/detail/{item_id}", response_class=HTMLResponse)
async def item_detail(request: Request, item_id: int, db: Session = Depends(get_session)):
    item = db.get(Item, item_id)
    return templates.TemplateResponse("fragments/item_detail.html", {"request": request, "item": item})

@router.post("/fragments/items/mark-claimed/{item_id}", response_class=HTMLResponse)
async def mark_claimed(request: Request, item_id: int, db: Session = Depends(get_session)):
    item = db.get(Item, item_id)
    if item:
        item.is_claimed = True
        db.add(item)
        db.commit()
        # return updated detail view
        return templates.TemplateResponse("fragments/item_detail.html", {"request": request, "item": item})
    return "Error: Item not found"

# --- htmx fragments: requests ---

@router.post("/fragments/requests/create", response_class=HTMLResponse)
async def create_request(
    request: Request,
    item_id: int = Form(...),
    requester_email: str = Form(...),
    db: Session = Depends(get_session)
):
    req = ItemRequest(item_id=item_id, requester_email=requester_email)
    db.add(req)
    db.commit()
    return """<div class="text-green-600 font-bold mt-2">✓ Request sent! The owner will contact you.</div>"""

@router.get("/fragments/requests/list", response_class=HTMLResponse)
async def list_requests_fragment(
    request: Request,
    owner_email: Optional[str] = None,
    db: Session = Depends(get_session)
):
    if not owner_email:
        return "Please enter your email to view requests."
        
    stmt = select(ItemRequest, Item).join(Item).where(Item.owner_email == owner_email)
    results = db.exec(stmt).all()
    
    # results is list of (Request, Item) tuples
    requests_data = []
    for req, item in results:
        requests_data.append({"request": req, "item": item})
        
    return templates.TemplateResponse("fragments/requests_list.html", {"request": request, "requests": requests_data})
