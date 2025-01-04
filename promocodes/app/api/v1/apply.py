@app.post("/api/v1/promocodes/apply/{code}")
def apply_promocode(code: str, db: Session = Depends(get_db)):
    promocode = db.query(PromoCode).filter_by(code=code).first()
    if not promocode:
        raise HTTPException(status_code=404, detail="Промокод не найден")
    promocode.used_count += 1
    db.commit()
    return {"detail": "Промокод успешно применен"}