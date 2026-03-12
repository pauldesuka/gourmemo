import timeit
import json

def iterative_fast(target_data):
    predict_result = []
    for data_i in target_data:
        input_grid = data_i.get("input", [])
        grid = [list(row) for row in input_grid]
        H = len(grid)
        if H == 0: 
            predict_result.append(grid)
            continue
        W = len(grid[0])
        
        stack = []
        for c in range(W):
            if grid[0][c] == 0: stack.append((0, c))
            if grid[H-1][c] == 0: stack.append((H-1, c))
            
        for r in range(1, H-1):
            if grid[r][0] == 0: stack.append((r, 0))
            if grid[r][W-1] == 0: stack.append((r, W-1))
            
        while stack:
            r, c = stack.pop()
            grid[r][c] = -1
            if r > 0 and grid[r-1][c] == 0: stack.append((r-1, c))
            if r < H-1 and grid[r+1][c] == 0: stack.append((r+1, c))
            if c > 0 and grid[r][c-1] == 0: stack.append((r, c-1))
            if c < W-1 and grid[r][c+1] == 0: stack.append((r, c+1))
            
        for r in range(H):
            row = grid[r]
            for c in range(W):
                val = row[c]
                if val == 0:
                    row[c] = 4
                elif val == -1:
                    row[c] = 0
        predict_result.append(grid)
    return predict_result


def bitwise_approach(target_data):
    predict_result = []
    for data_i in target_data:
        input_grid = data_i.get("input", [])
        H = len(input_grid)
        if H == 0:
            predict_result.append([])
            continue
        W = len(input_grid[0])
        
        # Represent wall (3) as 1, path (0) as 0 in an integer bitmask per row
        walls = [0]*H
        for r in range(H):
            row_mask = 0
            for c in range(W):
                if input_grid[r][c] == 3:
                    row_mask |= (1 << c)
            walls[r] = row_mask
            
        # Visited mask
        visited = [0]*H
        
        # stack of (r, c)
        stack = []
        
        # Top and bottom
        for c in range(W):
            if not ((walls[0] >> c) & 1): stack.append((0, c))
            if not ((walls[H-1] >> c) & 1): stack.append((H-1, c))
            
        for r in range(1, H-1):
            if not (walls[r] & 1): stack.append((r, 0))
            if not ((walls[r] >> (W-1)) & 1): stack.append((r, W-1))
            
        while stack:
            r, c = stack.pop()
            if (visited[r] >> c) & 1: continue
            
            # mark visited
            visited[r] |= (1 << c)
            
            # check neighbors
            if r > 0 and not ((walls[r-1] >> c) & 1) and not ((visited[r-1] >> c) & 1): stack.append((r-1, c))
            if r < H-1 and not ((walls[r+1] >> c) & 1) and not ((visited[r+1] >> c) & 1): stack.append((r+1, c))
            if c > 0 and not ((walls[r] >> (c-1)) & 1) and not ((visited[r] >> (c-1)) & 1): stack.append((r, c-1))
            if c < W-1 and not ((walls[r] >> (c+1)) & 1) and not ((visited[r] >> (c+1)) & 1): stack.append((r, c+1))
            
        # Reconstruct
        res = []
        for r in range(H):
            row_res = []
            for c in range(W):
                is_wall = (walls[r] >> c) & 1
                if is_wall:
                    row_res.append(3)
                else:
                    is_vis = (visited[r] >> c) & 1
                    if is_vis:
                        row_res.append(0)
                    else:
                        row_res.append(4)
            res.append(row_res)
        predict_result.append(res)
    return predict_result

file_path = "train.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

target_data = data.get("train", [])

# Verify
r1 = iterative_fast(target_data)
r2 = bitwise_approach(target_data)

assert r1 == r2

loop = 10000
sys_time1 = timeit.timeit('iterative_fast(target_data)', globals=globals(), number=loop)
sys_time2 = timeit.timeit('bitwise_approach(target_data)', globals=globals(), number=loop)

print(f"iterative_fast: {(sys_time1/loop)*1000000}µs")
print(f"bitwise_approach: {(sys_time2/loop)*1000000}µs")
