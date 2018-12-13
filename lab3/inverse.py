import numpy as np
import csv
from copy import deepcopy
from sklearn.metrics import mean_squared_error

def convert_inverse(file_name):

    # read matrix from csv file
    x = np.genfromtxt(file_name, delimiter=',')
    mat = np.array(x, np.float64)

    # make a copy of the matrix that we shall not modified to use to test
    # at the end to proof
    X = deepcopy(mat)

    rows = mat.shape[0]
    cols = mat.shape[1]

    id_mat = np.identity(rows, np.float64)
    Y = deepcopy(id_mat)

    print("The Matric to get Inverse of \n", mat)

    if np.linalg.det(mat) != 0:
        for j in range(cols):
            # take current row and multiply by 1/the that value that
            # makes it a 1
            if mat[j][j] != 1:
                if  mat[j][j] != 0:
                    divisor = 1/mat[j][j]
                else:
                    tmp = np.copy(mat[j])
                    tmp2 = np.copy(mat[j+1])
                    mat[j] = tmp2
                    mat[j+1] = tmp
                    divisor = 1/mat[j][j]

                id_mat[j] = np.multiply(id_mat[j], divisor)
                mat[j] = np.multiply(mat[j], divisor)

                # check that the current column doesnt have a 1 in the diagnol position
                # otherwise do the row operation
                for i in range(rows):
                    if j != i:
                        # negate the number which is on the same column
                        neg_mat = np.multiply(-1, mat[i][j])

                        # multiply the -ve scalar by the specific number we want to change to a 0
                        add_mat_scalar = neg_mat * mat[j, :]
                        add_idmat_scalar = neg_mat * id_mat[j, :]

                        # add the result above the number we want to chnage to a 0
                        mat[i, :] = np.add(add_mat_scalar, mat[i, :])
                        id_mat[i, :] = np.add(add_idmat_scalar, id_mat[i, :])
    else:
        print("The matrix is not Invertible")

    print("\n")
    print("----------------------------------------------------")
    print("\n")
    print("inverse matrix is: \n", id_mat)
    print("\n")
    # print("The proof: \n",)
    # print("----------------------------------------------------")

    # To verify the inverse, I use the numpy multiplication
    result = np.matmul(id_mat, X)
    print(result)

    # Computing the Maximum Absolute Error  and Mean Squared Error
    print("\n")
    print("----------------------------------------------------")
    print("The Mean Squared Error (MSE) is: ",
          mean_squared_error(result, Y))
    print("The Maximum Absolute Error (MAE) is: ", np.max(np.subtract(Y, result)))


convert_inverse("matrix.csv")
