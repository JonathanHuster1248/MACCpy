
# var_om_cost function to return the variable operation and maintainance costs of fuel (fuel) and generation (gen)
# var_om: float representing the cost ($) per unit generation (mwh)
# gen: float representing the generation (mwh)
def var_om_cost(var_om, gen):
    return var_om*gen

# fix_om_cost function to return the fixed operation and maintainance costs of capacity (cap)
# fix_om: float representing the cost ($) per unit capacity (mw)
# cap: float representing the capacity (mw)
def fix_om_cost(fix_om, cap):
    return fix_om*cap

# fuel_cost function to return the fuel costs of fuel_demand amount of fuel
# fuel_price: float representing the cost ($) per unit energy (mmbtu)
# fuel_dem: float representing the fuel demand (mmbtu)
def fuel_cost(fuel_price, fuel_dem):
    return fuel_price*fuel_dem

# fuel_demand function to return the fuel demand of a plant with heat rate heat_rate and generation gen
# heat_rate: float representing efficiency of the plant (heatrate) mmbtu_energy_in/mmbtu_elec_out
# gen: float representing the generation demand (kwh)
# kwh_mmbtu: float representing the unitless conversion (energy/energy) from kwh to mmbtu
def fuel_demand(heat_rate, gen, kwh_mmbtu = 0.00341):
    return gen*kwh_mmbtu*heat_rate

# capital_cost function to return the capital costs of building a plant with capital costs of cap_cost and capacity cap
# cap_cost: float representing capital cost in $/kw
# cap: float representing the capacity of the plant in kw
def capital_cost(cap_cost, cap):
    return cap_cost*cap

# =============================================================================
# # annualize_cost function to return the annualized cost of a lump sum payment with discount rate discount_rate. 
# # cost: float representing lump sum cost to pay off
# # discount_rate: float representing the discount rate of future costs
# # lifetime: float representing the length of payoff lifetime 
# def annualize_cost(cost, discount_rate, lifetime):
#     annuity_factor = (1-(1/((1+discount_rate)**lifetime)))/discount_rate
#     return cost/annuity_factor
# =============================================================================

def interval_payment(capital, rate, lifetime, payments_per_year=1):
    """
    

    Parameters
    ----------
    capital : float
        The initial principle to payoff
    rate : float
        A value (usually ~5% or 0.05) that represents the interest rate charged to the principle annually
    lifetime : float
        The lifetime to payoff the principle (in years)
    payments_per_year : float, optional
        The number of sub payments each year. We assume an annual payment, so the default is 1.

    Returns
    -------
    float
        The regular installment payment. This payment will be paid lifetime*payments_per_year times to be paid off

    """
    # TODO: Make checks that rate isn't 0 or payments per year isn't 0 as it breaks the code
    numerator = rate*capital
    denominator = payments_per_year*(1-(1+rate/payments_per_year)**(-payments_per_year*lifetime))
    return numerator/denominator

def remaining_cost(capital, age, rate, lifetime, payments_per_year=1):
    """
    

    Parameters
    ----------
    capital : float
        The initial principle to payoff
    age : float
        Current age of the plant (in years).
    rate : float
        A value (usually ~5% or 0.05) that represents the interest rate charged to the principle annually
    lifetime : float
        The lifetime to payoff the principle (in years)
    payments_per_year : float, optional
        The number of sub payments each year. We assume an annual payment, so the default is 1.

    Returns
    -------
    remaining_val : float
        value of the original capital that is remaining.

    """
    
    # TODO: Make unit tests that ensure that 0 payments means full capital remaining and full age means no capital remaining 
    # TODO: Error
    payment = interval_payment(capital, rate, lifetime, payments_per_year)
    num_payments = age*payments_per_year
    equivalent_rate = rate/payments_per_year
    
    
    lifetime_cost = capital*(1+equivalent_rate)**(num_payments)
    amount_paid = payment*((1+equivalent_rate)**(num_payments)-1)/(equivalent_rate)
    remaining_val = max(lifetime_cost - amount_paid, 0)
    return remaining_val


# total_cost function to return the total annual cost of running a plant 


def total_cost(var_om, fix_om, fuel_price, capital_cost, discount_rate, lifetime, gen, cap, fuel_dem):
    """[summary]

    Args:
        var_om ([float])       : Variable cost of operations and maintanace $/Mwh
        fix_om ([float])       : Fixed cost of operations and maintanance $/mw
        fuel_price ([float])   : Cost of fuel input $/mmbtu of fuel
        capital_cost ([float]) : Initial capital cost to build plant $/kw
        discount_rate ([float]): Rate of discount for future income/costs (typically between 5% and 20%)
        lifetime ([float])     : Lifetime for the pay off of capital
        gen ([float])          : annual generation of electricity (mwh)
        cap ([float])          : Capacity of plant (mw)
        fuel_dem ([float])     : Demand of fuel (mmbtu)

    Returns:
        [float]: annualized total cost of generation, gen, capacity, cap, fuel demand, fuel_dem, discount rate, and lifetime. 
    """
    return var_om_cost(var_om, gen)+fix_om_cost(fix_om, cap)+fuel_cost(fuel_price, fuel_dem)+interval_payment(capital_cost(capital_cost, cap), discount_rate, lifetime)
