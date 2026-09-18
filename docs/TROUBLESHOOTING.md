# Troubleshooting

- **Missing `data_paths.local.json`:** copy `configs/data_paths.example.json` and set the private manifest root.
- **Feature file not found:** add a path-prefix mapping rather than editing or reordering manifests.
- **AF_UNIX path too long:** keep the repository at a reasonably short path. The launcher already creates short temporary paths under `.tmp/`.
- **CUDA unavailable:** training requires a CUDA-capable GPU and a compatible PyTorch installation.
- **Existing run name:** use `--resume` to continue that run, or choose a new name for an independent experiment. Completed folds are preserved and skipped.
- **Interrupted run:** inspect `results/<run>/<experiment>/fold_<n>/simulator.log` (or the latest log under that fold's `resume_attempts/`), then repeat the original command with `--resume`. Keep the same code version, variant, Top-k value, data configuration, and run name. Recovery repeats an incomplete round from the last verified global checkpoint; it does not resume inside an epoch. Omit `--execute` to inspect the recovery plan without starting training.
- **Source-version mismatch on resume:** use the code revision that started the run. To use updated code, start a new run under a different name.
- **Checkpoint shape mismatch:** reconstruct the same `pooling` or `topk` model used by the saved run. The variants have different parameter sets and cannot share checkpoints interchangeably.
- **Disk usage:** FLARE exports a job and workspace for every fold. Ensure adequate space before starting both experiments.
