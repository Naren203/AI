def is_complementary(a, b):
    """Check if two literals are complementary"""
    return (a == "~" + b) or (b == "~" + a)

def resolve(c1, c2):
    """Resolve two clauses"""
    for lit1 in c1:
        for lit2 in c2:
            if is_complementary(lit1, lit2):
                new_clause = set(c1).union(set(c2))
                new_clause.discard(lit1)
                new_clause.discard(lit2)
                return new_clause
    return None

def resolution(kb):
    """Resolution algorithm"""
    new = []
    print("\nStarting Resolution Process...\n")
    while True:
        n = len(kb)
        for i in range(n):
            for j in range(i + 1, n):
                resolvent = resolve(kb[i], kb[j])
                if resolvent is not None:
                    print("Resolving", kb[i], "and", kb[j], "=>", resolvent)
                    if len(resolvent) == 0:
                        print("\n✅ Empty clause derived — contradiction found.")
                        print("✅ Conclusion is PROVED by Resolution.")
                        return True
                    if resolvent not in kb and resolvent not in new:
                        new.append(resolvent)
        if all(cl in kb for cl in new):
            print("\n❌ No new clauses. Cannot prove conclusion.")
            return False
        kb.extend(new)

# -------------------------------
# Take user input
# -------------------------------
num = int(input("Enter number of clauses in Knowledge Base: "))
knowledge_base = []

print("\nEnter each clause as space-separated literals (example: ~P Q):")
for i in range(num):
    clause = input(f"Clause {i+1}: ").strip().split()
    knowledge_base.append(set(clause))

print("\nKnowledge Base (in CNF):")
for clause in knowledge_base:
    print(clause)

# Run resolution
resolution(knowledge_base)


