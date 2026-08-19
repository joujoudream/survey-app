# معالجة الضغط على Enter أو زر الحفظ
    if submitted or btn_save_manual:
        st.session_state.notification_msg = None
        st.session_state.notification_type = None

        # 🔹 الحالة 1: الضغط على Enter بعد إدخال اسم المنطقة فقط
        if region_val and not prop_val:
            st.session_state.region_input_val = region_val
            st.session_state.focus_field = "property"
            st.rerun()

        # 🔹 الحالة 2: الضغط على Enter بعد إدخال رقم العقار
        elif region_val and prop_val:
            is_duplicate = False
            if not df.empty:
                is_duplicate = df[(df["المنطقة"].str.strip().str.lower() == region_val.lower()) & (df["رقم العقار"].str.strip() == prop_val)].shape[0] > 0
            
            if is_duplicate:
                st.session_state.notification_msg = f"⚠️ العقار رقم [{prop_val}] مكرر ومسجل سابقاً في منطقة [{region_val}]!"
                st.session_state.notification_type = "error"
                
                # 🎯 زيادة العداد لتفريغ خانة رقم العقار فوراً
                st.session_state.prop_key_counter += 1
                st.session_state.region_input_val = region_val
                st.session_state.focus_field = "region"
            else:
                new_row = pd.DataFrame([{"المنطقة": region_val, "رقم العقار": prop_val}])
                st.session_state.local_db = pd.concat([st.session_state.local_db, new_row], ignore_index=True)
                
                sorted_df = st.session_state.local_db.sort_values(by=["المنطقة", "رقم العقار"]).reset_index(drop=True)
                sorted_df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
                upload_to_github(st.session_state.local_db)
                
                st.session_state.notification_msg = f"✅ تم حفظ العقار [{prop_val}] بنجاح في منطقة [{region_val}]!"
                st.session_state.notification_type = "success"
                
                # 🎯 زيادة العداد لتفريغ خانة رقم العقار فوراً
                st.session_state.prop_key_counter += 1
                st.session_state.region_input_val = region_val
                st.session_state.focus_field = "region"

            st.rerun()
