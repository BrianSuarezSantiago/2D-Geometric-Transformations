from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

def plotter(ax, data1, data2, param_dict):
    """
    Makes a graph using data1 and data2.
    """
    out = ax.plot(data1, data2, **param_dict)
    return out

def translation(tx, ty, data):
    """
    Geometric translation of a vector (tx,ty)
    """
    translation_matrix = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    print("Translation matrix: ")
    print(translation_matrix)

    final_translation_matrix = np.matmul(translation_matrix, data)
    print("Translation result data: ")
    print(final_translation_matrix)
    return final_translation_matrix

def rotation(radians, data):
    """
    Geometric rotation of center (0,0), with
    angle in radians and points in data argument.
    """
    rotation_matrix = np.array([[math.cos(rad), -math.sin(rad), 0], [math.sin(rad), math.cos(rad), 0], [0, 0, 1]])
    print("Rotation matrix with angle", radians, " radians")
    print(rotation_matrix)

    final_rotation_matrix = np.matmul(rotation_matrix, data)
    print("Rotation result data: ")
    print(final_rotation_matrix)
    return final_rotation_matrix

def scaling(ex, ey, data):
    """
    Geometric scaling with respect to the point (0,0)
    with scale factors ex,ey, and points in the data
    argument.
    """
    print("Scaling matrix with respect to origin, with scaling factors (", ex, ',', ey, ')')
    scaling_matrix = np.array([[ex, 0, 0], [0, ey, 0], [0, 0, 1]])
    print(scaling_matrix)

    final_scaling_matrix = np.matmul(scaling_matrix, data)
    print("Scaling result data: ")
    print(final_scaling_matrix)
    return final_scaling_matrix

def new_data():
    """
    Allows the user to enter values for the calculation
    of different geometric transformations.
    """
    n = int(input("How many points will be used? "))

    data1 = np.empty(n + 1)
    data2 = np.empty(n + 1)
    data_aux = np.zeros(shape = (3, n + 1))
    
    for i in range(n):
        numx = float(input("\nX-Coordinate of the point " + str(i) + ':'))
        data1[i] = numx
        numy = float(input("Y-Coordinate of the point " + str(i) + ':'))
        data2[i] = numy
    
    data1[n] = data1[0]
    data2[n] = data2[0]
    row = np.ones(n + 1)
    result = np.array([data1, data2, row])
    
    print(data1)
    print(data2)

    r = input("Press any key ")
    return result

def visual3D():
    """
    Plot the image in 3D.
    """
    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection = "3d")
    x = np.linspace(-2, 2, 60)
    y = np.linspace(-2, 2, 60)
    x, y = np.meshgrid(x, y)
    r = np.sqrt(x * x + y * y)
    z = np.cos(r)
    surf = ax.plot_surface(x, y, z, rstride = 2, cstride = 2, cmap = 'viridis', linewidth = 0)
    plt.title(r"$z = \cos\,\left(\sqrt{x^2 + y^2}\right)$ ")
    plt.show(block = False)


print("··· GEOMETRIC TRANSFORMATIONS ···")
option = 1
new = True
ff = 1

while option < 5:
    # User menu
    print("Select the type of transformation you want to perform:")
    print("1. Translation")
    print("2. Rotation")
    print("3. Scaling")
    print("4. New transformation with new data")
    print("5. End program")
    
    option = int(input())

    if option >= 5:
        exit("Finished program.")

    if new == True:
        data = new_data()
        fig, ax = plt.subplots(1, 1)
        ax.grid(True)
        plotter(ax, data[0, :], data[1, :], {"marker": 'o'})

    if option == 1:
        tx = float(input("Translation in X: "))
        ty = float(input("Translation in Y: "))
        translation_matrix = translation(tx, ty, data)
        
        data1 = data[0, :]
        data2 = data[1, :]
        data3 = translation_matrix[0, :]
        data4 = translation_matrix[1, :]
        
        minx = min(min(data1), min(data3))
        maxx = max(max(data1), max(data3))
        miny = min(min(data2), min(data4))
        maxy = max(max(data2), max(data4))
        plt.axis([minx - 1.5, maxx + 1.5, miny - 1.5, maxy + 1.5])
        pax = 0.5 * (min(data3) + max(data3))
        pay = 0.5 * (min(data3) + max(data3))
        plt.annotate("Translation [" + str(ff) + ']', xy = (max(data3) + 0.1, max(data4) + 0.1),
                     xytext = (max(data3) + 0.5, max(data4) + 0.5),
                     arrowprops = dict(facecolor = "yellow", shrink = 0.0, width = 1, headwidth = 4))
        plt.title("Translation of the vector (" + str(tx) + ',' + str(ty) + ')')
        plotter(ax, data3, data4, {"marker": 's'})
        plt.show(block=False)

        data = translation_matrix
        new = False
        ff += 1

    elif option == 2:
        const_pi = math.pi

        angle = float(input("Rotation angle (degrees): "))
        rad = angle * const_pi / 180

        px = float(input("Rotation center, coord. X: "))
        py = float(input("Rotation center, coord. Y: "))

        if px == 0 and py == 0:
            final = rotation(rad, data)
        else:
            print("Performing vector translation (", -px, ',', -py, ')')
            med_translation = translation(-px, -py, data)

            print("Performing rotation with angle ", rad, " radians")
            med_rotation = rotation(rad, med_translation)

            print("Performing vector translation (", px, ',', py, ')')
            final = translation(px, py, med_rotation)

        data1 = data[0, :]
        data2 = data[1, :]
        data3 = final[0, :]
        data4 = final[1, :]
        
        minx = min(min(data1), min(data3))
        maxx = max(max(data1), max(data3))
        miny = min(min(data2), min(data4))
        maxy = max(max(data2), max(data4))
        plt.axis([minx - 1.5, maxx + 1.5, miny - 1.5, maxy + 1.5])

        plotter(ax, data3, data4, {"marker": 's'})
        plt.title("Rotation with angle " + r'$\alpha = ' + str(angle) + "^{\circ}$ and center (" + str(px) + ',' + str(py) + ')')
        plt.annotate("Rotation [" + str(ff) + ']', xy = (max(data3) + 0.1, max(data4) + 0.1),
                     xytext = (max(data3) + 0.5, max(data4) + 0.5),
                     arrowprops = dict(facecolor = 'green', shrink = 0.0, width = 1, headwidth = 4))
        plt.show(block = False)
        
        data = final
        new = False
        ff += 1

    elif option == 3:
        ex = float(input("Scaling factor in X: "))
        ey = float(input("Scaling factor in Y: "))

        px = float(input("The scaling is with respect to the point, coord. X: "))
        py = float(input("The scaling is with respect to the point, coord. Y: "))

        if px == 0 and py == 0:
            finale = scaling(ex, ey, data)
        else:
            print("Performing vector translation (", -px, ',', -py, ')')
            med_translation = translation(-px, -py, data)

            print("Performing scaling with factors (", ex, ',', ey, ')')
            med_scaling = scaling(ex, ey, med_translation)

            print("Performing vector translation (", px, ',', py, ')')
            finale = translation(px, py, med_scaling)

        data1 = data[0, :]
        data2 = data[1, :]
        data5 = finale[0, :]
        data6 = finale[1, :]
        
        plt.axis([min(data1) - 4.5, max(data5) + 2.5, min(data2) - 4.5, max(data6) + 2.5])
        plt.annotate("Scaling [" + str(ff) + ']', xy = (max(data5) + 0.1, max(data6) + 0.1),
                     xytext = (max(data5) + 0.5, max(data6) + 0.5),
                     arrowprops = dict(facecolor = 'red', shrink = 0.0, width = 1, headwidth = 4))
        plt.title("Scaling with factors (" + str(ex) + ',' + str(ey) + ") regarding the point (" + str(px) + ',' + str(py) + ')')
        plotter(ax, data5, data6, {"marker": 's'})
        plt.show(block = False)
        
        data = finale
        new = False
        ff += 1

    elif option == 4:
        new = True
        ff = 1
        print("Data: ", data, "New = ", new)

    elif option == 0:
        visual3D()

    else:
        exit(0)
