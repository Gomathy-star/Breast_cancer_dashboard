import pandas as pd

data = {
    "radius_mean":[14.2,17.5,12.0,20.0],
    "texture_mean":[20.1,25.0,15.0,30.0],
    "perimeter_mean":[90.0,110.0,75.0,130.0],
    "area_mean":[650.0,900.0,450.0,1400.0],
    "concavity_mean":[0.1,0.2,0.05,0.3],
    "concave_points_mean":[0.05,0.08,0.02,0.12],
    "radius_worst":[16.0,19.0,13.0,23.0],
    "perimeter_worst":[110.0,130.0,90.0,160.0],
    "area_worst":[800.0,1100.0,600.0,1800.0],
    "concave_points_worst":[0.07,0.09,0.03,0.15]
}

df = pd.DataFrame(data)
df.to_csv("sample_patients.csv", index=False)
print("sample_patients.csv created!")
