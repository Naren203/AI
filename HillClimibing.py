import random

# Function to calculate the cost: number of attacking pairs
def cost(state):
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks


# Function to get neighbors by swapping two queens
def get_neighbors(state):
    neighbors = []
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = state[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append((neighbor, (i, j)))  # keep track of which swap was made
    return neighbors


# Hill-Climbing algorithm
def hill_climbing(initial_state):
    current = initial_state
    current_cost = cost(current)
    step = 0

    print(f"Step {step}: {current}, Cost = {current_cost}")

    while True:
        neighbors = get_neighbors(current)
        neighbor_costs = [(n, cost(n), swap) for n, swap in neighbors]

        # Sort neighbors first by cost, then by smallest column index in swap (tie-breaking)
        neighbor_costs.sort(key=lambda x: (x[1], x[2][0], x[2][1]))

        best_neighbor, best_cost, best_swap = neighbor_costs[0]

        if best_cost >= current_cost:
            print(f"\nReached local minimum or goal state.")
            break

        current, current_cost = best_neighbor, best_cost
        step += 1
        print(f"Step {step}: Swap x{best_swap[0]} and x{best_swap[1]} -> {current}, Cost = {current_cost}")

    return current


# Example: Start with given state from slide
initial_state = [3, 1, 2, 0]
solution = hill_climbing(initial_state)

print("\nFinal Solution:", solution)
print("Final Cost:", cost(solution))
