# Problem [Chapter].[Number]

!!! info "Textbook Reference"
    - **Textbook**: *[Book Title]* ([Author], [Edition])
    - **Chapter**: [Chapter Number] — [Chapter Title]
    - **Problem**: [Problem Number]
    - **Topic**: [Comma-separated topics / concepts]

---

## Problem Statement

*(Provide a clear, self-contained summary of the problem, given quantities, and target variables. Paraphrase the prompt to respect fair use).*

Given:
- Parameters: ...
- Conditions: ...

Find:
1. ...
2. ...

---

## Solution

### Part 1: [Sub-heading if multi-part]

Detailed step-by-step mathematical derivation:
$$
\mathbf{F} = \frac{d\mathbf{p}}{dt}
$$

Substitute the given relations:
$$
...
$$

---

## Diagrams & Figures (If Applicable)

*(When an exercise requires a custom diagram, free-body diagram, or plot, author it using a paired Python script in the `figures/` subfolder using `docs/templates/diagram-template.py`).*

```markdown
![Figure Description](figures/fig_XX_YY.svg)
*Figure 1: Description of physical setup or trajectory. Source: [`figures/fig_XX_YY.py`](figures/fig_XX_YY.py).*
```

---

## Physical Remarks & Limiting Cases

- **Check Dimensions**: Verify that both sides have units of $[M L T^{-2}]$.
- **Limiting Cases**: What happens as $m \to 0$ or $t \to \infty$?
- **Key Takeaway**: Summary of physical intuition.
