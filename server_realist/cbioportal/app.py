import cbd
import pandas as pd
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

STUDIES = ['acc_tcga','blca_tcga','brca_tcga','cesc_tcga','chol_tcga','coadread_tcga','dlbc_tcga','esca_tcga','gbm_tcga','hnsc_tcga','kich_tcga','kirc_tcga','kirp_tcga','laml_tcga','lgg_tcga','lihc_tcga','luad_tcga','lusc_tcga','meso_tcga','ov_tcga','paad_tcga','pcpg_tcga','prad_tcga','sarc_tcga','skcm_tcga','stad_tcga','tgct_tcga','thca_tcga','thym_tcga','ucec_tcga','ucs_tcga','uvm_tcga']
STUDIES = STUDIES[:10]

def calc_alteration(data, gene):
    retdict = {}
    n_total = float(data.shape[0])
    tmp = data[['{}_GISTIC'.format(gene), '{}_MUT'.format(gene)]].sum(axis = 1).value_counts().to_dict()
    n_multiple = tmp.get(11, 0) + tmp.get(101, 0)
    n_mut = tmp.get(1, 0)
    n_homdel = tmp.get(100, 0)
    n_amp = tmp.get(10, 0)
    n_wt = tmp.get(0, 0)
    n_alt = n_multiple + n_mut + n_homdel + n_amp 

    retdict.update({'{}_PERC_AMP'.format(gene): n_amp*100/n_total})
    retdict.update({'{}_PERC_HOMDEL'.format(gene):n_homdel*100/n_total})
    retdict.update({'{}_PERC_MUT'.format(gene):n_mut*100/n_total})
    retdict.update({'{}_PERC_MULTIPLE'.format(gene):n_multiple*100/n_total})
    retdict.update({'{}_PERC_WT'.format(gene):n_wt*100/n_total})
    retdict.update({'PERC_ALT': n_alt*100/n_total})
    retdict.update({'N_TOTAL':n_total})
    return pd.Series(retdict)

@app.route('/<symbol>')
def tcga_alteration(symbol):
    gistic = cbd.get_gistic_calls(STUDIES,[symbol])
    gistic_status = gistic.applymap(lambda x: 10 if x=='amp' else 100 if x=='homdel' else 0 )
    mut = cbd.get_mutation(STUDIES,[symbol])
    mut = mut.fillna('wt')
    mut_status = mut.applymap(lambda x:x!='wt')
    joined = mut_status.drop('cancer_study_id', axis = 1).join(gistic_status.drop('cancer_study_id', axis = 1)).join(mut[['cancer_study_id']]).dropna()

    prev = joined.groupby('cancer_study_id').apply(calc_alteration, symbol).reset_index()
    prev['cancer_study_id'] = [ele.split('_')[0] for ele in prev.cancer_study_id.tolist()]
    prev = prev.ix[prev.N_TOTAL > 0,:]
    prev = prev.filter(regex='cancer|PERC', axis = 1)
    prev.columns = [ele.replace('{symbol}_PERC_'.format(symbol = symbol),'').lower() for ele in prev.columns]
    print(prev.head())
    prev = prev.sort_values('perc_alt', ascending = False)
    return prev.to_json(orient = 'records')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)

