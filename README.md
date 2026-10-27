# DSA — Radix Sort (Python)

A **non-comparison** sorting algorithm that sorts integers digit by digit, from the least significant digit to the most significant, using a **stable counting sort** at every pass.

---

## Problem Statement

Given a list of `n` **non-negative** integers, sort it in **ascending order** using Radix Sort (LSD — Least Significant Digit).

**Example**

```
Input:
8
170 45 75 90 802 24 2 66

Output:
2 24 45 66 75 90 170 802
```

---

## Solution

```python
n = int(input())
arr = [int(x) for x in input().split()]

max_val = arr[0]
for x in arr:
    if x > max_val:
        max_val = x

exp = 1
while max_val // exp > 0:
    output = [0] * n
    count = [0] * 10
    
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        
    for i in range(n):
        arr[i] = output[i]
        
    exp *= 10

print(*(arr))
```

---

## The Critical Idea

Radix Sort never compares two elements. Instead it sorts by **one digit at a time**, starting from the ones place:

1. Sort everything by the **ones** digit.
2. Sort everything by the **tens** digit.
3. Sort everything by the **hundreds** digit — and so on, until the largest number's digits are exhausted.

This works because every pass is **stable**: elements with equal digits keep the order from the previous pass. By the time the most significant digit is processed, the earlier passes have already ordered the ties correctly.

The stable per-digit sort is a **counting sort** on a tiny range (digits `0–9`), which is why only a 10-slot `count` list is needed.

---

## How the Loop Works

### Finding the number of passes

```python
exp = 1
while max_val // exp > 0:
    ...
    exp *= 10
```

- `exp` is the place value: `1`, `10`, `100`, ...
- The loop continues while the maximum still has a digit at that position. The number of passes equals the number of digits in `max_val`.

### One counting-sort pass

For each `exp`, the digit of `arr[i]` is `(arr[i] // exp) % 10`.

| Step | Code | Purpose |
|------|------|---------|
| 1. Count | `count[index] += 1` | How many elements have each digit |
| 2. Prefix sum | `count[i] += count[i-1]` | `count[d]` becomes the **end position** for digit `d` |
| 3. Place (right → left) | `output[count[index]-1] = arr[i]; count[index] -= 1` | Puts each element in its slot; going right to left keeps the pass **stable** |
| 4. Copy back | `arr[i] = output[i]` | Prepares the list for the next digit |

---

## Pseudocode

```
RADIX-SORT(arr, n):
    max = maximum of arr
    exp = 1
    while max // exp > 0:
        COUNTING-SORT-BY-DIGIT(arr, n, exp)
        exp = exp * 10

COUNTING-SORT-BY-DIGIT(arr, n, exp):
    count[0..9] = 0
    for i = 0 to n-1:
        count[(arr[i] // exp) % 10] += 1
    for d = 1 to 9:
        count[d] += count[d-1]
    for i = n-1 down to 0:
        d = (arr[i] // exp) % 10
        output[count[d] - 1] = arr[i]
        count[d] -= 1
    copy output back into arr
```

---

## Dry Run

Input: `arr = [170, 45, 75, 90, 802, 24, 2, 66]`, `max_val = 802` (3 digits → 3 passes)

| Pass | exp | Digit of each element (in current order) | List after the pass |
|------|-----|-------------------------------------------|---------------------|
| 1 | 1 | 170→0, 45→5, 75→5, 90→0, 802→2, 24→4, 2→2, 66→6 | `[170, 90, 802, 2, 24, 45, 75, 66]` |
| 2 | 10 | 170→7, 90→9, 802→0, 2→0, 24→2, 45→4, 75→7, 66→6 | `[802, 2, 24, 45, 66, 170, 75, 90]` |
| 3 | 100 | 802→8, 2→0, 24→0, 45→0, 66→0, 170→1, 75→0, 90→0 | `[2, 24, 45, 66, 75, 90, 170, 802]` |

**Output:** `2 24 45 66 75 90 170 802`

Notice that in pass 3 the elements with digit `0` (2, 24, 45, 66, 75, 90) stay in the order created by pass 2. That is stability at work.

---

## Complexity Analysis

Let `n` = number of elements, `d` = number of digits in the maximum, `b` = base (10).

| Case    | Time           | Space     |
|---------|----------------|-----------|
| Best    | O(d · (n + b)) | O(n + b)  |
| Average | O(d · (n + b)) | O(n + b)  |
| Worst   | O(d · (n + b)) | O(n + b)  |

- Each pass costs O(n + b); there are `d` passes.
- With `b = 10` constant, this simplifies to **O(d · n)** — effectively linear when `d` is small.
- **Space:** the `output` list holds `n` elements, and `count` holds 10.
- **Stability:** Radix Sort (with a stable inner sort) is **stable**.

---

## Edge Cases

| Input | Behaviour |
|-------|-----------|
| `n = 1` | One element; one pass per digit, result unchanged |
| All elements single-digit | Exactly one pass |
| Already sorted | Same number of passes — no early exit |
| Duplicates | Sorted correctly and kept in original relative order |
| All zeros | `max_val = 0`, the `while` condition is false immediately; the list is printed as is |
| **Negative numbers** | **Not supported** — a negative `max_val` skips the loop, and negative elements produce wrong digit indexes |
| `n = 0` | `arr[0]` raises an `IndexError` |

Python integers have arbitrary precision, so unlike C++ there is no overflow when `exp` grows.

---

## Code-Quality Notes

- The solution assumes **non-negative integers** and `n ≥ 1`. Guard against an empty list, and handle negatives by separating them, sorting their absolute values, and reversing.
- The manual maximum loop can be replaced with `max(arr)`.
- `(arr[i] // exp) % 10` is computed in two separate loops; that is fine for clarity, but could be cached.
- `output` and `count` are recreated on every pass, which keeps each pass independent and easy to read.
- The final copy loop can be written `arr = output[:]`.
- `print(*(arr))` can be written `print(*arr)`.

---

## Natural Extension

- Extract `counting_sort_by_digit(arr, exp)` as a helper function.
- Use **base 256** or **base 1024** to reduce the number of passes.
- Support negative integers.
- Sort strings or fixed-length keys with **MSD** Radix Sort.

---

## Repository Structure

```
DSA/
└── Sorting/
    └── Radix-Sort/
        ├── radix_sort.py
        └── README.md
```

---

## How to Run

```bash
python radix_sort.py
```

**Sample session**

```
8
170 45 75 90 802 24 2 66
2 24 45 66 75 90 170 802
```

---

## Key Concepts

- **Non-comparison sorting** — breaks the O(n log n) lower bound for comparison sorts
- **LSD (least significant digit) processing**
- **Counting sort as a subroutine** — digit range is only `0–9`
- **Prefix sums** — turn counts into final positions
- **Stability** — the property that makes the digit-by-digit approach correct

---

## Why This Problem Matters

Radix Sort shows that sorting can be done **without comparing elements**, and it underpins many practical systems that sort large sets of integers or fixed-width keys.

| Problem | Concept Used |
|---------|--------------|
| Maximum Gap | Radix sort / bucket idea |
| Sort an Array | Sorting algorithms |
| Sort Integers by The Number of 1 Bits | Custom keys |
| Relative Sort Array | Counting-based ordering |
| H-Index | Counting sort |

---

## Contributing

Contributions are welcome! Fork the repository, create a feature branch, and open a pull request with a short description of the change.

---

## License

This project is licensed under the MIT License.