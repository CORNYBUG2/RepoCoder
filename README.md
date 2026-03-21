# RepoCoder (Repository-Aware Code Completion)

A simple prototype of a **repository-aware code completion system** inspired by the RepoCoder research paper.

Instead of relying only on the current file, the system retrieves relevant code snippets from the entire repository and uses them as context for an LLM to generate completions.

---

## How it works

Pipeline:

```
Repository
 → Loader
 → File Scanner
 → Sliding Window Snippets
 → Sparse Retrieval (Jaccard similarity)
 → Prompt Builder
 → LLM Generation
```

The retrieved snippets are inserted into the prompt so the model generates code grounded in the project.

---

## Example

Input:

```python
def train_step(x, y):
    output = model(x)
    loss =
```

The system retrieves relevant snippets from the repository and asks the model to complete the code.

---

## Setup

Create environment:

```
conda create -n repoenv python=3.10
conda activate repoenv
```

Install dependencies:

```
pip install torch==2.2.2 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate
```

---

## Run

```
python main.py
```

Optional: pass a custom config or repo path.

```
python main.py --config config/config.yaml
python main.py --repo-path D:/path/to/another/repo
```

---

## Notes

This is a **prototype implementation** of repository-aware retrieval + generation for code. The focus is on the architecture rather than model performance.
