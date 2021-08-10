import numpy as np


def sample_strategy_all(xs, ys):
  return xs, ys


def sample_strategy_every_nth(xs, ys, n):
  return xs[::n], ys[::n]


def sample_strategy_percentage_rand(xs, ys, percentage):
  if not (0 < percentage <= 1):
    percentage = 1
  total_samples = int(np.ceil(len(xs)*percentage))
  indices_chosen = np.random.choice(np.arange(len(xs)), total_samples, replace=False)
  return xs[indices_chosen], ys[indices_chosen]

