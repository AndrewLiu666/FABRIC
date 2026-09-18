# Experiment Setup

Within each model variant, UNI and Virchow2 use the same recurrence labels, patient-level five-fold split, three client assignments, MIL architecture, optimizer, FL protocol, and evaluation. Only the frozen pathology encoder features and their input dimensions differ.

FABRIC offers two selectable MIL variants: `pooling` uses attention-weighted aggregation, and `topk` selects high- and low-scoring patch features for a second MIL tier. Select the variant with `--variant` and use a separate run name for each experiment.

| Setting | UNI | Virchow2 |
| --- | ---: | ---: |
| Input dimension | 1024 | 2560 |
| Patients | 804 | 804 |
| Feature files | 1284 | 1284 |
| FL rounds | 5 | 5 |
| Local epochs per round | 5 | 5 |

The three client training counts vary slightly by fold because the global patient-level test fold changes. All three participate in every round. Each starts from the same round-global model, trains locally, and returns full parameters. The server aggregates in the fixed order `CBTN_CQU`, `Harvard`, `EBRAINS`, weighted by each client's number of training patients.

The Adam optimizer and automatic mixed-precision (AMP) scaler are recreated for every local client task. Optimizer momentum is not carried across global rounds. There is no early stopping or best-round selection; the round-5 aggregate is evaluated.

Both variants support round-level recovery with `--resume`. Use the original run name, code version, and settings; see [NVIDIA FLARE workflow](NVFLARE_WORKFLOW.md) for checkpoint validation and recovery behavior.

The final test probability is computed from two logits. A threshold of 0.5 produces class predictions. AUC uses continuous recurrence probabilities. Reported means and sample standard deviations are calculated from the five patient-level test folds.

Random initialization uses `42 + fold*1000`. Local training uses `42 + fold*1000 + round*100 + client_index`, where rounds are numbered 1–5 and client indices follow the fixed aggregation order.

The code consumes previously extracted features and does not include slide preprocessing or UNI/Virchow2 feature extraction.

## Top-k feature selection

The Top-k model uses the following steps during both training and prediction:

1. Project each patch feature to the MIL embedding space and randomly partition the patient bag into pseudo-bags. The configured group count is eight; `torch.chunk` can return fewer nonempty groups for some bag sizes.
2. Apply attention pooling within each pseudo-bag and classify the pooled vector. Each pseudo-bag inherits its patient's recurrence label for weak supervision during training.
3. Apply the same classifier to each attention-weighted patch embedding to rank patches by recurrence score. The implementation sorts the binary logit margin, which gives the same ranking as recurrence probability without softmax saturation creating extra ties.
4. Select the K highest- and K lowest-scoring patches within each group. The default is K = 1 per high/low set. Overlapping selections in small groups are combined without duplicating patches.
5. Collect the selected projected patch embeddings into a distilled bag, then apply second-tier attention pooling and classification to predict patient-level recurrence.

Training uses random grouping from the seeded training generator. Prediction uses a separate generator with seed 42 for repeatable grouping without changing global random-number state or requiring patient labels.

The training loss is patient cross-entropy plus pseudo-bag cross-entropy with weight 1.0. Pseudo-bag losses are averaged within each patient, then combined across patients using the same class-weight normalization as patient cross-entropy. One Adam optimizer updates both tiers. The run configuration records the variant, K, pseudo-bag loss weight, and evaluation grouping seed.
