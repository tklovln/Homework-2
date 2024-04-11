liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

def getAmountOut(delta_x, x, y):
    return 997*delta_x*y / (1000*x+997*delta_x)

def check_token_reverse_handle(current_token, to):
    tokens=(current_token, to)
    tokens_reverse=(to, current_token)
    if tokens in liquidity:
        t0, t1 = liquidity[tokens]
        return t0, t1
    elif tokens_reverse in liquidity:
        t1, t0 = liquidity[tokens_reverse]
        return t0, t1
    else:
        print("no way")
        return None, None

from itertools import permutations

tokens = ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]

# 生成所有可能的排列组合
all_permutations = permutations(tokens)

# 篩選開頭是tokenB的組合
permu = [perm for perm in all_permutations if perm[0] == "tokenB"]

max_amountIn = 0
max_profit_path = []


for sample_path in permu:
    sample_path = list(sample_path)
    sample_path.append('tokenB')
    # print('sample_path', sample_path)

    amountIn = 5
    current_token='tokenB'
    print("path:", sample_path)
    for pool in sample_path [1:]:
        print(f"swap {current_token}->{pool}")
        reserve0, reserve1 = check_token_reverse_handle(current_token, pool)
        print("amountIn:", amountIn)
        amountIn = getAmountOut(amountIn, reserve0, reserve1)
        print("amountOut", amountIn)
        current_token = pool

    # print(amountIn)
    if amountIn > max_amountIn:
        max_amountIn = amountIn
        max_profit_path = sample_path

print("path: ", end="")
for p in max_profit_path[:-1]:
    print(f"{p}->", end="")
print(f"tokenB, tokenB balance={max_amountIn}.")