from django import forms

from .models import RecordInfo, Record


class RecordInfoForm(forms.ModelForm):
    class Meta:
        model = RecordInfo
        fields = ("address",
                  "ill",
                  "temperature",
                  "symptom",
                  "symptom_list",
                  "hospital",
                  "hospital_location",
                  "medicine",
                  "medicine_detail",
                  "designate_location",
                  "live_type",
                  "phone",
                  )

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Record
#         fields = ('user_name', 'user_org', 'user_bind_num', 'phone', 'email', 'gender')
