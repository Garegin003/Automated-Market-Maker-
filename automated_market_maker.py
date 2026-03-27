def simulate_amm_swap(x_reserve, y_reserve, amount_in):
    """
    x_reserve: pool-ում X տոկենի քանակը
    y_reserve: pool-ում Y տոկենի քանակը
    amount_in: որքան X token է swap արվում դեպի Y

    Օգտագործվում է constant product AMM:
    x * y = k
    """

    if x_reserve <= 0 or y_reserve <= 0:
        raise ValueError("Pool reserves must be greater than 0.")

    if amount_in <= 0:
        raise ValueError("Swap amount must be greater than 0.")

    # Սկզբնական invariant
    k = x_reserve * y_reserve

    # Գին swap-ից առաջ
    price_before = y_reserve / x_reserve   # Y per X

    # Նոր reserve-ները swap-ից հետո
    new_x_reserve = x_reserve + amount_in
    new_y_reserve = k / new_x_reserve

    # Օգտատերը ստանում է Y token
    amount_out = y_reserve - new_y_reserve

    # Գին swap-ից հետո
    price_after = new_y_reserve / new_x_reserve   # Y per X

    # Իրական execution price
    execution_price = amount_out / amount_in

    # Price impact / slippage համեմատած swap-ից առաջ spot price-ի հետ
    price_impact_percent = ((price_before - execution_price) / price_before) * 100

    # Spot price-ի փոփոխություն pool-ում
    pool_price_change_percent = ((price_after - price_before) / price_before) * 100

    return {
        "k": k,
        "price_before": price_before,
        "new_x_reserve": new_x_reserve,
        "new_y_reserve": new_y_reserve,
        "amount_out": amount_out,
        "price_after": price_after,
        "execution_price": execution_price,
        "price_impact_percent": price_impact_percent,
        "pool_price_change_percent": pool_price_change_percent,
    }


# ===== Example =====
# Pool:
# ETH = 100
# USDC = 200000
# Swap:
# 10 ETH

x_reserve = 100
y_reserve = 200000
amount_in = 10

result = simulate_amm_swap(x_reserve, y_reserve, amount_in)

print("=== AMM Swap Simulation ===")
print(f"Initial pool: {x_reserve} ETH, {y_reserve} USDC")
print(f"Swap size: {amount_in} ETH")
print()

print(f"k = {result['k']:.6f}")
print(f"Price before: {result['price_before']:.6f} USDC per ETH")
print(f"USDC received: {result['amount_out']:.6f}")
print(f"New pool reserves: {result['new_x_reserve']:.6f} ETH, {result['new_y_reserve']:.6f} USDC")
print(f"Price after: {result['price_after']:.6f} USDC per ETH")
print(f"Execution price: {result['execution_price']:.6f} USDC per ETH")
print(f"Price impact: {result['price_impact_percent']:.6f}%")
print(f"Pool spot price change: {result['pool_price_change_percent']:.6f}%")