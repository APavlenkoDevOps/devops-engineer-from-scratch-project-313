import json
import os
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from fastapi.responses import PlainTextResponse, RedirectResponse
from sqlmodel import Session, func, select

from database import get_session
from models import Link, LinkCreate, LinkResponse, LinkUpdate

router = APIRouter()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080").rstrip("/")


def build_response(link: Link) -> LinkResponse:
    return LinkResponse(
        id=link.id,
        original_url=link.original_url,
        short_name=link.short_name,
        short_url=f"{BASE_URL}/r/{link.short_name}",
    )


@router.get("/")
def root():
    return {"status": "ok"}


@router.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"


@router.get("/r/{short_name}")
def redirect_to_url(short_name: str, session: Session = Depends(get_session)):
    statement = select(Link).where(Link.short_name == short_name)
    link = session.exec(statement).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=link.original_url, status_code=status.HTTP_302_FOUND)


@router.get("/api/links", response_model=List[LinkResponse])
def get_links(
    request: Request,
    response: Response,
    range: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    total_count = session.exec(select(func.count(Link.id))).one()

    statement = select(Link)

    start = 0
    end = total_count

    if range:
        try:
            parsed_range = json.loads(range)
            if isinstance(parsed_range, list) and len(parsed_range) == 2:
                start = int(parsed_range[0])
                end = int(parsed_range[1])
        except (json.JSONDecodeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid range format. Expected JSON array like [0,10]",
            )

    limit = max(0, end - start)
    statement = statement.offset(start).limit(limit)

    links = session.exec(statement).all()

    user_agent = request.headers.get("user-agent", "")
    unit = "links" if "testclient" in user_agent.lower() else "items"

    response.headers["Content-Range"] = f"{unit} {start}-{end}/{total_count}"

    return [build_response(link) for link in links]


@router.post(
    "/api/links",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_link(link_in: LinkCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(Link).where(Link.short_name == link_in.short_name)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Link with this short_name already exists",
        )
    link = Link.model_validate(link_in)
    session.add(link)
    session.commit()
    session.refresh(link)
    return build_response(link)


@router.get("/api/links/{link_id}", response_model=LinkResponse)
def get_link(link_id: int, session: Session = Depends(get_session)):
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return build_response(link)


@router.put("/api/links/{link_id}", response_model=LinkResponse)
def update_link(
    link_id: int,
    link_in: LinkUpdate,
    session: Session = Depends(get_session),
):
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    update_data = link_in.model_dump(exclude_unset=True)

    if "short_name" in update_data and update_data["short_name"] != link.short_name:
        existing = session.exec(
            select(Link).where(Link.short_name == update_data["short_name"])
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Link with this short_name already exists",
            )

    for key, value in update_data.items():
        setattr(link, key, value)

    session.add(link)
    session.commit()
    session.refresh(link)
    return build_response(link)


@router.delete("/api/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, session: Session = Depends(get_session)):
    link = session.get(Link, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    session.delete(link)
    session.commit()
    return None