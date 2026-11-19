NEW SDN MODEL EXPERIMENT: LSTM, GRU, SMALL/LIGHTWEIGHT GRU AND RANDOM FOREST
=========================================================================
Data: Your real H14 TRAIN / VALIDATION / TEST CSVs.
Label 1 = SYNTHETIC probing, not confirmed real cyberattack.
All models are evaluated on the independent H14 TEST partition.
The 3 recurrent models are NEW EXPERIMENTS, not part of the final paper.
Do not attach these results to the submitted paper as if previously reported.
Training observations: only 72; interpret DL results as pilot results.
DL sequences: current and 2 previous time-ordered windows WITHIN the same run.
Random Forest sees identical window history flattened into fixed features.
Model performance: Tables/FOUR_MODELS_H14_VALIDATION_TEST.csv
Sizes and timing: Tables/MODEL_SIZE_CPU_LATENCY.csv
See experiment_config.json for technical and validity limitations.
