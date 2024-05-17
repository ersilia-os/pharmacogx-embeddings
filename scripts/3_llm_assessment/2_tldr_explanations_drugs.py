import os
import sys

root = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(root, "..", "..", "src"))

from tldr import DrugTLDRExplanation

dt = DrugTLDRExplanation()

data_dir = os.path.join(root, "..", "..", "data", "tldr", "drugs")
cids = []
for f in os.listdir(data_dir):
    cids.append(f.split(".")[0])

results_dir = os.path.join(root, "..", "..", "data", "tldr_explanations", "drugs")
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

print("Working on {0} drugs...".format(len(cids)))

for i, cid in enumerate(cids):
    print(i, cid)
    file_name = os.path.join(results_dir, "{0}.md".format(cid))
    if os.path.exists(file_name):
        continue
    text = dt.get(cid)
    with open(file_name, "w") as f:
        f.write(text)
    
