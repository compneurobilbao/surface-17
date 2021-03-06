export SUBJECTS_DIR=/media/asier/Vanjas_Passport/FS_processed_data
export LC_NUMERIC="en_US.UTF-8"
export FWHM=20

## LEFT HEMISPHERE
mris_preproc --fsgd g2v2.fsgd \
  --cache-in thickness.fwhm$FWHM.fsaverage \
  --target fsaverage \
  --hemi lh \
  --out lh.g2v2.thickness.$FWHM.mgh

mri_glmfit \
  --y lh.g2v2.thickness.$FWHM.mgh \
  --fsgd g2v2.fsgd dods\
  --C group_x_gender.mtx \
  --C group.diff.mtx \
  --surf fsaverage lh \
  --cortex \
  --glmdir lh.g2v2

#mri_glmfit-sim \
#  --glmdir lh.g2v2 \
#  --cache 4 abs \
#  --cwp  0.05 \
#  --2spaces


## RIGHT HEMISPHERE
mris_preproc --fsgd g2v2.fsgd \
  --cache-in thickness.fwhm$FWHM.fsaverage \
  --target fsaverage \
  --hemi rh \
  --out rh.g2v2.thickness.$FWHM.mgh

mri_glmfit \
  --y rh.g2v2.thickness.$FWHM.mgh \
  --fsgd g2v2.fsgd dods\
  --C group_x_gender.mtx \
  --C group.diff.mtx \
  --surf fsaverage rh \
  --cortex \
  --glmdir rh.g2v2

#mri_glmfit-sim \
#  --glmdir rh.g2v2 \
#  --cache 2 pos \
#  --cwp  0.05 \
#  --2spaces




## Secondary commands (Visualization)
export PROC_DIR=/home/asier/git/surface-kljajevic-17
export HEMI="rh" # lh or rh
export CONTRAST="group.diff" #contrast: group_x_gender or group.diff


# After preproc
#mri_info $HEMI.g2v1.thickness.${FWHM}.mgh


# After glmfit
freeview -f $SUBJECTS_DIR/fsaverage/surf/$HEMI.inflated:annot=aparc.annot:annot_outline=1:overlay=$PROC_DIR/$HEMI.g2v2/$CONTRAST/sig.mgh:overlay_threshold=2,5 -viewport 3d &


# After glmfit-sim
#less $PROC_DIR/$HEMI.g2v2/$CONTRAST/cache.th20.pos.sig.cluster.summary #careful with pos. thXX.

#freeview -f $SUBJECTS_DIR/fsaverage/surf/$HEMI.inflated:overlay=$PROC_DIR/$HEMI.g2v2/$CONTRAST/#cache.th40.neg.sig.cluster.mgh:overlay_threshold=2,5:annot=$PROC_DIR/$HEMI.g2v2/$CONTRAST/#cache.th40.neg.sig.ocn.annot -viewport 3d


# FDR correction
mri_surfcluster --in $PROC_DIR/$HEMI.g2v2/$CONTRAST/sig.mgh \
   --hemi $HEMI --thmin 2 --thmax 5 --thsign pos \
   --fdr 0.05 \
   --minarea 5 --sum summaryfile_${HEMI}_${CONTRAST}_${FWHM} \
   --subject fsaverage --annot aparc --o ./RES_${HEMI}_${CONTRAST}_${FWHM}










