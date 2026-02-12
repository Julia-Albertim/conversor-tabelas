import pandas as pd
def save_to_excel(data, filepath):
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
