import os
import cv2
import numpy as np
import heapq

def info(src_path):
    image = cv2.imread(src_path)
    row, column = image.shape[0:2]
    D = int(np.sqrt((row**2)+(column**2)))
    return row, column, D

def Canny(src_path, write_path, min, max):
    image = cv2.imread(src_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edge_image = cv2.Canny(image, min, max)
    cv2.imwrite(os.path.join(write_path, "edge_map.png"), edge_image)
    return edge_image

def DetectLine(src_path, write_path, edge_map, M, N, K):
    image = cv2.imread(src_path)
    row, column = edge_map.shape

    D = int(np.sqrt((row**2) + (column**2)))
    rho_min = -D
    L_rho = 2*D
    delta_rho = L_rho/M

    theta_min = np.deg2rad(-90)
    L_theta = np.pi
    delta_theta = L_theta/N


    #COMMULATOR
    A = np.zeros(shape=(M, N))
    for x in range(row):
        for y in range(column):
            if edge_map[x, y] !=0:
                for j in range(N):
                    Theta = theta_min + j*delta_theta + delta_theta/2
                    Rho = x*np.cos(Theta) + y*np.sin(Theta)
                    i = int((Rho-rho_min)/delta_rho)
                    A[i][j] += 1

    #APPLY NONMAXIMA
    for i in range(1, M-1):
        for j in range(1, N-1):
            NW = A[i-1][j-1]
            NO = A[i-1][j]
            NE = A[i-1][j+1]
            E = A[i][j+1]
            SE = A[i+1][j+1]
            S = A[i+1][j]
            SW = A[i+1][j-1]
            W = A[i][j-1]
            C = A[i][j]
            C1 = (C < NW) or (C < NO)
            C2 = (C < NE) or (C < E)
            C3 = (C < SE) or (C < S)
            C4 = (C < SW) or (C < W)
            if (C1 or C2 or C3 or C4):
                A[i][j] = 0

    #FIND MAXIMA
    Hmax = []
    indices = []
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (A[i][j] != 0):
                key = -A[i][j]
                data_rho = rho_min + i*delta_rho + delta_rho/2 #dcmidx2rho(i)
                data_theta = theta_min + j*delta_theta + delta_theta/2 #dcmidx2theta(j)
                E = [key, [data_rho, data_theta]]
                heapq.heappush(Hmax, E)
    k = 0
    while(len(Hmax) > 0 and k < K):
        E = heapq.heappop(Hmax)
        indices.append([E[1][0], E[1][1]])
        k += 1
    K = k

    rotate(row, column, indices, K, image, write_path)
    draw(image, indices, K, write_path)


def draw(image, indices, K, write_path):
    #draw line
    for i in range(K):
        rho_draw = indices[i][0]
        theta_draw = indices[i][1]

        b = np.cos(theta_draw)
        a = np.sin(theta_draw)
        x0 = a*rho_draw
        y0 = b*rho_draw

        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*a)
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*a)
        line = cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.imwrite(os.path.join(write_path, "line.png"), line)

def rotate(row, column, indices, K, origin_image, write_path):
    sum_theta = 0
    for i in range(K):
        sum_theta += indices[i][1]
    average_theta = sum_theta/K
    rad2deg_angle = np.rad2deg(average_theta)
    #angle = (rad2deg_angle > -18.5 and rad2deg_angle < 25) and -rad2deg_angle or rad2deg_angle
    M = cv2.getRotationMatrix2D((column / 2, row / 2), -rad2deg_angle, 1)
    rotated = cv2.warpAffine(origin_image, M, (column, row))
    cv2.imwrite(os.path.join(write_path, "rotated.png"), rotated)
