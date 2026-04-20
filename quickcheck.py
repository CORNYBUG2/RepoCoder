import os


# -----------------------------
# 1. LOAD FILES
# -----------------------------
def load_files(repo_path):
    files = []
    for root, _, filenames in os.walk(repo_path):
        for f in filenames:
            if f.endswith(".py"):  # only python files
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as file:
                    files.append({
                        "path": path,
                        "content": file.read()
                    })
    return files


# -----------------------------
# 2. SCAN FILES
# -----------------------------
def scan_files(files):
    scanned = []
    for f in files:
        if len(f["content"].strip()) > 0:  # ignore empty files
            scanned.append(f)
    return scanned


# -----------------------------
# 3. CHUNK FILES
# -----------------------------
def chunk_files(files, window_size=20, step_size=10):
    snippets = []

    for f in files:
        lines = f["content"].split("\n")

        for i in range(0, len(lines), step_size):
            chunk = lines[i:i + window_size]
            if chunk:
                snippets.append({
                    "content": "\n".join(chunk),
                    "source": f["path"]
                })

    return snippets


# -----------------------------
# 4. RETRIEVE (simple keyword match)
# -----------------------------
def retrieve(snippets, query, top_k=3):
    scored = []

    for s in snippets:
        score = sum(word in s["content"] for word in query.split())
        scored.append((score, s))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [s for _, s in scored[:top_k]]


# -----------------------------
# 5. BUILD PROMPT
# -----------------------------
def build_prompt(query, retrieved_snippets):
    context = "\n\n".join([s["content"] for s in retrieved_snippets])

    prompt = f"""
You are a code assistant.

Complete the following code:

{query}

Use the following context if helpful:

{context}

Return only code.
"""
    return prompt


# -----------------------------
# 6. GENERATE (dummy instead of LLM)
# -----------------------------
def generate(prompt):
    # replace with actual LLM call later
    return "loss = compute_loss(output, y)\nreturn loss"


# -----------------------------
# 7. STOP CONDITION
# -----------------------------
def should_stop(prev, curr, iteration, max_iter):
    if iteration >= max_iter:
        return True
    if prev == curr:
        return True
    return False


# -----------------------------
# 8. IMPROVE QUERY
# -----------------------------
def improve_query(original_query, output):
    return original_query + "\n# previous attempt:\n" + output


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():

    repo_path = "./"  # current folder

    # STEP 1 → LOAD
    files = load_files(repo_path)

    # STEP 2 → SCAN
    scanned_files = scan_files(files)

    # STEP 3 → CHUNK
    snippets = chunk_files(scanned_files)

    # STEP 4 → INPUT CODE
    query = """
def train_step(x, y):
    output = model(x)
    loss =
"""

    previous_output = None
    max_iterations = 2

    # STEP 5 → ITERATIVE LOOP
    for iteration in range(1, max_iterations + 1):

        # retrieve relevant code
        results = retrieve(snippets, query)

        # build prompt
        prompt = build_prompt(query, results)

        # generate answer
        output = generate(prompt)

        # stop check
        if should_stop(previous_output, output, iteration, max_iterations):
            break

        # improve query
        query = improve_query(query, output)
        previous_output = output

    # STEP 6 → OUTPUT
    print(output)


# ENTRY POINT
if __name__ == "__main__":
    main()