from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.thread_entity import Thread as ThreadModel
from app.db.app_entity import App as AppModel
from app.models.thread_models import ThreadRead, ThreadCreate

router = APIRouter(prefix="/thread", tags=["thread"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ThreadRead])
def list_threads(db: Session = Depends(get_db)):
    """List all threads"""
    return db.query(ThreadModel).all()

@router.get("/app/{app_id}", response_model=list[ThreadRead])
def list_threads_by_app(app_id: int, db: Session = Depends(get_db)):
    """List all threads for a specific app"""
    # Validate app exists
    app = db.query(AppModel).filter(AppModel.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    threads = db.query(ThreadModel).filter(ThreadModel.app_id == app_id).all()
    return threads

@router.post("/", response_model=ThreadRead, status_code=status.HTTP_201_CREATED)
def create_thread(thread: ThreadCreate, db: Session = Depends(get_db)):
    """Create a new thread for an app"""
    # Validate app exists
    app = db.query(AppModel).filter(AppModel.id == thread.app_id).first()
    if not app:
        raise HTTPException(status_code=400, detail="Invalid app_id: app does not exist")
    
    db_thread = ThreadModel(title=thread.title, app_id=thread.app_id)
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread

@router.get("/{thread_id}", response_model=ThreadRead)
def get_thread(thread_id: int, db: Session = Depends(get_db)):
    """Get a specific thread by ID"""
    thread = db.query(ThreadModel).filter(ThreadModel.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

@router.put("/{thread_id}", response_model=ThreadRead)
def update_thread(thread_id: int, thread_update: ThreadCreate, db: Session = Depends(get_db)):
    """Update a thread"""
    thread = db.query(ThreadModel).filter(ThreadModel.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Validate new app_id exists
    app = db.query(AppModel).filter(AppModel.id == thread_update.app_id).first()
    if not app:
        raise HTTPException(status_code=400, detail="Invalid app_id: app does not exist")
    
    thread.title = thread_update.title
    thread.app_id = thread_update.app_id
    db.commit()
    db.refresh(thread)
    return thread

@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_thread(thread_id: int, db: Session = Depends(get_db)):
    """Delete a thread"""
    thread = db.query(ThreadModel).filter(ThreadModel.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    db.delete(thread)
    db.commit()
    return None
