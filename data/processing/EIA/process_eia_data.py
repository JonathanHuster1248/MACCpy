import os
import pandas as pd


def merge_EIA(EIA_gen_file, EIA_plant_file, EIA_fuel_map_file, OUTFILE):
    cols = ["Plant Code", "Plant Name", "Generator ID", "Operating Year", "Prime Mover", "Nameplate Capacity (MW)", "Energy Source 1"]
    loc_cols = ["Plant Code", "State", "Latitude" ,"Longitude"]

    eia_data_operable = pd.read_excel(EIA_gen_file, sheet_name="Operable", skiprows = 1, usecols=cols)
    eia_data_retired = pd.read_excel(EIA_gen_file, sheet_name="Retired and Canceled", skiprows = 1, usecols=cols)
    eia_all = pd.concat([eia_data_operable, eia_data_retired])
    
    eia_loc = pd.read_excel(EIA_plant_file, sheet_name="Plant", skiprows = 1, usecols=loc_cols)
    eia_fuel_map = pd.read_csv(EIA_fuel_map_file, index_col = "Energy Source 1")
    fuel_dict = dict(zip(eia_fuel_map.index, eia_fuel_map.primary_fuel.values))
    

    eia_all['Nameplate Capacity (MW)'] = eia_all['Nameplate Capacity (MW)'].replace(' ', 0).fillna(0).astype(int)
    eia_all['Operating Year'] = eia_all['Operating Year'].replace(' ', 9999).fillna(9999).astype(int)
    
    eia_cap = eia_all.groupby(['Plant Code', "Plant Name"]).agg({'Nameplate Capacity (MW)': 'sum'})
    eia_year = eia_all.groupby(['Plant Code', "Plant Name"]).agg({'Operating Year': 'min'})
    eia_cap_fuel = eia_all.groupby(['Plant Code', "Plant Name", "Prime Mover", "Energy Source 1"]).agg({'Nameplate Capacity (MW)': 'sum'}).reset_index()

    eia_assumed_fuel = eia_cap_fuel.groupby(["Plant Code", "Plant Name"], as_index=False).apply(lambda df:df.sort_values("Nameplate Capacity (MW)", ascending=False).head(1)).droplevel(0).sort_values("Plant Code", ascending=False)[["Plant Code", "Plant Name", "Prime Mover", "Energy Source 1"]]

    eia_cap_fuel_pm = eia_assumed_fuel.merge(eia_year, on = "Plant Code", how = "left").merge(eia_cap, on = "Plant Code", how = "left").merge(eia_loc, on = "Plant Code", how = "left")

    eia_cap_fuel_pm["primary_fuel"] = eia_cap_fuel_pm["Energy Source 1"].map(fuel_dict)
    eia_cap_fuel_pm.to_csv(OUTFILE, index = False)
    return eia_cap_fuel_pm

def create_path(path):
    '''Helper function to create directories if needed.'''
    if not os.path.exists(path):
        os.makedirs(path)
    return path


if __name__ == "__main__":
    DIR = create_path('C:\\Users\\jonat\\OneDrive\\Desktop\\General\\School\\Stanford\\Research\\MACC\\MACCpy\\data\\processing\\EIA')
    EIA_FILE = os.path.join(DIR, "..", "..", "raw", "EIA", "2017", "3_1_Generator_Y2017.xlsx" )
    EIA_LOC_FILE = os.path.join(DIR, "..", "..", "raw", "EIA", "2017", "2___Plant_Y2017.xlsx" )
    EIA_FUEL_FILE = os.path.join(DIR, "eia_fuel_mapping.csv" )
    OUT_FILE = os.path.join(DIR, str(2017), "EIA_mapping_loc.csv")

    merge_EIA(EIA_FILE, EIA_LOC_FILE, EIA_FUEL_FILE, OUT_FILE)
    