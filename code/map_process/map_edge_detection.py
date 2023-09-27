import math
import random

import cv2


def edge_detection(map_pth, edge_pth):
    
    # detect edge of map image
    image = cv2.imread(map_pth)

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image_gray, 150, 255, 0)

    mode = cv2.RETR_TREE
    method = cv2.CHAIN_APPROX_SIMPLE
    contours, hierarchy = cv2.findContours(thresh, mode, method)
    contours = contours[1:]

    # print(contours)
    # print(len(hierarchy))

    # visualize edge detection result
    cv2.drawContours(image, contours, -1, (0, 0, 255), 2)
    cv2.imshow("Edge", image)
    cv2.waitKey(0)

    # save edge detection result
    edge_count = 0
    edge_f = open(edge_pth, "w")
    for edge in contours:
        # print(edge)
        
        l_edge = len(edge)
        for idx in range(l_edge - 1):
            
            p_head = edge[idx]
            p_tail = edge[idx + 1]
            
            x_dis = p_head[0][0] - p_tail[0][0]
            y_dis = p_head[0][1] - p_tail[0][1]
            
            # save only the edge with enough length
            if math.sqrt(pow(x_dis, 2) + pow(y_dis, 2)) > 15:            
                edge_f.write(f"({p_head[0][0]},{p_head[0][1]}), ({p_tail[0][0]},{p_tail[0][1]})\n")
                edge_count += 1
                
    print(f"Map {map_pth} has {edge_count} edges")
    

def vis_edge(edge_pth, map_pth):

    # read edge detection result
    edges = []
    edge_f = open(edge_pth)
    for edge in edge_f:
        edge = edge.split(", ")
        ps = []
        for p in edge:
            ps.append(eval(p))
        # print(ps)
        edges.append(ps)        
    # print(edges)
    
    # draw one edge on map image
    map_f = cv2.imread(map_pth)
    random.shuffle(edges)
    for ps in edges:
        # cv2.circle(map_f, p, 2, (0, 0, 255), -1)
        cv2.line(map_f, ps[0], ps[1], (0, 0, 255), 5)
    
    cv2.namedWindow("Edge", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Edge", 1200, 1200)
    cv2.imshow("Edge", map_f)
    cv2.waitKey(0)


if __name__ == "__main__":
    
    map_pth = "code/map_process/data/floor_no_obj_0.png"
    edge_pth = "code/map_process/data/floor_edge.txt"
    
    edge_detection(map_pth, edge_pth)
    
    vis_edge(edge_pth, map_pth)
