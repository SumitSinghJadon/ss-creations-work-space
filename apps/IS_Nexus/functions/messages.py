from django.contrib import messages


def delete(request):
    messages.warning(request, 'Success! The entry has been deleted.')

def delete_error(request):
    messages.error(request, 'The entry you are trying to delete could not be found.')

def saved(request):
    messages.success(request, 'Data has been successfully saved!')
    
def saved_error(request,data=None):
    messages.error(request, 'It seems that there was an issue, and data could not be saved.' if not None else data)

def form_error(request):
    messages.error(request, 'Please review the form and fill in all required fields.')

def update(request):
    messages.success(request, 'Data has been successfully updated!')

def update_error(request):
    messages.error(request, 'The data you are trying to update could not be found.')

def unexpected_error(request):
    messages.error(request, 'It seems that there was an issue, Please try again.')

