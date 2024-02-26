
def elect_next_budget_item(votes: list[set[str]], balances: list[float], costs: dict[str, float]):
    # setting supporters for each item.
    item_supporters = {item: [] for item in costs.keys()}

    for voter_index, voter_votes in enumerate(votes):
        for item in voter_votes:
            if item in item_supporters:
                item_supporters[item].append(voter_index)

    funding_item = {}
    for item, supporters in item_supporters.items():
        total_balance = sum(balances[i] for i in supporters)
        if total_balance >= costs[item] * len(supporters):  # Check if total balance covers the cost per supporter
            funding_item[item] = total_balance

    if not funding_item:
        print("There's no item can be funded with the current balances")
        return

    # Select the item with the most support that can be funded.
    next_item = max(funding_item.keys(), key=lambda i: (len(item_supporters[i]), -costs[i]))
    supporters = item_supporters[next_item]
    total_cost = costs[next_item]


    supporter_balances = [balances[i] for i in supporters]
    all_balances_similar = len(set(supporter_balances)) == 1

    if all_balances_similar:
        contribution = {i: total_cost for i in supporters}

    else:
        contribution = {}
        for i in supporters:
            contribution[i] = balances[i]

        total_contributions = sum(contribution.values())
        shortfall = total_cost - total_contributions

        if shortfall > 0:
            for i in supporters:
                if balances[i] - contribution[i] > 0:
                    additional_payment = min(balances[i] - contribution[i], shortfall / len(supporters))
                    contribution[i] += additional_payment
                    shortfall -= additional_payment
                    if shortfall <= 0:
                        break

    for i in supporters:
        balances[i] -= contribution[i]

    print(f"Round 1: {next_item} is elected")
    for i in supporters:
        print(f"Citizen {i + 1} pays {contribution[i]:.2f} and has {balances[i]:.2f} remaining balance.")


print("Examples ")

votes = [{'A', 'B', 'C', 'D', 'E'}] * 51 + [{'F', 'G', 'H', 'I', 'J'}] * 49
balances = [5] * 100
costs = {'A': 1.96, 'B': 1.96, 'C': 1.96, 'D': 1.96, 'E': 1.96, 'F': 2.04, 'G': 2.04, 'H': 2.04, 'I': 2.04, 'J': 2.04}

elect_next_budget_item(votes, balances, costs)



votes = [{'A', 'C', 'E'}] + [{'A', 'D'}] + [{'B', 'E'}] + [{'C', 'D', 'F'}]
balances = [7.5] * 4
costs = {'A': 5, 'B': 10, 'C': 5, 'D': 5, 'E': 5, 'F': 10}

elect_next_budget_item(votes, balances, costs)


votes = [{'A', 'D', 'E'}] + [{'A', 'C'}] + [{'B', 'E'}] + [{'C', 'D', 'F'}]
balances = [2.5, 2.5, 7.5, 7.5]
costs = {'A': 5, 'B': 10, 'C': 5, 'D': 5, 'E': 5, 'F': 10}

elect_next_budget_item(votes, balances, costs)