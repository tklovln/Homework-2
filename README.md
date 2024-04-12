# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

```
profitable path: tokenB->tokenA->tokenE->tokenD->tokenC->tokenB, tokenB balance=20.042339589188174.
swap tokenB->tokenA
amountIn: 5
amountOut 5.655321988655322
swap tokenA->tokenE
amountIn: 5.655321988655322
amountOut 1.0583153138066885
swap tokenE->tokenD
amountIn: 1.0583153138066885
amountOut 2.429786260142227
swap tokenD->tokenC
amountIn: 2.429786260142227
amountOut 5.038996197252911
swap tokenC->tokenB
amountIn: 5.038996197252911
amountOut 20.042339589188174
```
> Solution

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

### What is slippage in AMM?
Slippage in Automated Market Makers (AMMs) refers to the difference between the expected price of a trade and the actual price at which the trade is executed. This discrepancy occurs because AMMs adjust prices based on the ratio of assets in the liquidity pool, and larger trades can cause significant changes in this ratio, resulting in unfavorable prices for the trader.

### Ｈow does Uniswap V2 address this issue?

```
function getAmountOut(uint amountIn, uint reserveIn, uint reserveOut) internal pure returns (uint amountOut) {
    require(amountIn > 0, 'UniswapV2: INSUFFICIENT_INPUT_AMOUNT');
    require(reserveIn > 0 && reserveOut > 0, 'UniswapV2: INSUFFICIENT_LIQUIDITY');
    
    uint amountInWithFee = amountIn.mul(997);
    uint numerator = amountInWithFee.mul(reserveOut);
    uint denominator = reserveIn.mul(1000).add(amountInWithFee);
    amountOut = numerator / denominator;
}
```
This function takes the input amount, the reserves of the input token (reserveIn) and the output token (reserveOut), and calculates the output amount. The formula used here considers the fee (0.3% by default in Uniswap V2), adjusts the input amount accordingly, and then calculates the output amount based on the constant product invariant.

By using this formula, Uniswap V2 minimizes slippage by ensuring that the price impact of trades is proportional to the size of the trade relative to the liquidity in the pool.

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

