import timeit
import copy

def floodfill(target_data):
    predict_result = []
    
    for data_i in target_data:
        # FastAPI passes dict-like or obj? main.py passes dict directly
        input_grid = data_i.get("input", [])
        
        # Deep copy to avoid modifying original input
        grid = [row[:] for row in input_grid]
        H = len(grid)
        W = len(grid[0]) if H > 0 else 0

        if H == 0 or W == 0:
            predict_result.append(grid)
            continue
            
        stack = []
        
        # Add all border cells to stack
        for r in range(H):
            if grid[r][0] == 0:
                stack.append((r, 0))
            if grid[r][W-1] == 0:
                stack.append((r, W-1))
                
        for c in range(1, W-1):
            if grid[0][c] == 0:
                stack.append((0, c))
            if grid[H-1][c] == 0:
                stack.append((H-1, c))
                
        # Flood fill from border
        while stack:
            r, c = stack.pop()
            if r < 0 or r >= H or c < 0 or c >= W or grid[r][c] != 0:
                continue
            
            # Mark as connected to border
            grid[r][c] = -1
            
            # Add neighbors
            stack.append((r-1, c))
            stack.append((r+1, c))
            stack.append((r, c-1))
            stack.append((r, c+1))
            
        # Second pass: inner 0s become 4, border-connected (-1) become 0
        for r in range(H):
            for c in range(W):
                val = grid[r][c]
                if val == 0:
                    grid[r][c] = 4
                elif val == -1:
                    grid[r][c] = 0
                    
        predict_result.append(grid)
        
    return predict_result

def iterative_fast(target_data):
    predict_result = []
    
    for data_i in target_data:
        input_grid = data_i.get("input", [])
        grid = [list(row) for row in input_grid] # Faster copy
        H = len(grid)
        if H == 0: 
            predict_result.append(grid)
            continue
        W = len(grid[0])
        
        stack = []
        
        # Top and bottom rows
        for c in range(W):
            if grid[0][c] == 0: stack.append((0, c))
            if grid[H-1][c] == 0: stack.append((H-1, c))
            
        # Left and right columns (excluding corners already handled)
        for r in range(1, H-1):
            if grid[r][0] == 0: stack.append((r, 0))
            if grid[r][W-1] == 0: stack.append((r, W-1))
            
        while stack:
            r, c = stack.pop()
            grid[r][c] = -1
            
            # Check neighbors directly without popping invalid ones later
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

import json
file_path = "c:\\Users\\pauld\\OneDrive\\Documents\\test\\competition\\train.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

target_data = data.get("train", [])

# Verification
r1 = floodfill(target_data)
r2 = iterative_fast(target_data)

assert r1 == r2

loop = 10000
sys_time1 = timeit.timeit('floodfill(target_data)', globals=globals(), number=loop)
sys_time2 = timeit.timeit('iterative_fast(target_data)', globals=globals(), number=loop)

print(f"floodfill: {(sys_time1/loop)*1000000}µs")
print(f"iterative_fast: {(sys_time2/loop)*1000000}µs")
