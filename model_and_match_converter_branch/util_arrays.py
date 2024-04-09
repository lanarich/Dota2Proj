catboost_array = ['dire_POSITION_4_leaverStatus', 'radiant_POSITION_3_leaverStatus',
                              'radiant_POSITION_2_leaverStatus', 'dire_POSITION_5_leaverStatus',
                              'dire_POSITION_3_leaverStatus', 'dire_POSITION_2_leaverStatus',
                              'dire_POSITION_1_leaverStatus', 'radiant_POSITION_4_leaverStatus',
                              'radiant_POSITION_5_leaverStatus', 'radiant_POSITION_1_leaverStatus',
                              'dire_POSITION_5_isRadiant', 'dire_POSITION_4_intentionalFeeding',
                              'radiant_POSITION_5_isRadiant', 'dire_POSITION_5_intentionalFeeding',
                              'dire_POSITION_1_isRadiant', 'radiant_POSITION_3_intentionalFeeding',
                              'dire_POSITION_3_intentionalFeeding', 'radiant_POSITION_1_isRadiant',
                              'radiant_POSITION_4_isRadiant', 'radiant_POSITION_2_isRadiant',
                              'dire_POSITION_4_isRadiant', 'dire_POSITION_3_isRadiant',
                              'radiant_POSITION_3_isRadiant', 'radiant_POSITION_1_intentionalFeeding',
                              'radiant_POSITION_4_intentionalFeeding', 'radiant_POSITION_2_intentionalFeeding',
                              'dire_POSITION_2_isRadiant', 'dire_POSITION_1_intentionalFeeding',
                              'dire_POSITION_2_intentionalFeeding', 'radiant_POSITION_5_intentionalFeeding'
                              ]

columns_for_drop = ['_id', 'dire_POSITION_2_id', 'radiant_POSITION_4_id', 'radiant_POSITION_1_id',
                    'radiant_POSITION_2_position', 'startDateTime', 'radiant_POSITION_2_id', 'radiant_POSITION_5_id',
                    'dire_POSITION_2_position', 'radiant_POSITION_3_position', 'dire_POSITION_5_id',
                    'dire_POSITION_4_position', 'radiant_POSITION_5_position', 'dire_POSITION_1_id',
                    'durationSeconds', 'radiant_POSITION_4_position', 'dire_POSITION_4_id',
                    'dire_POSITION_1_position', 'radiant_POSITION_1_position', 'radiant_POSITION_3_id',
                    'dire_POSITION_3_id', 'id', 'dire_POSITION_3_position', 'gameMode', 'dire_POSITION_5_position',
                    ]

columns_with_leaver_status = ['dire_POSITION_4_leaverStatus', 'radiant_POSITION_3_leaverStatus',
                              'radiant_POSITION_2_leaverStatus', 'dire_POSITION_5_leaverStatus',
                              'dire_POSITION_3_leaverStatus', 'dire_POSITION_2_leaverStatus',
                              'dire_POSITION_1_leaverStatus', 'radiant_POSITION_4_leaverStatus',
                              'radiant_POSITION_5_leaverStatus', 'radiant_POSITION_1_leaverStatus']


columns_true_false_convert = ['dire_POSITION_5_isRadiant', 'dire_POSITION_4_intentionalFeeding',
                              'radiant_POSITION_5_isRadiant', 'dire_POSITION_5_intentionalFeeding',
                              'dire_POSITION_1_isRadiant', 'radiant_POSITION_3_intentionalFeeding',
                              'dire_POSITION_3_intentionalFeeding', 'radiant_POSITION_1_isRadiant',
                              'radiant_POSITION_4_isRadiant', 'radiant_POSITION_2_isRadiant',
                              'dire_POSITION_4_isRadiant', 'dire_POSITION_3_isRadiant',
                              'radiant_POSITION_3_isRadiant', 'radiant_POSITION_1_intentionalFeeding',
                              'radiant_POSITION_4_intentionalFeeding', 'radiant_POSITION_2_intentionalFeeding',
                              'dire_POSITION_2_isRadiant', 'dire_POSITION_1_intentionalFeeding',
                              'dire_POSITION_2_intentionalFeeding', 'radiant_POSITION_5_intentionalFeeding']