@app.post("/purchase/")
async def create_purchase(user_id: int, amount: float, promocode: Optional[str] = None):
    # Логика обработки покупки
    pass
