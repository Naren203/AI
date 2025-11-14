# --- Unification helpers ---
def unify(x, y, subst=None):
    if subst is None:
        subst = {}
    if x == y:
        return subst
    elif isinstance(x, str) and x.islower():  # variable (e.g., x)
        return unify_var(x, y, subst)
    elif isinstance(y, str) and y.islower():
        return unify_var(y, x, subst)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for xi, yi in zip(x, y):
            subst = unify(xi, yi, subst)
            if subst is None:
                return None
        return subst
    else:
        return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif x in subst:
        return unify(var, subst[x], subst)
    else:
        new_subst = deepcopy(subst)
        new_subst[var] = x
        return new_subst

def parse_predicate(pred):
    """
    Convert:
        'Human(Socrates)' -> ('Human', ['Socrates'])
        'Rainy' -> ('Rainy', [])
    Handles both with and without parentheses safely.
    """
    pred = pred.strip()
    if "=>" in pred:  # skip full rules, they are handled separately
        return pred, []
    if "(" in pred and ")" in pred:
        parts = pred.rstrip(")").split("(", 1)
        name = parts[0].strip()
        args = [a.strip() for a in parts[1].split(",") if a.strip()]
    else:
        name = pred.strip()
        args = []
    return name, args


# --- Forward chaining ---
def fol_fc_ask(KB, query):
    new = set()
    step = 1
    while True:
        inferred = set()
        for rule in KB:
            if "=>" in rule:
                # Split rule into premises and conclusion
                premises, conclusion = rule.split("=>")
                premises = [p.strip() for p in premises.split("&")]
                conclusion = conclusion.strip()

                # For each fact in KB, try to match premises
                for fact in list(KB):
                    if "=>" in fact:
                        continue  # skip rules
                    for premise in premises:
                        p_name, p_args = parse_predicate(premise)
                        f_name, f_args = parse_predicate(fact)

                        if p_name == f_name:
                            subst = unify(p_args, f_args, {})
                            if subst is not None:
                                c_name, c_args = parse_predicate(conclusion)
                                new_args = [subst.get(a, a) for a in c_args]
                                inferred_fact = (
                                    f"{c_name}({', '.join(new_args)})"
                                    if new_args
                                    else c_name
                                )
                                if inferred_fact not in KB:
                                    print(f"[Step {step}] Inferred: {inferred_fact}")
                                    step += 1
                                    inferred.add(inferred_fact)
                                    if inferred_fact == query:
                                        return True
        if not inferred:
            return False
        KB.update(inferred)


# --- User input section ---
def main():
    print("=== Forward Reasoning Algorithm (First-Order Logic) ===\n")

    n = int(input("Enter number of sentences in the Knowledge Base: "))
    KB = set()

    for i in range(n):
        sentence = input(f"Enter sentence {i+1}: ").strip()
        KB.add(sentence)

    query = input("\nEnter the query: ").strip()

    print("\nRunning inference...\n")
    result = fol_fc_ask(KB, query)

    print("\nResult:", result)
    print("Final Knowledge Base:", KB)


# --- Run program ---
if __name__ == "__main__":
    main()

