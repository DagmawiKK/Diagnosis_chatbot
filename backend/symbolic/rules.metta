;; Rule 1: Asthma diagnosis
!(add-reduct &medical_kb (: asthma_diagnosis_rule
                  (-> (Presents $patient wheezing)
                      (-> (Presents $patient chest_tightness)
                          (-> (Presents $patient dyspnea)
                              (-> (Shows spirometry $patient obstructive_pattern)
                                  (-> (Shows methacholine_challenge $patient bronchial_hyperreactivity)
                                      (-> (HasRiskFactor $patient family_history_atopy)
                                          (DiagnosedWith $patient asthma)))))))))

;; Rule 2: COPD diagnosis 
!(add-reduct &medical_kb (: copd_diagnosis_rule
                  (-> (Presents $patient persistent_cough)
                      (-> (Presents $patient dyspnea)
                          (-> (Presents $patient productive_cough)
                              (-> (HasRiskFactor $patient tobacco_use_disorder)
                                  (-> (Shows spirometry $patient obstructive_pattern)
                                      (-> (Shows ct_chest $patient emphysematous_changes)
                                          (DiagnosedWith $patient copd)))))))))

;; Rule 3: Pneumonia diagnosis 
!(add-reduct &medical_kb (: pneumonia_diagnosis_rule
                  (-> (Presents $patient fever)
                      (-> (Presents $patient productive_cough)
                          (-> (Presents $patient chest_pain)
                              (-> (Presents $patient dyspnea)
                                  (-> (Shows chest_xray $patient infiltrates)
                                      (-> (Shows sputum_culture $patient bacterial_growth)
                                          (DiagnosedWith $patient pneumonia)))))))))

;; Rule 4: Tuberculosis diagnosis 
!(add-reduct &medical_kb (: tuberculosis_diagnosis_rule
                  (-> (Presents $patient persistent_cough)
                      (-> (Presents $patient weight_loss)
                          (-> (Presents $patient night_sweats)
                              (-> (Presents $patient hemoptysis)
                                  (-> (Shows tuberculin_skin_test $patient positive_reaction)
                                      (-> (Shows chest_xray $patient infiltrates)
                                          (DiagnosedWith $patient pulmonary_tuberculosis)))))))))

;; Rule 5: Lung cancer diagnosis 
!(add-reduct &medical_kb (: lung_cancer_diagnosis_rule
                  (-> (Presents $patient persistent_cough)
                      (-> (Presents $patient weight_loss)
                          (-> (Presents $patient chest_pain)
                              (-> (Presents $patient hemoptysis)
                                  (-> (HasRiskFactor $patient tobacco_use_disorder)
                                      (-> (Shows ct_chest $patient pulmonary_nodules)
                                          (-> (Shows bronchoscopy $patient malignant_tissue)
                                              (DiagnosedWith $patient lung_cancer))))))))))

;; Rule 6: Pulmonary embolism diagnosis 
!(add-reduct &medical_kb (: pulmonary_embolism_diagnosis_rule
                  (-> (Presents $patient dyspnea)
                      (-> (Presents $patient chest_pain)
                          (-> (Presents $patient tachypnea)
                              (-> (HasRiskFactor $patient prolonged_immobilization)
                                  (-> (Shows pulse_oximetry $patient hypoxemia)
                                      (-> (Shows ct_pulmonary_angiogram $patient pulmonary_embolus)
                                          (DiagnosedWith $patient pulmonary_embolism)))))))))

;; Rule 7: Bronchitis diagnosis 
!(add-reduct &medical_kb (: acute_bronchitis_diagnosis_rule
                  (-> (Presents $patient persistent_cough)
                      (-> (Presents $patient productive_cough)
                          (-> (Presents $patient chest_tightness)
                              (-> (Presents $patient fatigue)
                                  (-> (HasPhysicalFinding $patient rhonchi)
                                      (DiagnosedWith $patient acute_bronchitis))))))))

;; Rule 8: Pleural effusion diagnosis 
!(add-reduct &medical_kb (: pleural_effusion_diagnosis_rule
                  (-> (Presents $patient dyspnea)
                      (-> (Presents $patient chest_pain)
                          (-> (HasPhysicalFinding $patient decreased_breath_sounds)
                              (-> (HasPhysicalFinding $patient dullness_to_percussion)
                                  (-> (Shows chest_xray $patient pleural_effusion)
                                      (DiagnosedWith $patient pleural_effusion))))))))

;; Rule 9: Allergic asthma diagnosis 
!(add-reduct &medical_kb (: allergic_asthma_diagnosis_rule
                  (-> (Presents $patient wheezing)
                      (-> (Presents $patient dyspnea)
                          (-> (HasRiskFactor $patient allergen_exposure)
                              (-> (Shows allergy_panel $patient environmental_allergens)
                                  (-> (Shows peak_flow $patient reduced_values)
                                      (DiagnosedWith $patient allergic_asthma))))))))

;; Rule 10: Occupational lung disease diagnosis 
!(add-reduct &medical_kb (: occupational_lung_disease_diagnosis_rule
                  (-> (Presents $patient persistent_cough)
                      (-> (Presents $patient dyspnea)
                          (-> (HasRiskFactor $patient occupational_dust_exposure)
                              (-> (Shows spirometry $patient obstructive_pattern)
                                  (-> (Shows chest_xray $patient infiltrates)
                                      (DiagnosedWith $patient pneumoconiosis))))))))

;; Rule 11: ARDS diagnosis 
!(add-reduct &medical_kb (: ards_diagnosis_rule
                  (-> (Presents $patient dyspnea)
                      (-> (Presents $patient tachypnea)
                          (-> (Presents $patient cyanosis)
                              (-> (Shows pulse_oximetry $patient hypoxemia)
                                  (-> (Shows arterial_blood_gas $patient respiratory_acidosis)
                                      (-> (Shows chest_xray $patient infiltrates)
                                          (DiagnosedWith $patient acute_respiratory_distress_syndrome)))))))))

;; Rule 12: Congestive heart failure with pulmonary edema 
!(add-reduct &medical_kb (: chf_pulmonary_edema_diagnosis_rule
                  (-> (Presents $patient orthopnea)
                      (-> (Presents $patient paroxysmal_nocturnal_dyspnea)
                          (-> (Presents $patient fatigue)
                              (-> (HasRiskFactor $patient cardiovascular_comorbidity)
                                  (-> (Shows echocardiogram $patient left_heart_failure)
                                      (-> (HasPhysicalFinding $patient rales)
                                          (DiagnosedWith $patient congestive_heart_failure_with_pulmonary_edema)))))))))

;; Rule 13: Laryngitis diagnosis 
!(add-reduct &medical_kb (: laryngitis_diagnosis_rule
                  (-> (Presents $patient hoarseness)
                      (-> (Presents $patient persistent_cough)
                          (-> (Presents $patient chest_tightness)
                              (DiagnosedWith $patient laryngitis))))))

;; Rule 14: Pneumothorax diagnosis 
!(add-reduct &medical_kb (: pneumothorax_diagnosis_rule
                  (-> (Presents $patient chest_pain)
                      (-> (Presents $patient dyspnea)
                          (-> (HasPhysicalFinding $patient decreased_breath_sounds)
                              (-> (Shows chest_xray $patient pneumothorax)
                                  (DiagnosedWith $patient pneumothorax)))))))

;; Rule 15: Severity classification 
!(add-reduct &medical_kb (: severe_respiratory_condition_rule
                  (-> (Presents $patient cyanosis)
                      (-> (Presents $patient tachypnea)
                          (-> (Shows pulse_oximetry $patient hypoxemia)
                              (-> (DiagnosedWith $patient $diagnosis)
                                  (ClassifiedAs $patient $diagnosis severe)))))))

;; Rule 16: Treatment indication 
!(add-reduct &medical_kb (: bronchodilator_indication_rule
                  (-> (DiagnosedWith $patient asthma)
                      (IndicatedFor $patient beta2_agonist_bronchodilators))))

!(add-reduct &medical_kb (: copd_treatment_indication_rule
                  (-> (DiagnosedWith $patient copd)
                      (IndicatedFor $patient long_acting_bronchodilators))))

!(add-reduct &medical_kb (: antibiotic_indication_rule
                  (-> (DiagnosedWith $patient pneumonia)
                      (IndicatedFor $patient broad_spectrum_antibiotics))))

!(add-reduct &medical_kb (: anti_tuberculosis_indication_rule
                  (-> (DiagnosedWith $patient pulmonary_tuberculosis)
                      (IndicatedFor $patient anti_tuberculosis_therapy))))

!(add-reduct &medical_kb (: anticoagulation_indication_rule
                  (-> (DiagnosedWith $patient pulmonary_embolism)
                      (IndicatedFor $patient anticoagulation_therapy))))

;; Rule 17: Comorbidity assessment 
!(add-reduct &medical_kb (: respiratory_comorbidity_rule
                  (-> (DiagnosedWith $patient copd)
                      (-> (DiagnosedWith $patient pneumonia)
                          (HasComorbidity $patient copd_pneumonia_overlap)))))

;; Rule 18: Contraindication 
!(add-reduct &medical_kb (: beta_blocker_contraindication_rule
                  (-> (DiagnosedWith $patient asthma)
                      (ContraindicatedFor $patient beta_blockers))))

;; Rule 19: Prognosis assessment
!(add-reduct &medical_kb (: poor_prognosis_rule
                  (-> (DiagnosedWith $patient lung_cancer)
                      (-> (ClassifiedAs $patient lung_cancer advanced_stage)
                          (HasPrognosis $patient poor_prognosis)))))

;; Rule 20: Follow-up requirement
!(add-reduct &medical_kb (: follow_up_requirement_rule
                  (-> (DiagnosedWith $patient pulmonary_tuberculosis)
                      (RequiresFollowUp $patient monthly_monitoring))))