import os
import sys
import pandas as pd
import numpy as np


root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(root, ".."))


data_folder = os.path.abspath(os.path.join(root, "..", "..", "data"))
processed_folder = os.path.join(data_folder, "pharmgkb_processed")
haps_path = os.path.join(data_folder, "pharmgkb", "haplotypes")
df2 = pd.read_csv(os.path.join(processed_folder, "haplotype.csv"))
df2 = df2[["hid", "haplotype"]]

# Get a list of filenames in the directory
filenames = os.listdir(haps_path)
gene_list = []
for filename in filenames:
    fn = str(filename)
    if fn[-3:]=="csv":
        gene = fn.split("_")[0]
        gene_list += [gene]

for g in gene_list:
    df = pd.read_csv(os.path.join(haps_path, "{}_allele_definition_table.csv".format(g)))
    hap_dict = {}
    for i,r in enumerate(df.values):
        if i == 0:
            starts = r[1:]
        elif i == 1: 
            proteins = r[1:]
        elif i == 2 :
            ncs = r[1:]
        elif i == 3:
            ngs = r[1:]
        elif i == 4:
            rsids = r[1:]

    for i,r in enumerate(df.values):
        if i >= 6:
            hap = r[0]
            hap_dict[hap] = []
            for n,x in enumerate(r[1:]):
                if x is not np.nan:
                    rsid = rsids[n]
                    start = starts[n]
                    protein = proteins[n]
                    nc = ncs[n]
                    ng = ngs[n]
                    hap_dict[hap] += [[rsid, start, protein, nc, ng]]

    df_rows = []
    for key, value in hap_dict.items():
        if isinstance(value, list):
            for sublist in value:
                df_rows.append([key] + sublist)
        else:
            df_rows.append([key] + value)

    df1 = pd.DataFrame(df_rows)
    df1.columns = ["haplotype_number", "rsID", "start", "protein", "NC", "NG"]
    df1["gene"] = [g]*len(df1)

    df1["haplotype"] = df1.apply(lambda row: row["gene"] + str(row["haplotype_number"]) if str(row["haplotype_number"]).startswith("*") else row["gene"] + " " + str(row["haplotype_number"]), axis=1)

    #add haplotype ID number to see how many do not have it
    data = pd.merge(df1, df2, on = "haplotype", how = "left")

    #manual curation of missed haplotypes
    if g == "ABCG2":
        data.loc[data["haplotype"] == "ABCG2 rs2231142 reference (G)", "hid"] = "PA166287823"
        data.loc[data["haplotype"] == "ABCG2 rs2231142 variant (T)", "hid"] = "PA166287824"
    elif g == "CACNA1S":
        data.loc[data["haplotype"] == "CACNA1S Reference", "hid"] = "PA166180429"
    elif g == "CYP1A2":
        data.loc[data["haplotype"] == "CYP1A2*1G", "hid"] = "PA165819177"
        data.loc[data["haplotype"] == "CYP1A2*1H", "hid"] = "PA165819192"
        data.loc[data["haplotype"] == "CYP1A2*1M", "hid"] = "PA165988095"
        data.loc[data["haplotype"] == "CYP1A2*1N", "hid"] = "PA165988096"
        data.loc[data["haplotype"] == "CYP1A2*1P", "hid"] = "PA165988097"
        data.loc[data["haplotype"] == "CYP1A2*1Q", "hid"] = "PA165988098"
        data.loc[data["haplotype"] == "CYP1A2*1R", "hid"] = "PA165988099"
        data.loc[data["haplotype"] == "CYP1A2*1S", "hid"] = "PA165988100"
        data.loc[data["haplotype"] == "CYP1A2*1T", "hid"] = "PA165988101"
        data.loc[data["haplotype"] == "CYP1A2*1U", "hid"] = "PA165988102"
        data.loc[data["haplotype"] == "CYP1A2*2", "hid"] = "PA165819180"
        data.loc[data["haplotype"] == "CYP1A2*5", "hid"] = "PA165819193"
        data.loc[data["haplotype"] == "CYP1A2*8", "hid"] = "PA165819185"
        data.loc[data["haplotype"] == "CYP1A2*9", "hid"] = "PA165819194"
        data.loc[data["haplotype"] == "CYP1A2*10", "hid"] = "PA165819186"
        data.loc[data["haplotype"] == "CYP1A2*12", "hid"] = "PA165819195"
        data.loc[data["haplotype"] == "CYP1A2*13", "hid"] = "PA165819188"
        data.loc[data["haplotype"] == "CYP1A2*14", "hid"] = "PA165819189"
        data.loc[data["haplotype"] == "CYP1A2*15", "hid"] = "PA165819190"
        data.loc[data["haplotype"] == "CYP1A2*16", "hid"] = "PA165819191"
        data.loc[data["haplotype"] == "CYP1A2*17", "hid"] = "PA165819196"
        data.loc[data["haplotype"] == "CYP1A2*18", "hid"] = "PA165819197"
        data.loc[data["haplotype"] == "CYP1A2*19", "hid"] = "PA165819198"
        data.loc[data["haplotype"] == "CYP1A2*20", "hid"] = "PA165819199"
        data.loc[data["haplotype"] == "CYP1A2*21", "hid"] = "PA165819200"
    elif g == "CYP2A6":
        data.loc[data["haplotype"] == "CYP2A6*1", "hid"] = "PA165924690"
        data.loc[data["haplotype"] == "CYP2A6*4", "hid"] = "PA165924721"
        data.loc[data["haplotype"] == "CYP2A6*8", "hid"] = "PA165924732"
        data.loc[data["haplotype"] == "CYP2A6*24", "hid"] = "PA165924753"
        data.loc[data["haplotype"] == "CYP2A6*28", "hid"] = "PA165924758"
        data.loc[data["haplotype"] == "CYP2A6*31", "hid"] = "PA166279710"
        data.loc[data["haplotype"] == "CYP2A6*34", "hid"] = "PA165924762"
        data.loc[data["haplotype"] == "CYP2A6*36", "hid"] = "PA165924765"
        data.loc[data["haplotype"] == "CYP2A6*37", "hid"] = "PA165924766"
        data.loc[data["haplotype"] == "CYP2A6*39", "hid"] = "PA166117265"
        data.loc[data["haplotype"] == "CYP2A6*40", "hid"] = "PA166117266"
        data.loc[data["haplotype"] == "CYP2A6*41", "hid"] = "PA166117267"
        data.loc[data["haplotype"] == "CYP2A6*42", "hid"] = "PA166117268"
        data.loc[data["haplotype"] == "CYP2A6*43", "hid"] = "PA166117269"
        data.loc[data["haplotype"] == "CYP2A6*44", "hid"] = "PA166117270"
        data.loc[data["haplotype"] == "CYP2A6*45", "hid"] = "PA166117271"
        data.loc[data["haplotype"] == "CYP2A6*46", "hid"] = "PA165924691"
        data.loc[data["haplotype"] == "CYP2A6*47", "hid"] = "PA165924724"
        data.loc[data["haplotype"] == "CYP2A6*48", "hid"] = "PA166279711"
        data.loc[data["haplotype"] == "CYP2A6*49", "hid"] = "PA166279712"
        data.loc[data["haplotype"] == "CYP2A6*50", "hid"] = "PA166279713"
        data.loc[data["haplotype"] == "CYP2A6*51", "hid"] = "PA166279714"
        data.loc[data["haplotype"] == "CYP2A6*52", "hid"] = "PA166279715"
        data.loc[data["haplotype"] == "CYP2A6*53", "hid"] = "PA166299421"
    elif g == "CYP2B6":
        data.loc[data["haplotype"] == "CYP2B6*39", "hid"] = "PA166290053"
        data.loc[data["haplotype"] == "CYP2B6*40", "hid"] = "PA166290054"
        data.loc[data["haplotype"] == "CYP2B6*41", "hid"] = "PA166290055"
        data.loc[data["haplotype"] == "CYP2B6*42", "hid"] = "PA166290056"
        data.loc[data["haplotype"] == "CYP2B6*43", "hid"] = "PA166290057"
        data.loc[data["haplotype"] == "CYP2B6*44", "hid"] = "PA166290058"
        data.loc[data["haplotype"] == "CYP2B6*45", "hid"] = "PA166290059"
        data.loc[data["haplotype"] == "CYP2B6*46", "hid"] = "PA166290060"
        data.loc[data["haplotype"] == "CYP2B6*47", "hid"] = "PA166290061"
        data.loc[data["haplotype"] == "CYP2B6*48", "hid"] = "PA166290062"
        data.loc[data["haplotype"] == "CYP2B6*49", "hid"] = "PA166290063"
    elif g == "CYP2C8":
        data.loc[data["haplotype"] == "CYP2C8*5", "hid"] = "PA165958687"
        data.loc[data["haplotype"] == "CYP2C8*6", "hid"] = "PA165958688"
        data.loc[data["haplotype"] == "CYP2C8*7", "hid"] = "PA165958689"
        data.loc[data["haplotype"] == "CYP2C8*8", "hid"] = "PA165958690"
        data.loc[data["haplotype"] == "CYP2C8*9", "hid"] = "PA165958691"
        data.loc[data["haplotype"] == "CYP2C8*10", "hid"] = "PA165958692"
        data.loc[data["haplotype"] == "CYP2C8*11", "hid"] = "PA165958693"
        data.loc[data["haplotype"] == "CYP2C8*12", "hid"] = "PA165958694"
        data.loc[data["haplotype"] == "CYP2C8*13", "hid"] = "PA165958695"
        data.loc[data["haplotype"] == "CYP2C8*14", "hid"] = "PA165958696"
        data.loc[data["haplotype"] == "CYP2C8*15", "hid"] = "PA166242949"
        data.loc[data["haplotype"] == "CYP2C8*16", "hid"] = "PA166242950"
        data.loc[data["haplotype"] == "CYP2C8*17", "hid"] = "PA166242951"
        data.loc[data["haplotype"] == "CYP2C8*18", "hid"] = "PA166242952"
    elif g == "CYP2C9":
        data.loc[data["haplotype"] == "CYP2C9*63", "hid"] = "PA166243717"
        data.loc[data["haplotype"] == "CYP2C9*64", "hid"] = "PA166243718"
        data.loc[data["haplotype"] == "CYP2C9*65", "hid"] = "PA166243719"
        data.loc[data["haplotype"] == "CYP2C9*66", "hid"] = "PA166243720"
        data.loc[data["haplotype"] == "CYP2C9*67", "hid"] = "PA166243721"
        data.loc[data["haplotype"] == "CYP2C9*68", "hid"] = "PA166243722"
        data.loc[data["haplotype"] == "CYP2C9*69", "hid"] = "PA166243723"
        data.loc[data["haplotype"] == "CYP2C9*70", "hid"] = "PA166243724"
        data.loc[data["haplotype"] == "CYP2C9*71", "hid"] = "PA166243725"
        data.loc[data["haplotype"] == "CYP2C9*72", "hid"] = "PA166257325"
        data.loc[data["haplotype"] == "CYP2C9*73", "hid"] = "PA166257326"
        data.loc[data["haplotype"] == "CYP2C9*74", "hid"] = "PA166257327"
        data.loc[data["haplotype"] == "CYP2C9*75", "hid"] = "PA166257328"
        data.loc[data["haplotype"] == "CYP2C9*76", "hid"] = "PA166269371"
        data.loc[data["haplotype"] == "CYP2C9*77", "hid"] = "PA166269372"
        data.loc[data["haplotype"] == "CYP2C9*78", "hid"] = "PA166269373"
        data.loc[data["haplotype"] == "CYP2C9*79", "hid"] = "PA166269374"
        data.loc[data["haplotype"] == "CYP2C9*80", "hid"] = "PA166269375"
        data.loc[data["haplotype"] == "CYP2C9*81", "hid"] = "PA166269376"
        data.loc[data["haplotype"] == "CYP2C9*82", "hid"] = "PA166269377"
        data.loc[data["haplotype"] == "CYP2C9*83", "hid"] = "PA166269378"
        data.loc[data["haplotype"] == "CYP2C9*84", "hid"] = "PA166269379"
        data.loc[data["haplotype"] == "CYP2C9*85", "hid"] = "PA166269380"
    elif g == "CYP2C19":
        data.loc[data["haplotype"] == "CYP2C19*39", "hid"] = "PA166243734"
    elif g == "CYP2D6":
        data.loc[data["haplotype"] == "CYP2D6*140", "hid"] = "PA166243647"
        data.loc[data["haplotype"] == "CYP2D6*141", "hid"] = "PA166243648"
        data.loc[data["haplotype"] == "CYP2D6*142", "hid"] = "PA166243649"
        data.loc[data["haplotype"] == "CYP2D6*143", "hid"] = "PA166243650"
        data.loc[data["haplotype"] == "CYP2D6*144", "hid"] = "PA166243651"
        data.loc[data["haplotype"] == "CYP2D6*145", "hid"] = "PA166243652"
        data.loc[data["haplotype"] == "CYP2D6*146", "hid"] = "PA166254043"
        data.loc[data["haplotype"] == "CYP2D6*147", "hid"] = "PA166254044"
        data.loc[data["haplotype"] == "CYP2D6*148", "hid"] = "PA166262301"
        data.loc[data["haplotype"] == "CYP2D6*149", "hid"] = "PA166254045"
        data.loc[data["haplotype"] == "CYP2D6*150", "hid"] = "PA166281708"
        data.loc[data["haplotype"] == "CYP2D6*151", "hid"] = "PA166281709"
        data.loc[data["haplotype"] == "CYP2D6*152", "hid"] = "PA166274897"
        data.loc[data["haplotype"] == "CYP2D6*153", "hid"] = "PA166274898"
        data.loc[data["haplotype"] == "CYP2D6*154", "hid"] = "PA166274899"
        data.loc[data["haplotype"] == "CYP2D6*155", "hid"] = "PA166274900"
        data.loc[data["haplotype"] == "CYP2D6*156", "hid"] = "PA166274901"
        data.loc[data["haplotype"] == "CYP2D6*157", "hid"] = "PA166274902"
        data.loc[data["haplotype"] == "CYP2D6*158", "hid"] = "PA166274903"
        data.loc[data["haplotype"] == "CYP2D6*159", "hid"] = "PA166274904"
        data.loc[data["haplotype"] == "CYP2D6*160", "hid"] = "PA166274905"
        data.loc[data["haplotype"] == "CYP2D6*161", "hid"] = "PA166274906"
        data.loc[data["haplotype"] == "CYP2D6*162", "hid"] = "PA166274907"
        data.loc[data["haplotype"] == "CYP2D6*163", "hid"] = "PA166274908"
        data.loc[data["haplotype"] == "CYP2D6*164", "hid"] = "PA166281710"
        data.loc[data["haplotype"] == "CYP2D6*165", "hid"] = "PA166281711"
        data.loc[data["haplotype"] == "CYP2D6*166", "hid"] = "PA166281712"
        data.loc[data["haplotype"] == "CYP2D6*167", "hid"] = "PA166281713"
        data.loc[data["haplotype"] == "CYP2D6*168", "hid"] = "PA166281714"
        data.loc[data["haplotype"] == "CYP2D6*169", "hid"] = "PA166281715"
        data.loc[data["haplotype"] == "CYP2D6*170", "hid"] = "PA166281716"
        data.loc[data["haplotype"] == "CYP2D6*171", "hid"] = "PA166281717"
        data.loc[data["haplotype"] == "CYP2D6*172", "hid"] = "PA166304182"
    elif g == "CYP2E1":
        data.loc[data["haplotype"] == "CYP2E1*2", "hid"] = "PA165948036"
        data.loc[data["haplotype"] == "CYP2E1*3", "hid"] = "PA165948037"
        data.loc[data["haplotype"] == "CYP2E1*4", "hid"] = "PA165948038"
        data.loc[data["haplotype"] == "CYP2E1*7", "hid"] = "PA165981619"
        data.loc[data["haplotype"] == "CYP2E1*/A", "hid"] = "PA165948042"
        data.loc[data["haplotype"] == "CYP2E1*7B", "hid"] = "PA165948043"
        data.loc[data["haplotype"] == "CYP2E1*7C", "hid"] = "PA165948044"
    elif g == "CYP3A4":
        data.loc[data["haplotype"] == "CYP3A4*35", "hid"] = "PA166245591"
        data.loc[data["haplotype"] == "CYP3A4*37", "hid"] = "PA166270241"
        data.loc[data["haplotype"] == "CYP3A4*38", "hid"] = "PA166287701"
    elif g == "CYP3A5":
        data.loc[data["haplotype"] == "CYP3A5*8", "hid"] = "PA166128235"
        data.loc[data["haplotype"] == "CYP3A5*9", "hid"] = "PA166128236"
    elif g == "CYP3A7":
        data.loc[data["haplotype"] == "CYP3A7*1B", "hid"] = "PA165948046"
        data.loc[data["haplotype"] == "CYP3A7*1D", "hid"] = "PA165948048"
        data.loc[data["haplotype"] == "CYP3A7*1E", "hid"] = "PA165948049"
        data.loc[data["haplotype"] == "CYP3A7*2", "hid"] = "PA165948050"
        data.loc[data["haplotype"] == "CYP3A7*3", "hid"] = "PA165948051"
    elif g == "CYP4F2":
        data.loc[data["haplotype"] == "CYP4F2*2", "hid"] = "PA165860686"
        data.loc[data["haplotype"] == "CYP4F2*4", "hid"] = "PA166287623"
        data.loc[data["haplotype"] == "CYP4F2*5", "hid"] = "PA166287624"
        data.loc[data["haplotype"] == "CYP4F2*6", "hid"] = "PA166287625"
        data.loc[data["haplotype"] == "CYP4F2*7", "hid"] = "PA166287626"
        data.loc[data["haplotype"] == "CYP4F2*8", "hid"] = "PA166304149"
        data.loc[data["haplotype"] == "CYP4F2*9", "hid"] = "PA166304150"
        data.loc[data["haplotype"] == "CYP4F2*10", "hid"] = "PA166304151"
        data.loc[data["haplotype"] == "CYP4F2*11", "hid"] = "PA166304152"
        data.loc[data["haplotype"] == "CYP4F2*12", "hid"] = "PA166304153"
        data.loc[data["haplotype"] == "CYP4F2*13", "hid"] = "PA166304154"
        data.loc[data["haplotype"] == "CYP4F2*14", "hid"] = "PA166304155"
        data.loc[data["haplotype"] == "CYP4F2*15", "hid"] = "PA166304156"
        data.loc[data["haplotype"] == "CYP4F2*16", "hid"] = "PA166304157"




    data.to_csv(os.path.join(processed_folder, "haplotypes_gene", "{}_haplotypes.csv".format(g)), index=False)