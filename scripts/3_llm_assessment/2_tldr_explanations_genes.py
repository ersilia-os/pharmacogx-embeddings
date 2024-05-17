import os
import sys

root = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(root, "..", "..", "src"))

from tldr import GeneTLDRExplanation

gt = GeneTLDRExplanation()

data_dir = os.path.join(root, "..", "..", "data", "tldr", "genes")
gids = []
for f in os.listdir(data_dir):
    gids.append(f.split(".")[0])

results_dir = os.path.join(root, "..", "..", "data", "tldr_explanations", "genes")
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

print("Working on {0} genes...".format(len(gids)))

for i, gid in enumerate(gids):
    print(i, gid)
    file_name = os.path.join(results_dir, "{0}.md".format(gid))
    if os.path.exists(file_name):
        continue
    text = gt.get(gid)
    with open(file_name, "w") as f:
        f.write(text)
    
