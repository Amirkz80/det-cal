from math import sqrt
import copy
from django.shortcuts import redirect, render
from calculator.forms import InputForm, MatrixInputForm
from django.forms import formset_factory


def two_in_two_matrix(matrix, length):
    """Section one : finding determinant of a 2*2 matrix"""
    determinant = (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

    return determinant


def minor(matrix, line, column):
    """A function to calculate the minor of a matrix"""

    matrix_copy = copy.deepcopy(matrix)
    
    # Deleting the (line)th line
    del matrix_copy[line]
    # Deleting the (column)th column
    for l in matrix_copy:
        del l[column]

    return matrix_copy


def big_matrix(matrix, length):
    """Section two : finding determinant of a matrix bigger than 2*2"""
    first_line = matrix[0]
    i = 0
    determinant = 0

    # Getting cofactors of each element in the first_line
    for element in first_line :
        
        # Getting minor of the matrix
        matrix_minor =  minor(matrix, 0, i)

        # If the minor of matrix was 2*2 then get the cofactor
        if len(matrix_minor) == 2 :
            if (i + 0) % 2 == 0 :
                cofactor = element * (two_in_two_matrix(matrix_minor, len(matrix_minor)))
            else :
                cofactor = (-1) * element * (two_in_two_matrix(matrix_minor, len(matrix_minor) ))
        # if the minor of the matrix was bigger than 2*2 get minor's det
        else :
            if (i + 0) % 2 == 0 :
                cofactor = element * big_matrix(matrix_minor, len(matrix_minor))
            else :
                cofactor = (-1) * element * big_matrix(matrix_minor, len(matrix_minor))
            
        i = i + 1
        # Summing up the result of cofactors
        determinant = determinant + cofactor

    return determinant


def main_page(request) :
    """Renders main page and gets the n (matrix demension number)"""
    
    if request.method != 'POST' :
        form = InputForm()
    
    else :

        form = InputForm(data=request.POST)
        if form.is_valid() :
            return redirect('calculator:set_demensions')

    context = {'form' : form}
    return render(request, 'calculator/main_page.html', context)


def set_demensions(request) :
    """A page to set numbers of matrix"""

    if 'n' in request.POST :

        demensions_number = int(request.POST['n'])
        matrix_formset = formset_factory(MatrixInputForm, extra = demensions_number * demensions_number)

        formset = matrix_formset()
        
        # See in which forms we go to the next row
        change_place = demensions_number
        change_list = []
        diff = change_place
        
        # See in wich indexes of forms should we go to the next row row
        while (change_place <= demensions_number * demensions_number) :
            change_list.append(change_place - 1)
            change_place = change_place + diff

        # Setting alerts to go to the next row in template, changing 
        Row = 1
        for form in formset :
            for number in change_list :
                if form.prefix == f'form-{number - (demensions_number - 1)}' :
                    form.keywargs = f'Row-{Row}'
                    Row = Row + 1

            
        # Setting alerts to go the next coulmn in template, defining kwargs for each form in formset
        column = 1
        for form in formset :
            form.form_kwargs = f'Column-{column} : '
            column = column + 1
            if column > demensions_number :
                column = column - demensions_number

    
        context = {'formset' : formset, 'demensions' : demensions_number}
        return render(request, "calculator/matrix_elements.html", context)     

    else :
        return redirect('calculator:main_page')


def result(request) :
    """Calculates the determinan of matrix and shows it in template"""

    if 'form-TOTAL_FORMS' in request.POST.keys() :
        
        demensions = int(request.POST['form-TOTAL_FORMS'])

        # Extracting matrix numbers from request forms and putting them in member list
        members = []
        for i in range(demensions) :
            member =  request.POST[f'form-{i}-matrix_members']
            
            # Change numbers to integer
            if bool(member) == False :
                member = 0

            try:
                member = int(member)
            except ValueError :
                member = int(float(member))
    
            members.append(member)

        # Making a final list based on list(rows) in lists
        change_place = int(demensions / sqrt(demensions) )
        change_list = []
        diff = change_place
        
        # See in wich indexes should program make nest row
        while (change_place <= demensions) :
            change_list.append(change_place - 1)
            change_place = change_place + diff

        # Braking the matrix into ((length)/demensions) parts
        rows = {}
        row = 0
        for j in range(demensions) :
            if f"row-{row+1}" not in rows.keys() :
                rows[f'row-{row+1}'] = []
            rows[f'row-{row+1}'].append(members[j])
            if j in change_list :
                row = row + 1

        # Final list that contains the final format of matrix
        matrix = []
        for value in rows.values() :
            matrix.append(value)       

        # Matrix is 1*1
        if sqrt(demensions) == 1 :
            determinant =  matrix[0][0]

        # Matrix is 2*2
        if sqrt(demensions) == 2 :
            determinant = two_in_two_matrix(matrix, sqrt(demensions))

        # Matrix is bigger than 2*2
        if sqrt(demensions) > 2 :
            determinant = big_matrix(matrix, sqrt(demensions))

        context = {'members' : members, 'matrix' : matrix, 'determinant' : determinant}
        return render(request, 'calculator/result.html', context)

    else :
        return redirect('calculator:main_page')    