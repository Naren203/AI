import ast

def occurs_check(var, expr):
    """Check if variable `var` occurs in expression `expr`."""
    if var == expr:
        return True
    elif isinstance(expr, list):
        return any(occurs_check(var, sub_expr) for sub_expr in expr)
    return False


def apply(subst, expr):
    """Apply a substitution to an expression."""
    if isinstance(expr, str):
        return subst.get(expr, expr)
    elif isinstance(expr, list):
        return [apply(subst, sub_expr) for sub_expr in expr]
    return expr


def apply_substitution(subst):
    """Apply substitution to all existing substitutions."""
    for var in subst:
        subst[var] = apply(subst, subst[var])
    return subst


def unify(x, y, subst=None):
    """Main Unification Algorithm."""
    if subst is None:
        subst = {}

    # Step 1: Variables or constants
    if x == y:
        return subst

    elif isinstance(x, str) and x.islower():  # x is variable
        if occurs_check(x, y):
            return 'FAILURE'
        else:
            subst[x] = y
            return apply_substitution(subst)

    elif isinstance(y, str) and y.islower():  # y is variable
        if occurs_check(y, x):
            return 'FAILURE'
        else:
            subst[y] = x
            return apply_substitution(subst)

    # Step 2: Predicate symbol check
    if isinstance(x, list) and isinstance(y, list):
        if x[0] != y[0]:
            return 'FAILURE'
        if len(x) != len(y):
            return 'FAILURE'

        # Step 5: Unify each argument
        for xi, yi in zip(x[1:], y[1:]):
            subst = unify(apply(subst, xi), apply(subst, yi), subst)
            if subst == 'FAILURE':
                return 'FAILURE'
        return subst

    return 'FAILURE'


# ----------- USER INPUT -------------
print("Enter expressions as Python-style lists, e.g. ['Knows', 'John', 'x']")

try:
    expr1 = ast.literal_eval(input("Enter first expression: "))
    expr2 = ast.literal_eval(input("Enter second expression: "))
except Exception as e:
    print("Invalid input format! Use list-like format such as ['Knows', 'John', 'x']")
    exit()

# ----------- RUN UNIFICATION ----------
result = unify(expr1, expr2)

print("\nUnification Result:", result)
