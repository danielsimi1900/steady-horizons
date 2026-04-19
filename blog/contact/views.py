from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Prepare email
            full_message = f"Message from {name} ({email}):\n\n{message}"
            
            # Send email (In development, this will print to the console)
            send_mail(
                subject,
                full_message,
                email,
                ['admin@t1dsteadyhorizons.com'], # Replace with your email
                fail_silently=False,
            )
            
            messages.success(request, "Thank you for sharing! We've received your message.")
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})
