export SUBJECTS_DIR=/media/asier/Vanjas_Passport/FS_processed_data
export LC_NUMERIC="en_US.UTF-8"


## LEFT HEMISPHERE
mris_preproc --fsgd g2v1.fsgd \
  --cache-in thickness.fwhm10.fsaverage \
  --target fsaverage \
  --hemi lh \
  --out lh.g2v1.thickness.10.mgh

mri_glmfit \
  --y lh.g2v1.thickness.10.mgh \
  --fsgd g2v1.fsgd dods\
  --C group_x_tot.mtx \
  --C group.diff.mtx \
  --C g1g2.tot.mtx \
  --C g1g2.intercept.mtx \
  --surf fsaverage lh \
  --glmdir lh.g2v1

mri_glmfit-sim \
  --glmdir lh.g2v1 \
  --cache 4 neg \
  --cwp  0.05 \
  --2spaces


## RIGHT HEMISPHERE
mris_preproc --fsgd g2v1.fsgd \
  --cache-in thickness.fwhm10.fsaverage \
  --target fsaverage \
  --hemi rh \
  --out rh.g2v1.thickness.10.mgh

mri_glmfit \
  --y rh.g2v1.thickness.10.mgh \
  --fsgd g2v1.fsgd dods\
  --C group_x_tot.mtx \
  --C group.diff.mtx \
  --C g1g2.tot.mtx \
  --C g1g2.intercept.mtx \
  --surf fsaverage lh \
  --glmdir rh.g2v1

mri_glmfit-sim \
  --glmdir rh.g2v1 \
  --cache 4 neg \
  --cwp  0.05 \
  --2spaces


export PROC_DIR=/home/asier/git/surface-kljajevic-17
freeview -f $SUBJECTS_DIR/fsaverage/surf/lh.inflated:overlay=$PROC_DIR/lh.g2v1/g1g2.intercept/cache.th40.neg.sig.cluster.mgh:overlay_threshold=2,5:annot=$PROC_DIR/lh.g2v1/g1g2.intercept/cache.th40.neg.sig.ocn.annot -viewport 3d

