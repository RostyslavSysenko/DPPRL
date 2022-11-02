python -u FileEncoder.py ./datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_0_nump_5.csv
python -u FileEncoder.py ./datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_1_nump_5.csv
python -u FileEncoder.py -l ./datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_2_nump_5.csv
python -u FileEncoder.py -d ./datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_3_nump_5.csv
python -u FileEncoder.py -d ./datasets_synthetic/ncvr_numrec_5000_modrec_2_ocp_0_myp_4_nump_5.csv
python computeMetrics.py