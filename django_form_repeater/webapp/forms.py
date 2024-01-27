from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.forms.models import BaseModelFormSet, BaseInlineFormSet
from .models import *


class GrandParentForm(forms.ModelForm):

    class Meta:
        model = GrandParent
        fields = "__all__"


class ParentForm(forms.ModelForm):

    class Meta:
        model = Parent
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs = {"class": "parent-formset-field"}
        self.fields["gender"].widget.attrs = {"class": "parent-formset-field"}
        self.fields["age"].widget.attrs = {"class": "parent-formset-field"}
        self.fields["img"].widget.attrs = {"class": "parent-formset-field"}


class ChildForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs = {"class": "formset-field"}
        self.fields["gender"].widget.attrs = {"class": "formset-field"}
        self.fields["age"].widget.attrs = {"class": "formset-field"}
        self.fields["img"].widget.attrs = {"class": "formset-field"}


class GrandChildForm(forms.ModelForm):

    class Meta:
        model = GrandChild
        fields = "__all__"


class BaseParentFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseParentFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def add_fields(self, form, index):
        super(BaseParentFormset, self).add_fields(form, index)

        # adding child formset to parent form
        form.nested = child_formset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix="%s-%s" % (form.prefix, child_formset.get_default_prefix()), # make prefix as you like, here i am formating prefix like (parent formset prefix-child formset prefix)
        )

    def is_valid(self):
        result = super(BaseParentFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested"):
                    result = result and form.nested.is_valid()
        return result

    def save(self, commit=True):
        result = super(BaseParentFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested"):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)
        return result


class BaseChildFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseChildFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class BaseGrandChildFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseGrandChildFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


parent_formset = forms.inlineformset_factory(GrandParent, Parent, form=ParentForm, formset=BaseParentFormset, extra=1)
child_formset = forms.inlineformset_factory(Parent, Child, form=ChildForm, formset=BaseChildFormset, extra=1)



