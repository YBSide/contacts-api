from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()
# Initialize in-memory store
app.state.contacts: List['Contact'] = []
app.state.current_id: int = 1

class Contact(BaseModel):
    id: int
    name: str
    phone: str
    favorite: Optional[bool] = False

class ContactCreate(BaseModel):
    name: str
    phone: str
    favorite: Optional[bool] = False

@app.get("/contacts", response_model=List[Contact])
def get_contacts():
    return app.state.contacts

@app.get("/contacts/favorites", response_model=List[Contact])
def get_favorites():
    return [c for c in app.state.contacts if c.favorite]

# Explicitly disallow DELETE on /contacts/favorites to return 405
@app.delete("/contacts/favorites", status_code=405)
def delete_favorites():
    raise HTTPException(status_code=405, detail="Method Not Allowed")

@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    for c in app.state.contacts:
        if c.id == contact_id:
            return c
    raise HTTPException(status_code=404, detail="Contact not found")

@app.post("/contacts", response_model=Contact, status_code=201)
def create_contact(contact: ContactCreate):
    cid = app.state.current_id
    new_contact = Contact(id=cid, **contact.dict())
    app.state.contacts.append(new_contact)
    app.state.current_id += 1
    return new_contact

@app.delete("/contacts/{contact_id}", status_code=200)
def delete_contact(contact_id: int):
    for i, c in enumerate(app.state.contacts):
        if c.id == contact_id:
            del app.state.contacts[i]
            return {"detail": "Contact deleted"}
    raise HTTPException(status_code=404, detail="Contact not found")