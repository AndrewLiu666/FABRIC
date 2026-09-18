"""Model-state copying and patient-count-weighted FedAvg."""

from __future__ import annotations

from typing import Sequence
import torch


def copy_state_dict(state_dict: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    return {key: value.detach().cpu().clone() for key, value in state_dict.items()}


def fedavg_state_dict(states: Sequence[dict[str, torch.Tensor]], weights: Sequence[int]) -> dict[str, torch.Tensor]:
    total = float(sum(weights))
    if total <= 0:
        raise ValueError("FedAvg received zero total client weight")
    averaged: dict[str, torch.Tensor] = {}
    for key in states[0]:
        first = states[0][key]
        if not torch.is_floating_point(first):
            averaged[key] = first.clone()
            continue
        value = torch.zeros_like(first, dtype=torch.float32)
        for state, weight in zip(states, weights):
            value += state[key].float() * (float(weight) / total)
        averaged[key] = value.to(dtype=first.dtype)
    return averaged
