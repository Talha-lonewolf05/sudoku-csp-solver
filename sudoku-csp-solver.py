import sys
import copy
from collections import deque


def read_board(file_path):
   
    board = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:                      
                row = [int(ch) for ch in line]
                board.append(row)
    return board


def print_board(board):
   
    print("+-------+-------+-------+")
    for r in range(9):
        row_str = "| "
        for c in range(9):
            val = board[r][c]
            row_str += (str(val) if val != 0 else ".") + " "
            if c in (2, 5):
                row_str += "| "
        row_str += "|"
        print(row_str)
        if r in (2, 5):
            print("+-------+-------+-------+")
    print("+-------+-------+-------+")


def get_peers(row, col):
   
    peers = set()

    for c in range(9):
        if c != col:
            peers.add((row, c))

    for r in range(9):
        if r != row:
            peers.add((r, col))

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r, c) != (row, col):
                peers.add((r, c))

    return peers


PEERS = {
    (r, c): get_peers(r, c)
    for r in range(9)
    for c in range(9)
}


def build_domains(board):
   
    domains = {}

    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                domains[(r, c)] = {board[r][c]}
            else:
                used = {board[pr][pc] for (pr, pc) in PEERS[(r, c)] if board[pr][pc] != 0}
                domains[(r, c)] = set(range(1, 10)) - used

    return domains

def ac3(domains):
   
    queue = deque()
    for cell in domains:
        for peer in PEERS[cell]:
            queue.append((cell, peer))

    while queue:
        xi, xj = queue.popleft()

        if revise(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False           

            for xk in PEERS[xi]:
                if xk != xj:
                    queue.append((xk, xi))

    return True


def revise(domains, xi, xj):

    revised = False
    for val in list(domains[xi]):
        if domains[xj] == {val}:        
            domains[xi].discard(val)
            revised = True
    return revised


def forward_check(domains, cell, value):
    
    pruned = []     

    for peer in PEERS[cell]:
        if value in domains[peer]:
            domains[peer].discard(value)
            pruned.append((peer, value))

            if len(domains[peer]) == 0:
                return False, pruned    

    return True, pruned


def undo_pruning(domains, pruned):
   
    for (cell, val) in pruned:
        domains[cell].add(val)

def select_unassigned_variable(assignment, domains):
   
    unassigned = [cell for cell in domains if cell not in assignment]
    best = min(
        unassigned,
        key=lambda cell: (
            len(domains[cell]),
            -sum(1 for p in PEERS[cell] if p not in assignment)
        )
    )
    return best


def order_domain_values(cell, domains):
    
    def count_conflicts(val):
        return sum(
            1
            for peer in PEERS[cell]
            if val in domains[peer]
        )

    return sorted(domains[cell], key=count_conflicts)

backtrack_calls   = 0
backtrack_failures = 0


def backtrack(assignment, domains):
  
    global backtrack_calls, backtrack_failures
    backtrack_calls += 1

    if len(assignment) == 81:
        return assignment

    cell = select_unassigned_variable(assignment, domains)

    for val in order_domain_values(cell, domains):

        if val not in domains[cell]:
            continue

        assignment[cell] = val
        saved_domain = domains[cell].copy()
        domains[cell] = {val}

        ok, pruned = forward_check(domains, cell, val)

        if ok:
            result = backtrack(assignment, domains)
            if result is not None:
                return result           

        backtrack_failures += 1
        del assignment[cell]
        domains[cell] = saved_domain
        undo_pruning(domains, pruned)

    return None   



def solve(board):
   
    global backtrack_calls, backtrack_failures
    backtrack_calls    = 0
    backtrack_failures = 0

    domains = build_domains(board)

    if not ac3(domains):
        print("  AC-3 detected no solution exists.")
        return None

    assignment = {}
    for cell, dom in domains.items():
        if len(dom) == 1:
            assignment[cell] = next(iter(dom))

    result = backtrack(assignment, domains)

    if result is None:
        return None

    solved_board = [[0] * 9 for _ in range(9)]
    for (r, c), val in result.items():
        solved_board[r][c] = val

    return solved_board


def run_puzzle(label, file_path):
    "\n"
    print(f"  {label} ")

    try:
        board = read_board(file_path)
    except FileNotFoundError:
        print(f"  [ERROR] File '{file_path}' not found. Skipping.")
        return

    print("\n  Original board:")
    print_board(board)

    solution = solve(board)

    if solution:
        print(f"\n  Solved board:")
        print_board(solution)
    else:
        print("\n  No solution found.")

    print(f"\n  Statistics:")
    print(f"    BACKTRACK called  : {backtrack_calls}")
    print(f"    BACKTRACK failures: {backtrack_failures}")

    if backtrack_failures == 0:
        print("    → AC-3 + forward checking solved it with zero backtracking... very easy puzzle")
    elif backtrack_failures < 20:
        print("    → Very few backtracks — puzzle was not too constrained...... likely easy..")
    elif backtrack_failures < 200:
        print("    → Moderate backtracking — typical for medium/hard puzzles.")
    else:
        print("    → Many backtracks — puzzle is highly ambiguous (very hard).")


def main():
    puzzles = [
        ("Easy Board",      "easy.txt"),
        ("Medium Board",    "medium.txt"),
        ("Hard Board",      "hard.txt"),
        ("Very Hard Board", "veryhard.txt"),
    ]

    if len(sys.argv) > 1:
        run_puzzle("Custom Board", sys.argv[1])
        return

    for label, file_path in puzzles:
        run_puzzle(label, file_path)

   
    print("  All puzzles done..........")


if __name__ == "__main__":
    main()