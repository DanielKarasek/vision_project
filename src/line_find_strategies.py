import numpy as np


def retrieve_exact_lines(rhos, angles, N, M):
  lines = []
  # time this, with some picture with moderate amount of lines
  # if slow, try vectorize -> np zeros, create all -> remove too out of window possibly
  for rho, angle in zip(rhos, angles):
    tmp = []
    angle_sin = np.sin(angle) if 0 < angle < np.pi else 0.00001

    x = 0
    y = rho / angle_sin
    if 0 <= y <= M:
      tmp.append([int(x), int(y)])

    x = N
    y = (rho - x * np.cos(angle)) / angle_sin
    if 0 <= y <= M:
      tmp.append([int(x), int(y)])

    y = 0
    x = rho / np.cos(angle)
    if 0 <= x <= N:
      tmp.append([int(x), int(y)])

    y = M
    x = (rho - y * np.sin(angle)) / np.cos(angle)
    if 0 <= x <= N:
      tmp.append([int(x), int(y)])

    lines.append(tmp)
  lines = np.array(lines)
  return lines


def retrieve_longer_lines(rhos, angles, N, M):
  coef  = np.max([N, M]) * 2
  angles_sin = np.sin(angles)
  angles_cos = np.cos(angles)
  xs_0 = angles_cos * rhos
  ys_0 = angles_sin * rhos

  return np.array([[xs_0 - coef * angles_sin,
                    xs_0 + coef * angles_sin],
                   [ys_0 + coef * angles_cos,
                    ys_0 - coef * angles_cos]], dtype=int).T
