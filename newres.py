import math
import numpy as np

previous_angles = None 
current_angles = None
angle_diff = None 
diff_sum_array = [0] * 12 
angle_differences_counts = [0] * 12
previous_diff_sum_array = [0] * len(diff_sum_array)
look = [0] * 12
sum = [0] * 12
diff = [0] * 12
global ct 
EPSILON = 0.0001
def lookcount():
    return look.copy()

def looksum():
    return sum.copy()

def lookdiff():
    return diff.copy()

def reset_flag(out_flag):
    global angle_differences_counts, diff_sum_array,look,sum,diff,angle_diff,previous_diff_sum_array,previous_angles,current_angles
    flag = out_flag
    if flag:
        print('#--------------------------------------------------------------------------------------------------------------------》')      
        look = angle_differences_counts
        sum = diff_sum_array
        angle_differences_counts = [0] * 12  # 重置计数
        diff_sum_array = [0] * 12 
        # angle_differences_counts = [1.0, 1.0, 0.5, 1.0, -1.0, 0.5, 1.0, -1.0, 1.0, 0.5, 0.5, 1.0]#累计上一轮计数
        # diff_sum_array = [225.0, 179.99999999999994, 135.00000000000009, 225.0, -224.99999999999994, 90.00000000000011, 180.0, -224.9999999999999, 225.00000000000006, 135.0, 90.00000000000003, 225.0]
        angle_diff = None 
        previous_diff_sum_array = [0] * len(diff_sum_array)
        previous_angles = None
        current_angles = None
        flag = False  # 重置标志位 

def calculate_angle(center, point):  
    dx = point[0] - center[0]  
    dy = point[1] - center[1] 
    angle_rad = math.atan2(dy, dx)  
    angle_deg = math.degrees(angle_rad)  
    if angle_deg < 0:  
        angle_deg += 360  
    return angle_deg 
def points_updates(X_, Y_):  
    updated_points = np.zeros([4, 2])  
    for i in range(4):  
        updated_points[i][0] = X_[i]  
        updated_points[i][1] = Y_[i]  
    return updated_points
def check_winding(x_, y_):  
    global previous_angles, current_angles, angle_diff, diff_sum_array, angle_differences_counts,previous_diff_sum_array,diff
    updated_points = points_updates(x_, y_)  
    winding_detected = False 
    diff_over90 = False 
    current_angles = []  
    all_angle_diffs = []
    for i in range(4):  
        center = updated_points[i]  
        for j in range(4):  
            if i != j:  
                current_angles.append(calculate_angle(center, updated_points[j]))  
        if previous_angles is not None and len(previous_angles) == len(current_angles):  
            for idx in range(len(current_angles)):  
                angle_diff = current_angles[idx] - previous_angles[idx]  
                angle_diff = (angle_diff + 180) % 360 - 180
                diff_sum_array[idx] += angle_diff
                all_angle_diffs.append(angle_diff)                
                previous_diff_sum_array = diff_sum_array.copy()  

                if abs(diff_sum_array[idx]) >= (90 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) < (90 - EPSILON):  
                    if diff_sum_array[idx] - angle_diff / 2 > 0:  
                        angle_differences_counts[idx] += 0.5  
                    else:  
                        angle_differences_counts[idx] -= 0.5  
                elif abs(diff_sum_array[idx]) >= (270 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) < (270 - EPSILON):  
                    if diff_sum_array[idx] - angle_diff > 0:  
                        angle_differences_counts[idx] += 0.5  
                    else:  
                         angle_differences_counts[idx] -= 0.5  


                if abs(diff_sum_array[idx]) >= (180 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) < (180 - EPSILON):  
                    if diff_sum_array[idx] - angle_diff > 0:  
                        angle_differences_counts[idx] += 0.5  
                    else:  
                        angle_differences_counts[idx] -= 0.5  
                elif abs(diff_sum_array[idx]) >= (360 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) < (360 - EPSILON):  
                    if diff_sum_array[idx] - angle_diff > 0:  
                        angle_differences_counts[idx] += 0.5  
                    else:  
                         angle_differences_counts[idx] -= 0.5




                if abs(diff_sum_array[idx]) < (90 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) >= (90 - EPSILON):  
                    if diff_sum_array[idx] - angle_diff  > 0:  
                        angle_differences_counts[idx] -= 0.5  
                    else:  
                        angle_differences_counts[idx] += 0.5  
                elif abs(diff_sum_array[idx]) < (270 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) >= (270 - EPSILON):  
                    if diff_sum_array[idx] - angle_diff > 0:  
                        angle_differences_counts[idx] -= 0.5  
                    else:  
                         angle_differences_counts[idx] += 0.5                           


                if abs(diff_sum_array[idx]) < (180 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) >= (180 - EPSILON):  
                    if diff_sum_array[idx] - angle_diff > 0:  
                        angle_differences_counts[idx] -= 0.5  
                    else:  
                        angle_differences_counts[idx] += 0.5  
                # elif abs(diff_sum_array[idx]) <= (360 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) > (360 - EPSILON):
                elif abs(diff_sum_array[idx]) < (360 - EPSILON) and abs(diff_sum_array[idx] - angle_diff) >= (360 - EPSILON):   
                    if diff_sum_array[idx] - angle_diff > 0:  
                        angle_differences_counts[idx] -= 0.5  
                    else:  
                         angle_differences_counts[idx] += 0.5  


                if angle_differences_counts[idx] >= 2 or angle_differences_counts[idx] <= -2:  
                    winding_detected = True                         
    winding_detected = any(count >= 2 or count <= -2 for count in angle_differences_counts) or any(perdiff > 90 or perdiff < -90 for perdiff in all_angle_diffs)
    diff =  all_angle_diffs
    # print('本次diff:',diff)
    # print('本次sum:',diff_sum_array)
    previous_angles = current_angles[:]
    if winding_detected:  
        return True 
    else:  
        return False
    


def process_paths0(paths):
    ct = 0
    reset_flag(True)
    if not all(len(path) == len(paths[0]) for path in paths):  
        raise ValueError("所有路径的长度必须相同")  
    for t in range(len(paths[0])):  
        x_coords = [path[t, 0] for path in paths]  
        y_coords = [path[t, 1] for path in paths]
        winding_count = check_winding(x_coords, y_coords)  
        if winding_count:
            ct0 += 1  
    return ct0