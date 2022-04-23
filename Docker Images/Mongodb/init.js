db.createUser(
    {
        user:"tradedev",
        pwd:"tradedev",
        roles: [
            {
                role:"readWrite",
                db: "Trader"
            }
        ]
    }
)