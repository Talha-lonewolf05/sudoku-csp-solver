# 🧩 Sudoku Solver using CSP

This project implements a **Constraint Satisfaction Problem (CSP)** based Sudoku solver.

It uses:
- Backtracking Search
- Forward Checking
- AC-3 Algorithm

The solver can handle Sudoku puzzles of different difficulty levels (Easy → Very Hard).

---

## 🚀 Features

- Solves 9x9 Sudoku boards
- Uses AI techniques (CSP)
- Supports multiple difficulty levels
- Reads input from text files
- Efficient constraint propagation

---

## 📂 Input Format

- File must contain **9 lines**
- Each line contains **9 digits (0–9)**
- `0` represents an empty cell

### Example (easy.txt)

004030050
609400000
005100489
000060930
300807002
026040000
453009600
000004705
090050200


---

## 🛠️ Algorithms Used

### 1. Backtracking Search
Basic recursive search to fill Sudoku cells.

### 2. Forward Checking
Removes invalid values from future variables.

### 3. AC-3 Algorithm
Ensures arc consistency to reduce search space.

---

## 📊 Boards Included

- Easy (`easy.txt`)
- Medium (`medium.txt`)
- Hard (`hard.txt`)
- Very Hard (`veryhard.txt`)

---

## ▶️ How to Run

```bash
python main.py easy.txt
