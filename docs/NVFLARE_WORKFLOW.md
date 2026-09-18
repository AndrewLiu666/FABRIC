# NVIDIA FLARE Workflow

The entry point exports one NVIDIA FLARE `FedAvgRecipe` per encoder and fold. NVIDIA FLARE's FedAvg workflow coordinates training rounds and calls FABRIC's custom `ModelAggregator` implementation to average updates by each client's number of training patients. The aggregator uses a fixed client order and retains non-floating buffers from the first client.

`ScriptRunner` configures `PTClientAPILauncherExecutor` to launch local FABRIC training in a separate client process. The NVIDIA FLARE Client API receives the global PyTorch state dictionary and returns locally updated parameters, training loss, and metadata. Metadata includes the client identity, training-patient count, round, seed, and input-state hash. `PTFileModelPersistor` loads and saves shared model weights.

The local simulator registers three logical clients with one concurrent execution slot, so the provided configuration trains clients sequentially on one GPU. All three clients participate in every round and start from the same global model.

## Completion checks

Before test evaluation, the runner requires a successful simulator process exit and verifies:

- Five server aggregation records and 15 client updates per fold, with the expected client order and round numbers.
- A final checkpoint containing all five completed rounds.
- Matching state hashes for the final checkpoint, the final aggregation record, and NVIDIA FLARE's persisted model.

The final model is evaluated on the held-out patient fold, and fold metrics are combined into a five-fold summary.

## Resuming a run

Both FABRIC variants support `--resume` in the existing result directory. Resume validation checks the saved configuration, manifests, and recorded source hashes. **Use the same code version that started the run.** If code has changed, restore that revision before resuming, or start an independent run under a new name. Do not bypass the source checks.

Recovery selects the latest global checkpoint that matches its aggregation record. Each round checkpoint is saved atomically before the audit record is written. Completed folds are skipped; an unfinished round restarts from the last verified global model. The original absolute round number and client seeds are preserved. Recovery does not continue from the middle of a local epoch.

If all rounds finished but evaluation was interrupted, the runner verifies the final NVIDIA FLARE checkpoint and reruns evaluation without further training. Recovery attempts keep their job exports and logs under `resume_attempts/`; incomplete records are archived there before a round is repeated.

Omit `--execute` to inspect a recovery plan without starting training. A resumed fold's wall-time fields cover that invocation, while the sum of client-training times includes all completed rounds.
