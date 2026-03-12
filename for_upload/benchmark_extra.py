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

def string_replace_approach(target_data):
    # This approach serializes the grid to a string to perform replace operations
    # It might be fast for small grids if we can figure out a trick, but flood fill
    # requires topological connectivity, not just simple replace.
    # We will skip purely string replace as it's algorithmically wrong for flood fill.
    pass

def dict_tuple_approach(target_data):
    # Use a dictionary or set for visited.
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
        visited = set()
        for c in range(W):
            if grid[0][c] == 0: stack.append((0, c))
            if grid[H-1][c] == 0: stack.append((H-1, c))
            
        for r in range(1, H-1):
            if grid[r][0] == 0: stack.append((r, 0))
            if grid[r][W-1] == 0: stack.append((r, W-1))
            
        while stack:
            r, c = stack.pop()
            if (r, c) in visited: continue
            visited.add((r, c))
            
            if r > 0 and grid[r-1][c] == 0: stack.append((r-1, c))
            if r < H-1 and grid[r+1][c] == 0: stack.append((r+1, c))
            if c > 0 and grid[r][c-1] == 0: stack.append((r, c-1))
            if c < W-1 and grid[r][c+1] == 0: stack.append((r, c+1))
            
        for r in range(H):
            row = grid[r]
            for c in range(W):
                val = row[c]
                if val == 0 and (r, c) not in visited:
                    row[c] = 4
                    
        predict_result.append(grid)
    return predict_result

import sys
try:
    import numpy as np
    from scipy.ndimage import binary_fill_holes
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

def scipy_binary_fill_holes(target_data):
    predict_result = []
    for data_i in target_data:
        input_grid = data_i.get("input", [])
        if not input_grid:
            predict_result.append([])
            continue
            
        arr = np.array(input_grid)
        # 3 is wall, 0 is path
        # binary_fill_holes treats False as hole to fill, True as wall
        wall_mask = (arr == 3)
        filled = binary_fill_holes(wall_mask)
        
        # Where it was filled but wasn't originally a wall, it's an enclosed space
        enclosed = filled ^ wall_mask
        
        arr[enclosed] = 4
        predict_result.append(arr.tolist())
    return predict_result

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    
def cv2_floodfill(target_data):
    predict_result = []
    for data_i in target_data:
        input_grid = data_i.get("input", [])
        H = len(input_grid)
        if H == 0:
            predict_result.append([])
            continue
        W = len(input_grid[0])
        
        # cv2 floodfill requires uint8 image and a mask that is H+2, W+2
        arr = np.array(input_grid, dtype=np.uint8)
        mask = np.zeros((H+4, W+4), np.uint8)
        
        # Pad with 0s so outer is all connected.
        padded = np.zeros((H+2, W+2), dtype=np.uint8)
        padded[1:-1, 1:-1] = arr
        
        # Flood fill the padded area with -1 (or e.g. 255) from 0,0
        cv2.floodFill(padded, mask, (0,0), 255)
        
        # Now padded has 255 for outside, 0 for inside enclosed spaces, 3 for walls
        # Reconstruct exactly the inner HxW
        inner = padded[1:-1, 1:-1]
        
        res = []
        for r in range(H):
            row_res = []
            for c in range(W):
                val = inner[r,c]
                if val == 0:
                    row_res.append(4)
                elif val == 255:
                    row_res.append(0)
                else:
                    row_res.append(int(val))
            res.append(row_res)
            
        predict_result.append(res)
    return predict_result

file_path = "train.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

target_data = data.get("train", [])

# Verify
r1 = iterative_fast(target_data)
r2 = dict_tuple_approach(target_data)

assert r1 == r2

if HAS_SCIPY:
    r3 = scipy_binary_fill_holes(target_data)
    assert r1 == r3
    
if HAS_CV2:
    r4 = cv2_floodfill(target_data)
    assert r1 == r4

loop = 10000
sys_time1 = timeit.timeit('iterative_fast(target_data)', globals=globals(), number=loop)
sys_time2 = timeit.timeit('dict_tuple_approach(target_data)', globals=globals(), number=loop)

print(f"iterative_fast: {(sys_time1/loop)*1000000}µs")
print(f"dict_tuple_approach: {(sys_time2/loop)*1000000}µs")

if HAS_SCIPY:
    sys_time3 = timeit.timeit('scipy_binary_fill_holes(target_data)', globals=globals(), number=loop)
    print(f"scipy_binary_fill_holes: {(sys_time3/loop)*1000000}µs")
    
if HAS_CV2:
    sys_time4 = timeit.timeit('cv2_floodfill(target_data)', globals=globals(), number=loop)
    print(f"cv2_floodfill: {(sys_time4/loop)*1000000}µs")
