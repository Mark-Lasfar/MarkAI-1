@router.post("/tracking")
async def track_interaction(
    track_data: schemas.TrackingCreate,
    db: Session = Depends(get_db)
):
    db_track = crud.create_tracking(db, track_data)
    return {"status": "tracked"}