import numpy as np

from auxiliary import find_parallel_pair, find_intersection


def find_rhombus_quadruplets(parallel_pairs, angle_max_difference):
  quadruplets = []
  pi_half = np.pi / 2
  for first_idx in np.arange(len(parallel_pairs)):
    for second_idx in np.arange(first_idx + 1, len(parallel_pairs)):
      first_angle = parallel_pairs[first_idx][2]
      second_angle = parallel_pairs[second_idx][2]
      if first_angle < second_angle:
        first_angle += pi_half
      else:
        second_angle += pi_half
      if (first_angle - angle_max_difference <=
              second_angle <=
              first_angle + angle_max_difference):
        quadruplets.append([parallel_pairs[first_idx], parallel_pairs[second_idx]])
  return quadruplets


def _find_rhombuses(possible_rhomb_quadruplets, y_max, x_max):
  def within(lambda_x, lambda_y):
    return (0 <= lambda_y < y_max) and (0 <= lambda_x < x_max)

  rhombuses = []
  for quadruple in possible_rhomb_quadruplets:
    rhomb = []
    x, y = find_intersection(quadruple[0][0], quadruple[1][0])
    if within(x, y):
      rhomb.append([x, y])
    else:
      continue
    x, y = find_intersection(quadruple[0][0], quadruple[1][1])
    if within(x, y):
      rhomb.append([x, y])
    else:
      continue
    x, y = find_intersection(quadruple[0][1], quadruple[1][1])
    if within(x, y):
      rhomb.append([x, y])
    else:
      continue
    x, y = find_intersection(quadruple[0][1], quadruple[1][0])
    if within(x, y):
      rhomb.append([x, y])
    else:
      continue
    rhombuses.append(rhomb)
  rhombuses = np.asarray(rhombuses, dtype=int)
  if len(rhombuses) == 0:
    return np.array([])

  l1 = np.sqrt(np.sum((rhombuses[:, 0] - rhombuses[:, 1]) ** 2, axis=1))
  l2 = np.sqrt(np.sum((rhombuses[:, 1] - rhombuses[:, 2]) ** 2, axis=1))
  keep_idx = np.where((l1 + 0.1 * l1 > l2) & (l1 - (0.1 * l1) < l2))[0]

  return rhombuses[keep_idx, :]


def find_rhombuses(lines_r_angle, max_y, max_x, angle_par_err_max=0.1, angle_perp_err_max=0.1):
  parallel = find_parallel_pair(lines_r_angle, angle_par_err_max)
  pos_rhom_quadruplets = find_rhombus_quadruplets(parallel, angle_perp_err_max)

  if len(pos_rhom_quadruplets) > 0:
    rhombuses = _find_rhombuses(pos_rhom_quadruplets, max_y, max_x)
  else:
    return np.array([])
  return rhombuses


def get_rhombus_sizes(rhombuses):
  try:
    d1 = np.sqrt(np.sum((rhombuses[:, 0] - rhombuses[:, 2]) ** 2, axis=1))
    d2 = np.sqrt(np.sum((rhombuses[:, 1] - rhombuses[:, 3]) ** 2, axis=1))
  except IndexError:
    return np.array([])
  return d1 * d2 / 2
