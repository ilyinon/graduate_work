@app.post("/api/v1/promocodes/revoke/{code}")
def revoke_promocode(code: str, db: Session = Depends(get_db)):
    promocode = db.query(PromoCode).filter_by(code=code).first()
    if not promocode:
        raise HTTPException(status_code=404, detail="Промокод не найден")
    if promocode.used_count > 0:
        promocode.used_count -= 1
        db.commit()
    return {"detail": "Использование промокода отменено"}