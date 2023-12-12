import os
import subprocess
import tempfile
import shutil

root = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(os.path.join(root, "..", "data"))
bioteque_path = os.path.abspath(os.path.join(data_path, "bioteque"))


def download_gene_embeddings(metapath, dataset):
    cwd = os.getcwd()
    output_path = os.path.join(bioteque_path, metapath, dataset)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)
    tmp_folder = tempfile.mkdtemp()
    cmd = 'wget "https://bioteque.irbbarcelona.org/downloads/embeddings>GEN>{0}>{1}/embeddings.tar.gz" -O {2}/embeddings.tar.gz'.format(
        metapath, dataset, tmp_folder
    )
    subprocess.Popen(cmd, shell=True).wait()
    cmd = "cd {0}; tar -xf {1}/embeddings.tar.gz; cd {2}".format(
        output_path, tmp_folder, cwd
    )
    subprocess.Popen(cmd, shell=True).wait()
    keep_files = ["GEN_emb.h5", "GEN_ids.txt"]
    for fn in os.listdir(output_path):
        if fn not in keep_files:
            os.remove(os.path.join(output_path, fn))
    shutil.rmtree(tmp_folder)


download_gene_embeddings("GEN-ass-DIS", "opentargets")
download_gene_embeddings("GEN-ass-DIS", "disgenet_curated")
download_gene_embeddings("GEN-has-MFN", "gomf_goa_curated")
download_gene_embeddings("GEN-has-CMP", "jensencompartmentcurated")
download_gene_embeddings("GEN-ass-PWY", "reactome")
download_gene_embeddings("GEN-ppi-GEN", "string")
download_gene_embeddings("GEN-ppi-GEN", "huri_union")
download_gene_embeddings("GEN-pab-TIS", "hpa_proteome")
download_gene_embeddings("GEN-pdf-TIS", "hpa_proteome")
download_gene_embeddings("GEN-has-DOM", "interpro")
download_gene_embeddings("GEN-upr-CLL", "gdsc1000_mrna")
download_gene_embeddings("GEN-ppi-GEN", "hi_union")
download_gene_embeddings("GEN-cex-GEN", "coexpressdb")
