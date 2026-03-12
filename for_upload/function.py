from fastapi import FastAPI
from pydantic import BaseModel, field_validator, ValidationError
from typing import List

app = FastAPI()

class PredictionResponse(BaseModel):
    predict: List[List[List[int]]]

    @field_validator('predict')
    @classmethod
    def check_not_empty(cls, v):
        if not v:
            raise ValueError("predict must contain at least one element.")
        return v

@app.post("/predict")
def function(target_data):

    """
    Args:
        - "input": 画像の 2次元リスト (高さ H × 幅 W)。
            例: [[pixel, pixel, ...], [pixel, pixel, ...]]
            ※ pixelには、0, 3(壁) が入ります
        - "output": 目的値(inputと同じ型) ※答え確認用

    Returns:
        predict_result: 予測結果のリスト。予測結果(inputと同じ型)を順番に格納
        ※塗りつぶす位置で、inputの0を4に変更
    """
    
    import numpy as np
    import cv2
    
    predict_result = []
    
    for data_i in target_data:
        input_grid = data_i.get('input', []) 
        
        H = len(input_grid)
        if H == 0:
            predict_result.append([])
            continue
        W = len(input_grid[0])
        
        arr = np.array(input_grid, dtype=np.uint8)
        mask = np.zeros((H+4, W+4), np.uint8)
        
        # Pad with 0s so outer is all connected.
        padded = np.zeros((H+2, W+2), dtype=np.uint8)
        padded[1:-1, 1:-1] = arr
        
        # Flood fill the padded area with -1 (or 255) from 0,0
        cv2.floodFill(padded, mask, (0,0), 255)
        
        # Now padded has 255 for outside, 0 for inside enclosed spaces, 3 for walls
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
