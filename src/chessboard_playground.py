import numpy as np

from auxiliary import find_intersection


def chess_nine_tuplets_pairs(nine_tuples, angle_max_difference):
  mins = np.min(nine_tuples[:, :, 1], axis=1)
  angles2change = np.where((nine_tuples[:, :, 1].T <= mins + 1.57) &
                           (mins - 1.57 <= nine_tuples[:, :, 1].T),
                           False,
                           True).T
  for i in np.arange(nine_tuples.shape[0]):
    nine_tuples[i, angles2change[i], 1] -= np.pi
  avg_angles = np.average(nine_tuples[:, :, 1], axis=1)
  pi_half = np.pi / 2

  possible_chessboards = []
  # better iteration over the angles
  for first_idx in np.arange(len(avg_angles)):
    for second_idx in np.arange(first_idx + 1, len(avg_angles)):
      first_angle = avg_angles[first_idx]
      second_angle = avg_angles[second_idx]
      if first_angle < second_angle:
        first_angle += pi_half
      else:
        second_angle += pi_half
      if (first_angle - angle_max_difference <=
              second_angle <=
              first_angle + angle_max_difference):
        # return indices??
        possible_chessboards.append([nine_tuples[first_idx], nine_tuples[second_idx]])
  possible_chessboards = np.array(possible_chessboards)
  return possible_chessboards


def chessboard_from_pairs(pairs):
  chessboards = []
  for pair in pairs:
    first_max = np.argmax(pair[0, :, 0])
    second_max = np.argmax(pair[1, :, 0])
    first_min = np.argmin(pair[0, :, 0])
    second_min = np.argmin(pair[1, :, 0])
    chessboard_tmp = []
    x, y = find_intersection(pair[0, first_max], pair[1, second_max])
    chessboard_tmp.append([x, y])
    x, y = find_intersection(pair[0, first_max], pair[1, second_min])
    chessboard_tmp.append([x, y])
    x, y = find_intersection(pair[0, first_min], pair[1, second_min])
    chessboard_tmp.append([x, y])
    x, y = find_intersection(pair[0, first_min], pair[1, second_max])
    chessboard_tmp.append([x, y])
    chessboards.append(chessboard_tmp)
  chessboards = np.asarray(chessboards, dtype=np.int32)
  return chessboards


# def find_n_even_spaced_parallel(lines_r_angle, angle_max_difference, n):
#   n_tuples = []
#   pi_half = np.pi / 2
#   for first_idx in np.arange(len(lines_r_angle)):
#     tmp_n_tuple = [lines_r_angle]
#     for second_idx in np.arange(first_idx + 1, len(lines_r_angle)):
#       first_angle = lines_r_angle[first_idx]
#       second_angle = lines_r_angle[second_idx]
#       if np.abs(first_angle - second_angle) > pi_half:
#         if first_angle < second_angle:
#           first_angle += np.pi
#         else:
#           second_angle += np.pi
#       if (first_angle - angle_max_difference <=
#               second_angle <=
#               first_angle + angle_max_difference):
#         tmp_n_tuple.append(lines_r_angle[second_idx])
#     if len(tmp_n_tuple) == n:
#       n_tuples.append(np.array(tmp_n_tuple))
#     elif len(tmp_n_tuple) > n:
#       n_tuples = np.array(n_tuples)
#       differences = n_tuples[:-1] - n_tuples[1:]
      # tady vezmu vzdycky n_tici-1 za n_tici-1 a chci staty:
      # staty: prumerna differecne + min/max difference? -> pokud vetsi nez pripustna chyba
      #        tak pesek
      # index n-tice start -> index n-tice start + n


def find_ninetuples(lines_r_angle, angle_max_difference):
  ninetuples = []
  pi_half = np.pi / 2
  for first_idx in np.arange(len(lines_r_angle)):
    tmp_ninetuple = [lines_r_angle[first_idx]]
    # tu vytvorim tmp
    for second_idx in np.arange(first_idx + 1, len(lines_r_angle)):
      first_angle = lines_r_angle[first_idx][1]
      second_angle = lines_r_angle[second_idx][1]
      if np.abs(first_angle - second_angle) > pi_half:
        if first_angle < pi_half:
          first_angle += np.pi
        else:
          second_angle += np.pi
      if (first_angle - angle_max_difference <=
              second_angle <=
              first_angle + angle_max_difference):
        # tu pridavam do tmp
        tmp_ninetuple.append(lines_r_angle[second_idx])
    if len(tmp_ninetuple) == 9:
      ninetuples.append(np.abs(tmp_ninetuple))
    if len(tmp_ninetuple) > 9:
      tmp_ninetuple = np.array(tmp_ninetuple)
      sorted_r = np.sort(np.abs(tmp_ninetuple[:, 0]))
      median_r = sorted_r[len(tmp_ninetuple) // 2]
      tmp_rs = np.abs(tmp_ninetuple[:, 0]) - median_r
      sorted_idx = np.argsort(tmp_rs)
      ninetuples.append(tmp_ninetuple[sorted_idx[:9]])
    # tu pridam tmp to ninetuples pokud jich je > 9, dalsi resseni pak
  ninetuples = np.array(ninetuples)
  return ninetuples


def validate_ninetuple(ninetuple, acc_er_prc):
  r_s = np.abs(ninetuple[:, 0])
  idx_sorted = np.argsort(r_s)
  avg_dif = r_s[idx_sorted[1]] - r_s[idx_sorted[0]]
  for x in np.arange(2, 9):
    current_dif = r_s[idx_sorted[x]] - r_s[idx_sorted[x - 1]]
    if not (avg_dif - acc_er_prc * avg_dif <= current_dif <= avg_dif + acc_er_prc * avg_dif):
      return False
    avg_dif = ((x - 1) * avg_dif + current_dif) / x
  return True


def get_chessboard(lines_r_angle, parallel_angle_err=0.1, ninetuples_dist_err=0.2, ninetuples_ang_err=0.2):
  all_ninetuples = find_ninetuples(lines_r_angle, parallel_angle_err)
  valid_arr = np.zeros((all_ninetuples.shape[0]), dtype=np.bool)
  for ninetuple_idx in np.arange(all_ninetuples.shape[0]):
    valid_arr[ninetuple_idx] = validate_ninetuple(all_ninetuples[ninetuple_idx], ninetuples_dist_err)

  all_ninetuples = np.delete(all_ninetuples, ~valid_arr, axis=0)
  chess_ninetuples = chess_nine_tuplets_pairs(all_ninetuples, ninetuples_ang_err)
  chessboards = chessboard_from_pairs(chess_ninetuples)
  return chessboards
