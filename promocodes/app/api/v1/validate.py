
@app.get("/api/v1/promocodes/validate/{code}")
def validate_promocode(code: str, db: Session = Depends(get_db)):
    promocode = db.query(PromoCode).filter_by(code=code).first()
    if not promocode:
        raise HTTPException(status_code=404, detail="Промокод не найден")
    if not promocode.is_active:
        raise HTTPException(status_code=400, detail="Промокод неактивен")
    if promocode.start_date and datetime.utcnow() < promocode.start_date:
        raise HTTPException(status_code=400, detail="Промокод еще не активен")
    if promocode.end_date and datetime.utcnow() > promocode.end_date:
        raise HTTPException(status_code=400, detail="Срок действия промокода истек")
    if promocode.is_one_time and promocode.used_count >= 1:
        raise HTTPException(status_code=400, detail="Промокод уже использован")
    if promocode.usage_limit and promocode.used_count >= promocode.usage_limit:
        raise HTTPException(status_code=400, detail="Достигнут лимит использований промокода")

    return {
        "code": promocode.code,
        "discount_percent": promocode.discount_percent,
        "fixed_discount": promocode.fixed_discount
    }