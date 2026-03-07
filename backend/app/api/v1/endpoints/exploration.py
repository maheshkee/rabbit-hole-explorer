from fastapi import APIRouter, HTTPException, Depends, status
from typing import Any
from sqlalchemy.orm import Session
from app.schemas.exploration import (
    ExplorationRequest, 
    ExplorationResponse, 
    ExplorationGraphResponse,
    NodeExpansionResponse
)
from app.services.exploration_service import exploration_service
from app.db.session import get_db

router = APIRouter()

@router.post("/explore", response_model=ExplorationResponse, status_code=status.HTTP_201_CREATED)
async def explore_topic(
    request: ExplorationRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Generate a list of 5 related concepts (a 'rabbit hole') for a given topic
    and persist the resulting graph in the database.
    """
    try:
        result = await exploration_service.generate_rabbit_hole(request.topic, db)
        
        if not result or not result.get("concepts"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not generate concepts at this time."
            )
            
        return ExplorationResponse(
            exploration_id=result["exploration_id"],
            topic=request.topic,
            concepts=result["concepts"]
        )
    except Exception as e:
        # Proper production logging would go here
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/explorations/{exploration_id}", response_model=ExplorationGraphResponse)
async def get_exploration(
    exploration_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve an exploration graph from the database by exploration_id.
    """
    try:
        graph = await exploration_service.get_exploration_graph(exploration_id, db)
        
        if not graph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exploration with ID {exploration_id} not found."
            )
            
        return ExplorationGraphResponse(**graph)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the graph: {str(e)}"
        )

@router.post("/nodes/{node_id}/expand", response_model=NodeExpansionResponse)
async def expand_node(
    node_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Expands an existing node by generating 5 more related concepts.
    """
    try:
        result = await exploration_service.expand_node(node_id, db)
        return NodeExpansionResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while expanding the node: {str(e)}"
        )
