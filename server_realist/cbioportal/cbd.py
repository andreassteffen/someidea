import pandas as pd

def set_suffix(mylist, suffix):
	return ['{}_{}'.format(element,suffix) for element in mylist]

def truncate(mystring, strlength = 20):
	return (mystring[:strlength-3] + '...') if len(mystring) > strlength else mystring

def clean_celllines(celllines):
	celllines = [str(cell).translate(None,'-_').upper() for cell in celllines.split('\n')]
	celllines = filter(None, celllines)
	return list(celllines)

URL = "http://www.cbioportal.org/public-portal/webservice.do"


def get_all_studies():
    url = "{base}?cmd={func}".format(base=URL, func="getCancerStudies")
    studies = pd.read_table(url)
    return studies


def get_tcga_provisional_studies():
    studies = get_all_studies()
    studies = studies[studies.cancer_study_id.str.endswith('tcga')]
    studies['name'] = studies.name.str.replace(' \(TCGA, Provisional\)', '')
    return studies.reset_index(drop=True)


def get_case_lists(cancer_study_id):
    url = "{base}?cmd={func}&cancer_study_id={cancer_study_id}".format(base=URL, func="getCaseLists",
                                                                       cancer_study_id=cancer_study_id)
    cases = pd.read_table(url)
    return cases


def get_genetic_profiles(cancer_study_id):
    url = "{base}?cmd={func}&cancer_study_id={cancer_study_id}".format(base=URL, func="getGeneticProfiles",
                                                                       cancer_study_id=cancer_study_id)
    profiles = pd.read_table(url)
    return profiles


def _get_data(cancer_study_ids, genes, case_suffix, profile_suffix, column_suffix):
    print("now in _get_data")
    gene_list = ','.join(genes if type(genes) == list else [genes])
    cancer_study_ids = cancer_study_ids if type(cancer_study_ids) == list else [cancer_study_ids]
    all_data = []
    for cancer_study_id in cancer_study_ids:
        case_list_id = "{cancer_study_id}_{case_suffix}".format(case_suffix=case_suffix,
                                                                cancer_study_id=cancer_study_id)
        profile_id = "{cancer_study_id}_{profile_suffix}".format(profile_suffix=profile_suffix,
                                                                 cancer_study_id=cancer_study_id)
        url = "{base}?cmd={func}"
        url += "&id_type=gene_symbol"
        url += "&cancer_study_id={cancer_study_id}"
        url += "&case_set_id={case_set_id}"
        url += "&genetic_profile_id={profile_id}"
        url += "&gene_list={gene_list}"
        url = url.format(base=URL, func="getProfileData", cancer_study_id=cancer_study_id, case_set_id=case_list_id,
                         profile_id=profile_id, gene_list=gene_list)
        try:
            data = pd.read_table(url, comment='#')
        except:
            continue
        if len(data) == 0:
            continue

        data.rename(columns={'COMMON': 'symbol'}, inplace=True)
        del data['GENE_ID']
        data.set_index('symbol', inplace=True)
        data = data.T
        data.columns = set_suffix(data.columns, column_suffix)
        data['cancer_study_id'] = cancer_study_id
        all_data.append(data)

    return pd.concat(all_data)


def get_gistic_calls(cancer_study_ids, genes, to_string_call=True):
    if (type(cancer_study_ids) == str) and (
        (cancer_study_ids == 'cellline_ccle_broad') or (cancer_study_ids == 'ccle')):
        data = _get_data('cellline_ccle_broad', genes, 'cna', 'CNA', 'GISTIC')
        data.index = [cell.split('_')[0] if not cell.split('_')[0] == 'TT' else cell for cell in data.index]
    else:
        data = _get_data(cancer_study_ids, genes, 'cna', 'gistic', 'GISTIC')
    if to_string_call:
        data.replace(-2, 'homdel', inplace=True)
        data.replace(-1, 'hetdel', inplace=True)
        data.replace(0, 'diploid', inplace=True)
        data.replace(1, 'gain', inplace=True)
        data.replace(2, 'amp', inplace=True)
    return data


def get_log2_copynumber(cancer_study_ids, genes):
    data = _get_data(cancer_study_ids, genes, 'cna', 'linear_CNA', 'LOG2CN')
    if (type(cancer_study_ids) == str) and (
        (cancer_study_ids == 'cellline_ccle_broad') or (cancer_study_ids == 'ccle')):
        data.index = [cell.split('_')[0] if not cell.split('_')[0] == 'TT' else cell for cell in data.index]
    return data


def get_rnaseq_log2tpm(cancer_study_ids, genes):
    data = _get_data(cancer_study_ids, genes, 'rna_seq_v2_mrna', 'rna_seq_v2_mrna', 'TPM')
    data = data.T.drop_duplicates().T

    for col in data.columns:
        if col == 'cancer_study_id':
            continue
        gene = col.split('_')[0]
        data['{gene}_LOG2TPM'.format(gene=gene)] = pd.np.log2(data['{gene}_TPM'.format(gene=gene)].astype('float')+1)
    return data


def get_methylation(cancer_study_ids, genes):
    data = _get_data(cancer_study_ids, genes, 'methylation_hm450', 'methylation_hm450', 'HM450')
    return data


def get_microarray(cancer_study_ids, genes):
    data = _get_data(cancer_study_ids, genes, 'mrna', 'mrna', 'MICROARRAY')
    return data


def get_microarray_zscores(cancer_study_ids, genes):
    data = _get_data(cancer_study_ids, genes, 'mrna', 'mrna_median_Zscores', 'MICROARRAY_ZSCORE')
    return data


def get_rnaseq_zscores(cancer_study_ids, genes):
    data = _get_data(cancer_study_ids, genes, 'rna_seq_v2_mrna', 'rna_seq_v2_mrna_median_Zscores', 'ZSCORE')
    genes = genes if type(genes) == list else [genes]
    return data


def get_mutation(cancer_study_ids, genes):
    return _get_data(cancer_study_ids, genes, 'sequenced', 'mutations', 'MUT')


def get_rppa(cancer_study_ids, genes):
    return _get_data(cancer_study_ids, genes, 'rppa', 'RPPA_protein_level', 'RPPA')

