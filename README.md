# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

### What is slippage in AMM?
Slippage in Automated Market Makers (AMMs) refers to the difference between the expected price of a trade and the actual price at which the trade is executed. This discrepancy can occur due to the continuous changes in the asset prices within the AMM's liquidity pool.

### Ｈow does Uniswap V2 address this issue

```
function swapTokensForTokens(
    uint256 amountIn,
    uint256 amountOutMin,
    address[] calldata path,
    address to,
    uint256 deadline
) external returns (uint256[] memory amounts) {
    amounts = UniswapV2Router.getAmountsOut(amountIn, path);
    require(amounts[amounts.length - 1] >= amountOutMin, "UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT");
    UniswapV2Router.swapExactTokensForTokens(
        amountIn,
        amounts[amounts.length - 1],
        path,
        to,
        deadline
    );
}

```


## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution

The rationale behind the minimum liquidity subtraction in the initial liquidity minting process of the UniswapV2Pair contract is to prevent the potential exploitation of the system by users.

When the pool is being initialized, and there is no existing liquidity (_totalSupply == 0), the function calculates the initial liquidity by taking the square root of the product of the two token amounts. However, it then subtracts a constant value MINIMUM_LIQUIDITY from this calculated liquidity and mints those tokens to the zero address, effectively locking them permanently.

The rationale behind this design is to prevent a potential attack known as the "reentrancy attack." In this attack, an attacker could repeatedly call the mint function before the contract updates the reserve values, effectively minting an unlimited number of LP tokens.

By permanently locking a small amount of liquidity (the MINIMUM_LIQUIDITY), the contract ensures that there is always a minimum amount of liquidity in the pool, even if the rest of the liquidity is drained. This makes the pool less vulnerable to reentrancy attacks and other potential exploits.

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution

In the mint function of the UniswapV2Pair contract, the liquidity minting calculation for subsequent deposits (when the total supply is non-zero) is as follows:
```
else {
    liquidity = min(amount0 * _totalSupply / _reserve0, amount1 * _totalSupply / _reserve1);
}
```
This formula ensures that the ratio of the two token amounts in the liquidity pool remains constant, preserving the constant product invariant (x * y = k).

The rationale behind this design is to maintain the constant product invariant, which is a crucial property of the CPMM model used in Uniswap V2. The constant product invariant ensures that the product of the two token reserves in the pool remains constant, which in turn determines the swap price and prevents price slippage.

By using this specific formula, the contract ensures that the new liquidity added to the pool is proportional to the existing reserves, keeping the constant product invariant intact. 

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution

Sandwich attacks are a type of attack that can occur in decentralized exchanges (DEXs) that use Automated Market Makers (AMMs), such as Uniswap V2. The attack aims to exploit the price slippage that can occur during the execution of a user's swap transaction.

The attack works by observing the user's swap transaction in the mempool (the pool of unconfirmed transactions) and then quickly submitting two additional transactions to profit from the price movement. 

First, the attacker will submit a front-running transaction that swaps one of the tokens involved in the user's transaction. This causes the price to move in a direction that is unfavorable to the user. 

After the user's transaction has been executed, the attacker will then submit a back-running transaction to swap the tokens back, profiting from the price movement caused by the user's transaction.

The impact of a sandwich attack on the user initiating the swap can be significant. The user's transaction will experience higher slippage than expected due to the price movement caused by the attacker's transactions. This can result in the user receiving significantly less of the output token than they expected, reducing their overall profit from the swap. Additionally, the user may end up paying higher gas fees due to the additional transactions involved in the sandwich attack.

