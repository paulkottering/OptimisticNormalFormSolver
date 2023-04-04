import numpy as np
import matplotlib.pyplot as plt
def sample_index(Game,i):
    if i == "d":
        return descending_active(Game)
    if i == "ra":
        return random_active(Game)
    if i == "nr":
        return nearby_then_random(Game)
    if i == "r":
        return random_index(Game)
    if i == "or":
        return opt_then_random(Game)
    if i == "lr":
        return low_then_random(Game)
    if i == "pr":
        return pes_then_random(Game)
    if i == "pm":
        return prob_match(Game)
    if i == "pa":
        return prob_active(Game)
    if i == "da":
        return descending_active_2(Game)
    if i == "da2":
        return descending_active_3(Game)
    if i == "pa3":
        return prob_active_3(Game)
    if i == "pa4":
        return prob_active_4(Game)
def descending_active(game):

    reverse_ascending_order = np.argsort(game.OptPhi - game.PesPhi, axis=None)[::-1]

    for i in range(len(reverse_ascending_order)):
        index = reverse_ascending_order[i]
        row, col = np.unravel_index(index, game.OptPhi.shape)
        if game.OptPhi[row, col] > np.max(game.PesPhi):
            if np.isnan(game.OptPhi[row, col]):
                return ind_to_prob_matrix_one_zero(row,col,game.n)

    if np.any(np.isnan(game.KnownU1)):
        rand_ind1 = np.argwhere(np.isnan(game.KnownU1))[0][0]
        rand_ind2 = np.argwhere(np.isnan(game.KnownU1))[0][1]
        return ind_to_prob_matrix_one_zero(rand_ind1, rand_ind2,game.n)
def random_active(game):

    ind1, ind2 = np.unravel_index(np.argmax(game.OptPhi, axis=None), (game.n, game.n))

    if np.isnan(game.KnownU1[ind1, ind2]):
        return ind_to_prob_matrix_one_zero(ind1, ind2,game.n)

    nan_new_act = []
    new_act = []
    indices = []
    for index in np.ndindex((game.n,game.n)):
        indices.append(list(index))

    for ind in indices:
        if game.OptPhi[ind[0], ind[1]] >= np.max(game.PesPhi):
            if np.isnan(game.KnownU1[ind[0], ind[1]]):
                nan_new_act.append(ind)
            new_act.append(ind)

    if len(nan_new_act) > 1:
        nan_active_indices = np.array(nan_new_act)
        rand_active_ind = np.random.choice(range(len(nan_active_indices)), size=1, replace=False)

        rand_active_ind1 = nan_active_indices[rand_active_ind][0][0]
        rand_active_ind2 = nan_active_indices[rand_active_ind][0][1]
        return ind_to_prob_matrix_one_zero(rand_active_ind1, rand_active_ind2, game.n)

    if np.any(np.isnan(game.KnownU1)):
        rand_ind1 = np.argwhere(np.isnan(game.KnownU1))[0][0]
        rand_ind2 = np.argwhere(np.isnan(game.KnownU1))[0][1]
        return ind_to_prob_matrix_one_zero(rand_ind1, rand_ind2, game.n)
def nearby_then_random(game):

    ind1, ind2 = np.unravel_index(np.argmax(game.OptPhi, axis=None), (game.n, game.n))

    if np.isnan(game.KnownU1[ind1, ind2]):
        return ind_to_prob_matrix_one_zero(ind1, ind2,game.n)

    if 0 <= ind2-1 :
        if np.isnan(game.KnownU1[ind1,ind2-1]):
            return ind_to_prob_matrix_one_zero(ind1, ind2-1, game.n)

    if ind2+1 < game.n:
        if np.isnan(game.KnownU1[ind1,ind2+1]):
            return ind_to_prob_matrix_one_zero(ind1, ind2+1, game.n)

    if ind1+1 < game.n:
        if np.isnan(game.KnownU1[ind1+1, ind2]):
            return ind_to_prob_matrix_one_zero(ind1+1, ind2,game.n)

    if 0 <= ind1-1 :
        if np.isnan(game.KnownU1[ind1-1, ind2]):
            return ind_to_prob_matrix_one_zero(ind1-1, ind2,game.n)

    if np.any(np.isnan(game.KnownU1)):
        rand_ind1 = np.argwhere(np.isnan(game.KnownU1))[0][0]
        rand_ind2 = np.argwhere(np.isnan(game.KnownU1))[0][1]
        return ind_to_prob_matrix_one_zero(rand_ind1,rand_ind2,game.n)
def random_index(game):
    if np.any(np.isnan(game.KnownUs[0])):
        rand_ind1 = np.argwhere(np.isnan(game.KnownU1))[0][0]
        rand_ind2 = np.argwhere(np.isnan(game.KnownU1))[0][1]
        return ind_to_prob_matrix_one_zero(rand_ind1,rand_ind2,game.n)
def opt_then_random(game):
    ind1, ind2 = np.unravel_index(np.argmax(game.OptPhi, axis=None), (game.n, game.n))

    if np.isnan(game.KnownU1[ind1, ind2]):
        return ind_to_prob_matrix_one_zero(ind1,ind2,game.n)

    if np.any(np.isnan(game.KnownU1)):
        rand_ind1 = np.argwhere(np.isnan(game.KnownU1))[0][0]
        rand_ind2 = np.argwhere(np.isnan(game.KnownU1))[0][1]
        return ind_to_prob_matrix_one_zero(rand_ind1,rand_ind2,game.n)
def pes_then_random(game):
    ind1, ind2 = np.unravel_index(np.argmax(game.PesPhi, axis=None), (game.n, game.n))

    if np.isnan(game.KnownU1[ind1, ind2]):
        return ind_to_prob_matrix_one_zero(ind1,ind2,game.n)

    if np.any(np.isnan(game.KnownU1)):
        rand_ind1 = np.argwhere(np.isnan(game.KnownU1))[0][0]
        rand_ind2 = np.argwhere(np.isnan(game.KnownU1))[0][1]
        return ind_to_prob_matrix_one_zero(rand_ind1, rand_ind2,game.n)
def low_then_random(game):
    ind1, ind2 = np.unravel_index(np.argmax(game.PesPhi, axis=None), (game.n, game.n))

    if np.isnan(game.KnownU1[ind1, ind2]):
        return ind_to_prob_matrix_one_zero(ind1,ind2,game.n)
def prob_match(game):
    n = game.n
    ind1, ind2 = np.unravel_index(np.argmax(game.OptPhi, axis=None), (n, n))
    prob_matrix = np.ones((n, n))

    prob_matrix[ind1, ind2 ] += ((n - 1) ** 2 + 2 * (n - 1)) / n ** 2

    for a in range(n):
        for b in range(n):
            if a != ind1 and b != ind2:
                prob_matrix[a, b] += 3 * (1 / n ** 2)
            elif a == ind1 and b != ind2:
                prob_matrix[a, b] += 2 * (n - 1) / n ** 2 + (1 / n ** 2)
            elif b == ind2 and a != ind1:
                prob_matrix[a, b] += 2 * (n - 1) / n ** 2 + (1 / n ** 2)

    prob_matrix = prob_matrix / np.sum(prob_matrix)

    prob_array = prob_matrix.flatten()

    choice = np.random.choice(range(n**2),1,p=prob_array)

    j = choice % n
    i = choice // n
    return i,j,prob_matrix
def prob_active(game):
    n = game.n
    Phi = np.copy(game.OptPhi)

    mask = Phi < np.max(game.PesPhi)
    Phi[mask] = 1e-8

    Phi /= np.sum(Phi)

    prob_array = Phi.flatten()
    choice = np.random.choice(np.arange(prob_array.size), p=prob_array)
    random_sample = np.unravel_index(choice, Phi.shape)

    return random_sample, Phi

def prob_active_2(game):
    n = game.n
    k = game.k
    phi = np.copy(game.OptPhi)

    #mask = phi < np.max(game.PesPhi)
    #phi[mask] = 0

    phi = phi - np.min(game.OptPhi)
    mask = phi < np.max(game.PesPhi) - np.min(game.OptPhi)
    phi[mask] = 1e-8

    phi /= np.sum(phi)

    prob_array = phi.flatten()
    choice = np.random.choice(np.arange(prob_array.size), p=prob_array)
    random_sample = np.unravel_index(choice, phi.shape)

    return random_sample, phi

def prob_active_3(game):
    n = game.n
    k = game.k
    phi = np.copy(game.OptPhi)

    mask = phi < np.max(game.PesPhi)
    phi[mask] = 0

    mask2 = game.Values < 0
    phi[mask2] = 0

    phi = phi - np.min(game.OptPhi)
    mask = phi < np.max(game.PesPhi) - np.min(game.OptPhi)
    phi[mask] = 1e-15
    phi[mask2] = 1e-15

    max_tuple = np.unravel_index(np.argmax(game.UnknownGame), game.OptPhi.shape)
    #phi_2 = np.zeros([n]*k)
    phi_2 = np.copy(phi)

    phi[max_tuple] = 1e-15
    phi /= np.sum(phi)

    prob_array = phi.flatten()
    opt_prob_array = game.UnknownGame.flatten()

    fig, ax1 = plt.subplots()

    ax1.scatter(range(len(prob_array)),prob_array,color='red')

    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    ax3.scatter(range(len(prob_array)), phi_2.flatten(), color='green')
    ax2.scatter(range(len(opt_prob_array)), opt_prob_array,color='blue')
    plt.show()
    choice = np.random.choice(np.arange(prob_array.size), p=prob_array)
    random_sample = np.unravel_index(choice, phi.shape)

    return random_sample, phi

def prob_active_4(game):
    n = game.n
    k = game.k
    phi = np.copy(game.OptPhi)

    mask = phi < np.max(game.PesPhi)
    phi[mask] = 0

    mask2 = game.Values < 0
    phi[mask2] = 0

    phi = phi - np.min(game.OptPhi)
    mask = phi < np.max(game.PesPhi) - np.min(game.OptPhi)
    phi[mask] = 1e-15
    phi[mask2] = 1e-15

    max_tuple = np.unravel_index(np.argmax(game.OptPhi), game.OptPhi.shape)
    phi_2 = np.zeros([n]*k)
    phi_2[max_tuple] = 1

    if ~np.isnan(game.KnownUs[0][max_tuple]):
        a = np.random.rand(1)
        print(a)
        if a < 0.1:
            phi /= np.sum(phi)
            phi_2 = np.copy(phi)

    prob_array = phi_2.flatten()
    opt_prob_array = game.UnknownGame.flatten()

    # fig, ax1 = plt.subplots()
    #
    # ax1.scatter(range(len(prob_array)),prob_array,color='red')
    #
    # ax2 = ax1.twinx()
    # ax3 = ax1.twinx()
    # ax3.scatter(range(len(prob_array)), phi.flatten(), color='green')
    # ax2.scatter(range(len(opt_prob_array)), opt_prob_array,color='blue')
    # plt.show()
    choice = np.random.choice(np.arange(prob_array.size), p=prob_array)
    random_sample = np.unravel_index(choice, phi.shape)

    return random_sample, phi_2

def prob_active_5(game):
    n = game.n
    k = game.k
    phi = np.copy(game.OptPhi)

    mask = phi < np.max(game.PesPhi)
    phi[mask] = 0

    mask2 = game.Values < 0
    phi[mask2] = 0

    phi = phi - np.min(game.OptPhi)
    mask = phi < np.max(game.PesPhi) - np.min(game.OptPhi)
    phi[mask] = 1e-15
    phi[mask2] = 1e-15

    max_tuple = np.unravel_index(np.argmax(game.OptPhi), game.OptPhi.shape)
    phi_2 = np.zeros([n]*k)
    phi_2[max_tuple] = 1

    if ~np.isnan(game.KnownUs[0][max_tuple]):
        a = np.random.rand(1)
        print(a)
        if a < 0.1:
            phi /= np.sum(phi)
            phi_2 = np.copy(phi)

    prob_array = phi_2.flatten()
    opt_prob_array = game.UnknownGame.flatten()

    # fig, ax1 = plt.subplots()
    #
    # ax1.scatter(range(len(prob_array)),prob_array,color='red')
    #
    # ax2 = ax1.twinx()
    # ax3 = ax1.twinx()
    # ax3.scatter(range(len(prob_array)), phi.flatten(), color='green')
    # ax2.scatter(range(len(opt_prob_array)), opt_prob_array,color='blue')
    # plt.show()
    choice = np.random.choice(np.arange(prob_array.size), p=prob_array)
    random_sample = np.unravel_index(choice, phi.shape)

    return random_sample, phi_2

def ind_to_prob_matrix_one_zero(sample_tuple,n,k):
    shape = [n]*k
    prob_matrix = np.zeros(shape)
    prob_matrix[sample_tuple] = 1
    return sample_tuple,prob_matrix

def descending_active_2(game):
    num_top_values = 100
    sorted_indices = np.unravel_index(np.argsort(game.OptPhi.ravel())[-num_top_values:], game.OptPhi.shape)

    # Sort the indices according to the highest value
    sorted_indices = list(zip(*sorted_indices))
    sorted_indices.reverse()

    if game.OptPhi[sorted_indices[1]] < np.max(game.PesPhi):
        return ind_to_prob_matrix_one_zero(sorted_indices[0], game.n, game.k)

    for ind in sorted_indices:
        if (np.isnan(game.KnownUs[0][ind])) and game.OptPhi[ind] > np.max(game.PesPhi):
            return ind_to_prob_matrix_one_zero(ind, game.n, game.k)

    non_nan_indices = np.argwhere(~np.isnan(game.KnownUs[0]))
    index = np.random.choice(non_nan_indices)
    return ind_to_prob_matrix_one_zero(index, game.n, game.k)

def descending_active_3(game):
    sorted_indices = np.unravel_index(np.argsort(game.OptPhi.ravel())[:], game.OptPhi.shape)

    # Sort the indices according to the highest value
    sorted_indices = list(zip(*sorted_indices))
    sorted_indices.reverse()
    return ind_to_prob_matrix_one_zero(sorted_indices[0], game.n, game.k)

