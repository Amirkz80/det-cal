from django import forms

# creating a form
class InputForm(forms.Form):
    """A form to get n (matrix demensions number) from user"""

    n = forms.IntegerField(
        max_value=9,
        min_value=1,
        required=True,
        initial=1,
        label = '',
    )

class MatrixInputForm(forms.Form):
    """A form to take members of a matrix"""

    matrix_members = forms.IntegerField(
        required = True,
        initial=0,
        label='',
    )