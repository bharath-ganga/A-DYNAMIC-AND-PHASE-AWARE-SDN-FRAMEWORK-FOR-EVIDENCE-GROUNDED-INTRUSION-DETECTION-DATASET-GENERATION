from pathlib import Path
import zipfile,csv,io,json,shutil,hashlib
root=Path('dist/evidence');(root/'graphs').mkdir(parents=True,exist_ok=True)
dataset=Path(r'C:/Users/bhara/OneDrive/Desktop/Bharath_cap/D05_FINAL_DATASET_EXPORT_v1.zip')
guide=Path(r'C:/Users/bhara/OneDrive/Desktop/Bharath_cap/FINAL RESULTS/FINAL_RESULTS_GUIDE_PACKAGE.zip')
def csvrows(blob):return list(csv.DictReader(io.StringIO(blob.decode('utf-8-sig'))))
titles={
'01_H14_split_sizes':'Train, validation, and test split sizes',
'02_H14_label_distribution':'Synthetic probing label distribution',
'05_H14_ROC_curves':'ROC curves · newly trained H14 models',
'06_H14_precision_recall_curves':'Precision–recall curves · newly trained H14 models',
'07_H14_feature_correlation':'H14 feature correlation',
'08_importance_Gradient_Boosting':'Gradient Boosting feature importance',
'08_importance_Random_Forest':'Random Forest feature importance',
'09_H14_phase_distribution':'H14 operational phase distribution',
'10_H14_scenario_distribution':'Four scenarios in the H14 export',
'11_PAPER_H23_Balanced_Accuracy':'H23 frozen-model balanced accuracy',
'11_PAPER_H23_Recall':'H23 frozen-model recall',
'11_PAPER_H23_FPR':'H23 frozen-model false positive rate',
'12_PAPER_H28_RTT':'H28 measured mean round-trip time',
'13_PAPER_H28_goodput':'H28 measured TCP bulk goodput'}
with zipfile.ZipFile(dataset) as z:
 blob=z.read('01_MAIN_DATASET/SDN_MAIN_H14_216_INTERVALS.csv');rows=csvrows(blob)
 assert len(rows)==216 and len(rows[0])==20
 runs={s:{r['run_id'] for r in rows if r['split']==s} for s in ['train','validation','test']}
 assert not (runs['train']&runs['test'] or runs['train']&runs['validation'] or runs['test']&runs['validation'])
 (root/'h14.csv').write_bytes(blob)
 (root/'dataset.json').write_text(json.dumps({'columns':list(rows[0]),'rows':rows,'sha256':hashlib.sha256(blob).hexdigest()},separators=(',',':')),encoding='utf-8')
 for split in ['TRAIN','VALIDATION','TEST']:(root/f'h14-{split.lower()}.csv').write_bytes(z.read(f'01_MAIN_DATASET/SDN_H14_{split}.csv'))
with zipfile.ZipFile(guide) as z:
 graphs=[]
 for n in sorted(z.namelist()):
  if '/03_GRAPHS_PNG/' not in n or not n.endswith('.png'):continue
  name=Path(n).name;stem=Path(n).stem;paper='PAPER' in stem
  title=titles.get(stem,stem.removeprefix('03_').removeprefix('04_').replace('_',' ').replace('CONFUSION','Confusion matrix ·').replace('H14 validation','H14 validation ·').replace('H14 test','H14 test ·'))
  group='paper' if paper else 'dataset' if stem[:2] in ['01','02','07','09','10'] else 'supplementary'
  graphs.append({'file':'evidence/graphs/'+name,'title':title,'group':group,'scope':'Paper · H23 frozen models' if 'H23' in stem else 'Paper · H28 network fidelity' if 'H28' in stem else 'H14 dataset analysis' if group=='dataset' else 'Supplementary · newly trained H14 models'})
  (root/'graphs'/name).write_bytes(z.read(n))
 (root/'graphs.json').write_text(json.dumps(graphs),encoding='utf-8')
 for source,dest in [('04_PAPER_REFERENCE_TABLES/H23_TABLE_IV_FROM_PAPER.csv','paper-h23.csv'),('04_PAPER_REFERENCE_TABLES/H28_TABLE_VI_FROM_PAPER.csv','paper-h28.csv'),('02_NEW_H14_MODEL_RESULTS/H14_NEW_ML_METRICS.csv','supplementary-h14-metrics.csv')]:
  (root/dest).write_bytes(z.read('FINAL RESULTS/'+source))
shutil.copyfile(dataset,root/'original-dataset-package.zip');shutil.copyfile(guide,root/'original-guide-package.zip')
print(f'Prepared {len(rows)} dataset rows and {len(graphs)} original graphs.')
