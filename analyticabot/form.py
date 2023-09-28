from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Upload a File', required=False)

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-fileUploadForm'
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'

    # class Meta:
    #     # model = Project
    #     fields = ['title', 'image', 'description', 'image_url']



 
# class UploadFileForm(forms.Form):
# 	file = forms.FileField()
 
# 	def __init__(self, *args, **kwargs):
#         super(UploadFileForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_id = 'id-uploadFileForm'
#         self.helper.form_method = 'post'
#         self.helper.form_enctype = 'multipart/form-data'
