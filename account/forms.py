from account.models import Account
from django import forms

class AccountForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "password", "profile_picture", "bio"]
        widgets = {
            "password": forms.PasswordInput(),
            "bio": forms.Textarea(attrs={"rows": 4, "cols": 40}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data["password"])
        if commit:
            account.save()
        return account
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "profile_picture", "bio"]