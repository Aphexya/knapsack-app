from itertools import product

def brute_force_knapsack(weights, values, capacity):
    n = len(weights)
    max_value = 0
    best_combination = ()
    best_weight = 0
    logs = []

    for idx, combination in enumerate(product([0, 1], repeat=n), start=1):
        total_weight = sum(w * x for w, x in zip(weights, combination))
        total_value = sum(v * x for v, x in zip(values, combination))
        status = "✅ Valid" if total_weight <= capacity else "❌ Melebihi kapasitas"

        if total_weight <= capacity and total_value > max_value:
            max_value = total_value
            best_combination = combination
            best_weight = total_weight
            status += " ⬅️ Baru terbaik"

        logs.append({
            'index': idx,
            'combination': combination,
            'weight': total_weight,
            'value': total_value,
            'status': status
        })

    return max_value, best_combination, best_weight, logs
