import numpy as np

# Functions
def box_char_func_np(x, x0, x1, y0, y1, z0, z1):
    """
    Determines if points in a NumPy array are within a specified 3D box.

    Parameters:
    x (np.ndarray): A 2D NumPy array of shape (n, 3) where each row represents a point in 3D space.
    x0 (float): The minimum x-coordinate of the box.
    x1 (float): The maximum x-coordinate of the box.
    y0 (float): The minimum y-coordinate of the box.
    y1 (float): The maximum y-coordinate of the box.
    z0 (float): The minimum z-coordinate of the box.
    z1 (float): The maximum z-coordinate of the box.

    Returns:
    np.ndarray: A 1D boolean array of length n where each element is True if the corresponding point is within the box, and False otherwise.
    """
    return np.logical_and.reduce((x[:, 0] >= x0, x[:, 0] <= x1, x[:, 1] >= y0, x[:, 1] <= y1, x[:, 2] >= z0, x[:, 2] <= z1))

def unif_concentration(x, a):
    """
    Generates a uniform concentration array.

    Parameters:
    x (numpy.ndarray): An array whose shape will be used to determine the size of the output array.
    a (float): The value to fill the output array with.

    Returns:
    numpy.ndarray: An array of the same length as the first dimension of `x`, filled with the value `a`.
    """
    return np.full(x.shape[0], a)

def clip(x, min_val, max_val):
    """
    Clips (limits) the values in an array.

    Parameters:
    x (numpy.ndarray): The array to clip.
    min_val (float): The minimum value to allow in the array.
    max_val (float): The maximum value to allow in the array.

    Returns:
    numpy.ndarray: A new array clipped so that all values are between `min_val` and `max_val`.
    """
    return np.clip(x, min_val, max_val)

def vertical_linear_gradient_dist(x, z_0, z_1, c_0, c_1):
    """
    Generates a linear gradient in the vertical direction.

    Parameters:
    x (numpy.ndarray): A 2D NumPy array of shape (n, 3) where each row represents a point in 3D space.
    z_0 (float): The minimum z-coordinate of the gradient.
    z_1 (float): The maximum z-coordinate of the gradient.
    c_0 (float): The value of the gradient at z=z_0.
    c_1 (float): The value of the gradient at z=z_1.

    Returns:
    numpy.ndarray: An array of length n with the gradient values.
    """
    _ = c_0 + (c_1 - c_0) * (x[:, 2] - z_0) / (z_1 - z_0)
    return np.clip(_, c_0, c_1)

def radial_linear_gradient_dist(x, r_0, r_1, c_0, c_1):
    """
    Generates a linear gradient in the radial direction.

    Parameters:
    x (numpy.ndarray): A 2D NumPy array of shape (n, 3) where each row represents a point in 3D space.
    r_0 (float): The minimum radial distance of the gradient.
    r_1 (float): The maximum radial distance of the gradient.
    c_0 (float): The value of the gradient at r=r_0.
    c_1 (float): The value of the gradient at r=r_1.

    Returns:
    numpy.ndarray: An array of length n with the gradient values.
    """
    r = np.linalg.norm(x[:, :2], axis=1)
    _ = c_0 + (c_1 - c_0) * (r - r_0) / (r_1 - r_0)
    return np.clip(_, min([c_0, c_1]), max([c_0, c_1]))

def y_linear_gradient(x, y_0, y_1, c_0, c_1):
    """
    Generates a linear gradient in the y direction.

    Parameters:
    x (numpy.ndarray): A 2D NumPy array of shape (n, 3) where each row represents a point in 3D space.
    y_0 (float): The minimum y-coordinate of the gradient.
    y_1 (float): The maximum y-coordinate of the gradient.
    c_0 (float): The value of the gradient at y=y_0.
    c_1 (float): The value of the gradient at y=y_1.

    Returns:
    numpy.ndarray: An array of length n with the gradient values.
    """
    _ = c_0 + (c_1 - c_0) * (x[:, 1] - y_0) / (y_1 - y_0)
    return np.clip(_, c_0, c_1)

ids = [14000, 8016, 1001]
rel_portions = [0.44, 0.55, 0.01]

# below gets relative portions of the remaining elements keeping them proportional to the remaining weight
def bandaid_get_elems(x, f, rel_portions, round_to=8): 
    out = {}
    out = np.zeros((x.shape[0], len(rel_portions)+1))
    c = f(x)
    out[:, 0] = -c
    for i, port in enumerate(rel_portions):
        out[:, i+1] = -(1-c)*port
    out = np.round(out, round_to)

    return out

def force_n_digits(x, n):
    # if x is less that 10^n, return 0000...x such that the length is n digits, else return x
    if x < 10**n:
        return f'{x:0{n}d}'
    return f'{x}'

def make_mcnp(
        extent, 
        res, 
        f, 
        noncarbon_rel_portions, 
        noncarbon_labels, 
        surface_header = '', 
        surface_footer= '', 
        mat_header = '', 
        mat_footer='', 
        cell_header= '', 
        cell_footer= '',
        sample_pos = 'center', # 'center' or 'top-center'
        ):
    
    x0, x1, y0, y1, z0, z1 = extent
    x_res, y_res, z_res = res
    xs = np.linspace(x0, x1, x_res+1)
    ys = np.linspace(y0, y1, y_res+1)
    zs = np.linspace(z0, z1, z_res+1)

    n = int(np.ceil(np.log10(max(x_res+1, y_res+1, z_res+1))))
    surfaces = ''
    x_ids = []
    y_ids = []
    z_ids = []
    for i, x in enumerate(xs):
        surface_id = f'{surface_header}1{force_n_digits(i, n)}{surface_footer}'
        x_ids.append(surface_id)
        surfaces += (f'{int(surface_id)} px {x}\n')
    for i, y in enumerate(ys):
        surface_id = f'{surface_header}2{force_n_digits(i, n)}{surface_footer}'
        y_ids.append(surface_id)
        surfaces += (f'{int(surface_id)} py {y}\n')
    for i, z in enumerate(zs):
        surface_id = f'{surface_header}3{force_n_digits(i, n)}{surface_footer}'
        z_ids.append(surface_id)
        surfaces += (f'{int(surface_id)} pz {z}\n')

    if sample_pos == 'center':
        xs = xs+(x1-x0)/(x_res+1)
        ys = ys+(y1-y0)/(y_res+1)
        zs = zs+(z1-z0)/(z_res+1)
    elif sample_pos == 'top-center':
        xs = xs+(x1-x0)/x_res
    
    xx, yy, zz = np.meshgrid(xs[:-1], ys[:-1], zs[:-1])
    xx_index, yy_index, zz_index = np.meshgrid(x_ids[:-1], y_ids[:-1], z_ids[:-1])
    xx_index, yy_index, zz_index = xx_index.flatten(), yy_index.flatten(), zz_index.flatten()
    xl_ids, yl_ids, zl_ids = x_ids[1:], y_ids[1:], z_ids[1:]
    xxl_index, yyl_index, zzl_index = np.meshgrid(xl_ids, yl_ids, zl_ids)
    xxl_index, yyl_index, zzl_index = xxl_index.flatten(), yyl_index.flatten(), zzl_index.flatten()
    points = np.column_stack((xx.flatten(), yy.flatten(), zz.flatten()))
    elems = bandaid_get_elems(points, f, noncarbon_rel_portions, 10)
    mats = ''
    nn = int(np.ceil(np.log10(len(elems))))
    elem_ids = []
    for i, elem in enumerate(elems):
        elem_id = f'{mat_header}{force_n_digits(i, nn)}{mat_footer}'
        elem_ids.append(elem_id)
        mats += f'm{elem_id} '
        for id, e in zip(['6000']+noncarbon_labels, elem):
            mats += f'{id} {e} '
        mats += '\n'

    cells = ''
    density = -1.05
    cell_ids = []
    for i, e in enumerate(elem_ids):
        cell_id = f'{cell_header}{force_n_digits(i, nn)}{cell_footer}'
        cell_ids.append(cell_id)
        cells += f'{cell_id} {e} {density} {xx_index[i]} -{xxl_index[i]} {yy_index[i]} -{yyl_index[i]} {zz_index[i]} -{zzl_index[i]} imp:n,p 1\n'
    
    edge_index = [xx_index[0], xxl_index[-1], yy_index[0], yyl_index[-1], zz_index[0], zzl_index[-1]]
    return cells, edge_index, surfaces, mats, elems


def yz_slice_inspect(ax, conc_func, y0, y1, z0, z1, x=.5, n=100, v_min=0, v_max=1):
    """
    Generate and graph a vertical slice of a 3D function.

    Parameters:
    y0 (float): The minimum y-coordinate of the slice.
    y1 (float): The maximum y-coordinate of the slice.
    z0 (float): The minimum z-coordinate of the slice.
    z1 (float): The maximum z-coordinate of the slice.
    x (float): The x-coordinate of the slice.
    n (int): The number of points to sample in the y and z directions.

    Returns:
    numpy.ndarray: A 2D array of shape (n, n) where each element is the value of the function at that point in the slice.
    """

    y = np.linspace(y0, y1, n)
    z = np.linspace(z0, z1, n)
    yy, zz = np.meshgrid(y, z)
    xx = np.full_like(yy, x)
    points = np.column_stack((xx.flatten(), yy.flatten(), zz.flatten()))
    conc = conc_func(points)
    conc = conc.reshape(n, n)

    contourf = ax.contourf(yy, zz, conc, levels=20, cmap='viridis', alpha=0.5, vmin=v_min, vmax=v_max)

    ax.set_xlim(y0, y1)
    ax.set_ylim(z0, z1)
    ax.set_aspect('equal')
    
    return contourf, conc