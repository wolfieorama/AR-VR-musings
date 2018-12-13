import numpy as np
import csv
import scipy


def read_coordinates(file):
    """
    Read coordinates from the csv file
    """
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        x = []
        y = []
        z = []
        pixels = []

        for row in readCSV:
            x.append(int(row[0]))
            y.append(int(row[1]))
            z.append(int(row[2]))
            pixels.append([int(row[3]), int(row[4])])

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        pixels = np.array(pixels)
return x, y, z, pixels


def build_matrix_A(x, y, z, pixels):
    """
    Build the A matrix
    """
    matrix = []
    X = []
    for i in range(len(x)):
        matrix.append([x[i], y[i], z[i], 1, 0, 0, 0, 0,-(pixels[i][0]*x[i]), -(pixels[i][0]*y[i]), -(pixels[i][0]*z[i])])
        matrix.append([0, 0, 0, 0, x[i], y[i], z[i], 1,-(pixels[i][1]*x[i]), -(pixels[i][1]*y[i]), -(pixels[i][1]*z[i])])
        X.append(pixels[i][0])
        X.append(pixels[i][1])
    matrix = np.array(matrix)
    X = np.array(X).reshape(-1,1)
    return matrix, X


def buildH(matrix, X):
    """
    Build the H matrix
    """
    H = np.dot(np.linalg.pinv(matrix), X).tolist()
    H.append([1])
    newH = np.array(H).reshape(3, 4)
    return newH


def buildKR(H_matrix):
    """
    Build the K and Rotation matrices
    """
    H = H_matrix[:, :3]
    R, Q = scipy.linalg.rq(H)
    R = R/R[2, 2]
    K = np.copy(R)
    rotation = np.copy(Q.T)
    return K, rotation


def Transilation(K, rotation, H_matrix):
    """
 Calculate the translation matrix
    """
    tb = np.dot(-rotation, np.dot(np.linalg.inv(K), H_matrix[:, 3]))
    return tb


def implementation(file):
    """
    produce the output
    """
    x, y, z, pixels = read_coordinates(file)
    matrix1, X1 = build_matrix_A(x, y, z, pixels)
    matrix2, X2 = build_matrix_A(x[:10], y[:10], z[:10], pixels[:10])
    H_matrix1 = buildH(matrix1, X1)
    H_matrix2 = buildH(matrix2, X2)
    K1, rotation1 = buildKR(H_matrix1)
    K2, rotation2 = buildKR(H_matrix2)
    Translation1 = Transilation(K1, rotation1, H_matrix1)
    Translation2 = Transilation(K2, rotation2, H_matrix2)

    np.savetxt('K_matrix_' + file, K1, delimiter=',')
    np.savetxt('K_matrix 10_' + file, K2, delimiter=',')
    np.savetxt('rotation_' + file, rotation1, delimiter=',')
    np.savetxt('rotation 10_' + file, rotation2, delimiter=',')
    np.savetxt('Translation_' + file, Translation1, delimiter=',')
    np.savetxt('Translation_10_' + file, Translation2, delimiter=',')


implementation('913.csv')
implementation('1050.csv')
implementation('points0820')
implementation('points21000')