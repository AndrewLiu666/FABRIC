# Reproducibility Record

Both FABRIC variants, `pooling` and `topk`, have completed NVIDIA FLARE 2.7.2 runs: five UNI folds and five Virchow2 folds per variant. Every fold recorded five server aggregations, three client contributions per round, a matching framework-persisted model, predictions, and final metrics. The Top-k experiments used K = 1 for each high/low set.

The resulting five-fold summaries were:

| Experiment | Variant | AUC mean | AUC SD | BACC mean | BACC SD | ACC mean | ACC SD |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| UNI | `pooling` | 0.6442315096251265 | 0.038115029353321186 | 0.6288449848024317 | 0.057440507674056944 | 0.7151397515527951 | 0.031898979545280835 |
| UNI | `topk` | 0.6173651758575771 | 0.05338137836289219 | 0.5721580547112463 | 0.06848356775927386 | 0.7176164596273292 | 0.025009407830178673 |
| Virchow2 | `pooling` | 0.6492596613113332 | 0.017959434307833724 | 0.6219604863221885 | 0.0429184349596534 | 0.7176863354037268 | 0.012214931609405169 |
| Virchow2 | `topk` | 0.649039875524678 | 0.04898753245371643 | 0.5909726443768998 | 0.05885101676961675 | 0.7089829192546583 | 0.03813878052197939 |

SD denotes sample standard deviation across the five patient-level test folds.

Exact numerical equality requires the same manifests, feature tensors, feature ordering, model variant, and experiment settings, together with a compatible software and hardware environment. GPU and CUDA/cuDNN differences can affect floating-point results. Record the environment and all five fold values alongside summary metrics. Data requirements are described in [Private Data Format](DATA_FORMAT.md); completion checks and recovery are described in [NVIDIA FLARE Workflow](NVFLARE_WORKFLOW.md).
