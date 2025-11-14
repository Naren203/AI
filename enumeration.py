import itertools

def extract_symbols(expr):
    # Extracts unique propositional symbols from the expression
    tokens = expr.replace('(', ' ').replace(')', ' ').replace('not', ' ').replace('and', ' ').replace('or', ' ').replace('==>', ' ').replace('<=>', ' ')
    return sorted(set(token.strip() for token in tokens.split() if token.strip().isalpha()))

def pl_true(expr, model):
    # Evaluates the logical expression with the given model
    try:
        return eval(expr, {}, model)
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return False

def tt_entails(kb_expr, alpha_expr):
    symbols = sorted(set(extract_symbols(kb_expr) + extract_symbols(alpha_expr)))
    all_models = list(itertools.product([False, True], repeat=len(symbols)))
    
    print("\nTruth Table:")
    header = " | ".join(symbols) + " | KB | α"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    result = True
    for values in all_models:
        model = dict(zip(symbols, values))
        kb_val = pl_true(kb_expr, model)
        alpha_val = pl_true(alpha_expr, model)
        row = " | ".join(str(model[symbol]) for symbol in symbols)
        print(f"{row} | {kb_val} | {alpha_val}")
        if kb_val and not alpha_val:
            result = False  # found counter-example

    print("-" * len(header))
    return result

# --- Main Program ---
print("Enter the knowledge base (e.g., P and Q):")
kb = input("KB: ")
print("Enter the query (e.g., P):")
alpha = input("α: ")

# Replace logical connectives for Python evaluation
kb = kb.replace("and", " and ").replace("or", " or ").replace("not", " not ")
alpha = alpha.replace("and", " and ").replace("or", " or ").replace("not", " not ")

# Run entailment check
if tt_entails(kb, alpha):
    print("\n✔️ YES: KB entails α")
else:
    print("\n❌ NO: KB does not entail α")
