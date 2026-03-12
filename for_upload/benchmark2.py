import timeit
import copy
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

def flat_1d(target_data):
    predict_result = []
    for data_i in target_data:
        input_grid = data_i.get("input", [])
        H = len(input_grid)
        if H == 0:
            predict_result.append(input_grid)
            continue
        W = len(input_grid[0])
        
        # Flatten to 1D
        grid = [val for row in input_grid for val in row]
        
        stack = []
        # Top and bottom
        for c in range(W):
            if grid[c] == 0: stack.append(c)
            idx = (H-1)*W + c
            if grid[idx] == 0: stack.append(idx)
            
        # Left and right
        for r in range(1, H-1):
            idx = r*W
            if grid[idx] == 0: stack.append(idx)
            idx = r*W + W - 1
            if grid[idx] == 0: stack.append(idx)
            
        while stack:
            idx = stack.pop()
            grid[idx] = -1
            r = idx // W
            c = idx % W
            
            if r > 0 and grid[idx-W] == 0: stack.append(idx-W)
            if r < H-1 and grid[idx+W] == 0: stack.append(idx+W)
            if c > 0 and grid[idx-1] == 0: stack.append(idx-1)
            if c < W-1 and grid[idx+1] == 0: stack.append(idx+1)
            
        # Unflatten and map back
        res = []
        for r in range(H):
            row_res = []
            for c in range(W):
                val = grid[r*W+c]
                if val == 0:
                    row_res.append(4)
                elif val == -1:
                    row_res.append(0)
                else:
                    row_res.append(val)
            res.append(row_res)
        predict_result.append(res)
    return predict_result

def in_place_mutate_original(target_data):
    # Depending on rules, we might mutate the dictionary. The original function didn't.
    # We will do a fast copy first.
    predict_result = []
    for data_i in target_data:
        # Instead of generic deepcopy, construct new lists directly.
        # But wait, we can just build the output from a boolean visited matrix, or just do the 2D array list-comp.
        input_grid = data_i.get("input", [])
        H = len(input_grid)
        if H == 0:
            predict_result.append([])
            continue
        W = len(input_grid[0])
        
        grid = [row[:] for row in input_grid]
        stack = []
        
        for c in range(W):
            if grid[0][c] == 0: stack.append((0, c))
            if grid[H-1][c] == 0: stack.append((H-1, c))
            
        for r in range(1, H-1):
            if grid[r][0] == 0: stack.append((r, 0))
            if grid[r][W-1] == 0: stack.append((r, W-1))
            
        # Using pop/append is faster in python list than deque for small data.
        while stack:
            r, c = stack.pop()
            grid[r][c] = -1
            
            # Unrolled neighbors
            if r > 0 and grid[r-1][c] == 0: stack.append((r-1, c))
            if r < H-1 and grid[r+1][c] == 0: stack.append((r+1, c))
            if c > 0 and grid[r][c-1] == 0: stack.append((r, c-1))
            if c < W-1 and grid[r][c+1] == 0: stack.append((r, c+1))
            
        # Direct mutation pass over grid is very fast
        for r in range(H):
            row = grid[r]
            for c in range(W):
                if row[c] == 0:
                    row[c] = 4
                elif row[c] == -1:
                    row[c] = 0
                    
        predict_result.append(grid)
    return predict_result

file_path = "c:\\Users\\pauld\\OneDrive\\Documents\\test\\competition\\train.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

target_data = data.get("train", [])

# Verify
r1 = iterative_fast(target_data)
r2 = flat_1d(target_data)
r3 = in_place_mutate_original(target_data)

assert r1 == r2 == r3

loop = 10000
sys_time1 = timeit.timeit('iterative_fast(target_data)', globals=globals(), number=loop)
sys_time2 = timeit.timeit('flat_1d(target_data)', globals=globals(), number=loop)
sys_time3 = timeit.timeit('in_place_mutate_original(target_data)', globals=globals(), number=loop)

print(f"iterative_fast: {(sys_time1/loop)*1000000}µs")
print(f"flat_1d: {(sys_time2/loop)*1000000}µs")
print(f"in_place_mutate_original: {(sys_time3/loop)*1000000}µs")
