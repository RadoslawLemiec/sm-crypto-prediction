from experiments.experiment_def import run_expreminent


run_expreminent(look_back=1, hidden_size=4, batch_size=50, epochs=100, dropout=0.2, window_size=30, file_name="window-30.csv")
run_expreminent(look_back=1, hidden_size=4, batch_size=50, epochs=100, dropout=0.2, window_size=60, file_name="window-60.csv")
run_expreminent(look_back=1, hidden_size=4, batch_size=50, epochs=100, dropout=0.2, window_size=120, file_name="window-120.csv")
run_expreminent(look_back=1, hidden_size=4, batch_size=50, epochs=100, dropout=0.2, window_size=720, file_name="window-720.csv")
